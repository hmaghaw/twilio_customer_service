from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import date, timedelta

app = Flask(__name__)
CORS(app)

db_config = {
    'host': 'coffeehome.ca',
    'port': 3307,
    #'host': 'dental_clinic_db',
    'user': 'clinicuser',
    'password': 'clinicpass',
    'database': 'dental_clinic'
}

def get_db():
    return mysql.connector.connect(**db_config)

@app.route("/patients", methods=["POST"])
def create_patient():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO patient (full_name, phone, email, dob, notes)
        VALUES (%s, %s, %s, %s, %s)
    """, (data["full_name"], data["phone"], data.get("email"), data.get("dob"), data.get("notes")))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"success": True, "message": "Patient created."}), 201

@app.route("/patients/<phone_number>", methods=["GET"])
def get_patient_by_phone(phone_number):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patient WHERE phone = %s", (phone_number,))
    patient = cursor.fetchone()
    cursor.close()
    conn.close()
    if patient:
        return jsonify(patient), 200
    else:
        return jsonify({"success": False, "message": "Patient not found."}), 404

@app.route("/appointments", methods=["POST"])
def create_appointment_from_details():
    data = request.json
    phone = data.get("phone")
    date = data.get("date")
    time = data.get("time")
    dentist_name = data.get("dentist_name")  # optional

    if not all([phone, date, time]):
        return jsonify({"success": False, "message": "Missing required fields."}), 400

    conn = get_db()
    cursor = conn.cursor()

    # Get patient_id by phone
    cursor.execute("SELECT patient_id FROM patient WHERE phone = %s", (phone,))
    patient = cursor.fetchone()
    if not patient:
        return jsonify({"success": False, "message": "Patient not found."}), 404
    patient_id = patient[0]

    # If dentist_name is given, find the matching schedule
    if dentist_name:
        cursor.execute("SELECT dentist_id FROM dentist WHERE full_name = %s", (dentist_name,))
        dentist = cursor.fetchone()
        if not dentist:
            return jsonify({"success": False, "message": "Dentist not found."}), 404
        dentist_id = dentist[0]

        cursor.execute("""
            SELECT schedule_id FROM schedule
            WHERE date = %s AND slot_start = %s AND dentist_id = %s AND status = 'available'
        """, (date, time, dentist_id))
    else:
        # If no dentist_name provided, find any available schedule for the date and time
        cursor.execute("""
            SELECT schedule_id FROM schedule
            WHERE date = %s AND slot_start = %s AND status = 'available'
            LIMIT 1
        """, (date, time))

    schedule = cursor.fetchone()
    if not schedule:
        return jsonify({"success": False, "message": "This time slot is not available"}), 200

    schedule_id = schedule[0]

    # Insert appointment
    cursor.execute("""
        INSERT INTO appointment (patient_id, schedule_id, status)
        VALUES (%s, %s, %s)
    """, (patient_id, schedule_id, "Scheduled"))

    # Mark the schedule as booked
    cursor.execute("""
        UPDATE schedule
        SET status = 'booked'
        WHERE schedule_id = %s
    """, (schedule_id,))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"success": True, "message": "Appointment created."}), 201


@app.route("/appointments/<int:appointment_id>", methods=["GET"])
def get_appointment(appointment_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM appointment WHERE appointment_id = %s", (appointment_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return jsonify(result), 200
    else:
        return jsonify({"success": False, "message": "Appointment not found"}), 429

@app.route("/schedule/available", methods=["POST"])
def get_next_available_times():
    data = request.json
    date = data.get("date")
    operator = data.get("operator", "any").lower()  # "before", "after", or "any"
    time = data.get("time", "00:00")  # default minimum time

    if not date:
        return jsonify({"success": False, "message": "Missing 'date' in request."}), 400

    # Validate and convert time to HH:MM:SS format
    try:
        hour, minute = map(int, time.split(":"))
        filter_time = f"{hour:02}:{minute:02}:00"
    except:
        return jsonify({"success": False, "message": "Invalid 'time' format. Use HH:MM."}), 400

    conn = get_db()
    cursor = conn.cursor()

    base_query = """
        SELECT DISTINCT date, slot_start
        FROM schedule
        WHERE status = 'available'
          AND date >= %s
    """

    params = [date]

    if operator == "before":
        base_query += " AND slot_start < %s"
        params.append(filter_time)
    elif operator == "after":
        base_query += " AND slot_start >= %s"
        params.append(filter_time)

    base_query += " ORDER BY date ASC, slot_start ASC LIMIT 3"

    cursor.execute(base_query, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Format results as "YYYY-MM-DD H:MM AM/PM"
    times = []
    for row in rows:
        date_str = row[0].strftime("%Y-%m-%d") if hasattr(row[0], "strftime") else str(row[0])
        total_seconds = int(row[1].total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes = remainder // 60

        suffix = "AM" if hours < 12 or hours == 24 else "PM"
        display_hour = hours % 12
        if display_hour == 0:
            display_hour = 12

        time_str = f"{display_hour}:{minutes:02} {suffix}"
        times.append(f"{time_str}")

    return jsonify({"success": True, "times": times}), 200

@app.route("/patients/modify", methods=["PUT"])
def modify_patient():
    data = request.json
    phone = data.get("phone")

    if not phone:
        return jsonify({"success": False, "message": "Missing phone to identify patient."}), 400

    fields_to_update = ["full_name", "phone", "email", "dob", "notes"]
    set_clauses = []
    values = []

    for field in fields_to_update:
        if field in data and field != "phone":
            set_clauses.append(f"{field} = %s")
            values.append(data[field])

    if not set_clauses:
        return jsonify({"success": False, "message": "No fields provided for update."}), 400

    conn = get_db()
    cursor = conn.cursor()

    # Check if patient with given phone exists
    cursor.execute("SELECT patient_id FROM patient WHERE phone = %s", (phone,))
    patient = cursor.fetchone()
    if not patient:
        cursor.close()
        conn.close()
        return jsonify({"success": False, "message": "Patient not found."}), 404

    # Append original phone at the end for WHERE clause
    values.append(phone)

    # Run the update query
    query = f"UPDATE patient SET {', '.join(set_clauses)} WHERE phone = %s"
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"success": True, "message": "Patient record updated."}), 200

@app.route("/appointments/list/by_phone", methods=["POST"])
def list_appointments_by_phone():
    data = request.json
    phone = data.get("phone")
    if not phone:
        return jsonify({"success": False, "message": "Missing phone number."}), 400

    today_str = date.today().strftime("%Y-%m-%d")

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.appointment_id, a.schedule_id, a.status, a.notes,
               s.date, s.slot_start
        FROM appointment a
        JOIN patient p ON a.patient_id = p.patient_id
        JOIN schedule s ON a.schedule_id = s.schedule_id
        WHERE p.phone = %s AND s.date >= %s
        ORDER BY s.date ASC, s.slot_start ASC
    """, (phone, today_str))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Format date as 'YYYY-MM-DD'
    for row in rows:
        if isinstance(row["date"], date):
            row["date"] = row["date"].strftime("%Y-%m-%d")
        if isinstance(row["slot_start"], timedelta):
            total_seconds = int(row["slot_start"].total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes = remainder // 60
            row["slot_start"] = f"{hours:02}:{minutes:02}"
    print(rows)

    return jsonify({"success": True, "appointments": rows}), 200


@app.route("/appointments/cancel/by_phone", methods=["DELETE"]) # Cancel Appointment
def cancel_appointment_by_phone():
    data = request.json
    phone = data.get("phone")
    date = data.get("date")
    time = data.get("time")

    if not all([phone, date, time]):
        return jsonify({"success": False, "message": "Missing phone, date, or time."}), 400

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT a.appointment_id, s.schedule_id
        FROM appointment a
        JOIN patient p ON a.patient_id = p.patient_id
        JOIN schedule s ON a.schedule_id = s.schedule_id
        WHERE p.phone = %s AND s.date = %s AND s.slot_start = %s AND s.date >= CURDATE()
    """, (phone, date, time))
    row = cursor.fetchone()

    if not row:
        return jsonify({"success": False, "message": "Appointment not found."}), 404

    appointment_id, schedule_id = row

    cursor.execute("UPDATE appointment SET status = 'Cancelled' WHERE appointment_id = %s", (appointment_id,))
    cursor.execute("UPDATE schedule SET status = 'available' WHERE schedule_id = %s", (schedule_id,))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"success": True, "message": "Appointment cancelled."}), 200

@app.route("/appointments/reschedule/by_phone", methods=["PUT"])
def reschedule_appointment_by_phone():
    data = request.json
    phone = data.get("phone")
    old_date = data.get("date")
    old_time = data.get("time")
    new_date = data.get("new_date")
    new_time = data.get("new_time")
    notes = data.get("notes")

    if not all([phone, old_date, old_time, new_date, new_time]):
        return jsonify({"success": False, "message": "Missing required fields for rescheduling."}), 400

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT a.appointment_id, s.schedule_id, p.patient_id
        FROM appointment a
        JOIN patient p ON a.patient_id = p.patient_id
        JOIN schedule s ON a.schedule_id = s.schedule_id
        WHERE p.phone = %s AND s.date = %s AND s.slot_start = %s AND s.date >= CURDATE()
    """, (phone, old_date, old_time))
    row = cursor.fetchone()

    if not row:
        return jsonify({"success": False, "message": "Current appointment not found."}), 404

    appointment_id, old_schedule_id, patient_id = row

    # Find new available slot
    cursor.execute("""
        SELECT schedule_id FROM schedule
        WHERE date = %s AND slot_start = %s AND status = 'available'
        LIMIT 1
    """, (new_date, new_time))
    new_schedule = cursor.fetchone()

    if not new_schedule:
        return jsonify({"success": False, "message": "No available slot found at the new date and time."}), 404

    new_schedule_id = new_schedule[0]

    # Cancel current, release slot, and book new
    cursor.execute("UPDATE appointment SET status = 'Cancelled' WHERE appointment_id = %s", (appointment_id,))
    cursor.execute("UPDATE schedule SET status = 'available' WHERE schedule_id = %s", (old_schedule_id,))
    cursor.execute("""
        INSERT INTO appointment (patient_id, schedule_id, status, notes)
        VALUES (%s, %s, 'Scheduled', %s)
    """, (patient_id, new_schedule_id, notes))
    cursor.execute("UPDATE schedule SET status = 'booked' WHERE schedule_id = %s", (new_schedule_id,))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"success": True, "message": "Appointment rescheduled."}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

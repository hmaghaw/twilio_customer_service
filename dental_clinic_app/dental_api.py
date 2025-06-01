from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

db_config = {
    'host': 'dental_clinic_db',
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
    shift = data.get("shift", "Anything")  # Default to no filter

    if not date:
        return jsonify({"success": False, "message": "Missing 'date' in request."}), 400

    conn = get_db()
    cursor = conn.cursor()

    # Dynamic query
    if shift in ("Morning", "Afternoon"):
        cursor.execute("""
            SELECT DISTINCT date, slot_start
            FROM schedule
            WHERE status = 'available'
              AND date >= %s
              AND shift = %s
            ORDER BY date ASC, slot_start ASC
            LIMIT 3
        """, (date, shift))
    else:
        cursor.execute("""
            SELECT DISTINCT date, slot_start
            FROM schedule
            WHERE status = 'available'
              AND date >= %s
            ORDER BY date ASC, slot_start ASC
            LIMIT 3
        """, (date,))

    rows = cursor.fetchall()
    times = [f"{str(row[1])[:4]}" for row in rows]

    cursor.close()
    conn.close()

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

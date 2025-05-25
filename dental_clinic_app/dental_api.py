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

@app.route("/patients/phone/<phone_number>", methods=["GET"])
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

@app.route("/patients/phone/<phone_number>", methods=["PUT"])
def update_patient_by_phone(phone_number):
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE patient SET full_name=%s, phone=%s, email=%s, dob=%s, notes=%s
        WHERE phone=%s
    """, (data["full_name"], data["phone"], data.get("email"), data.get("dob"), data.get("notes"), phone_number))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"success": True, "message": "Patient updated."}), 200

@app.route("/appointments", methods=["POST"])
def book_appointment():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO appointment (patient_id, dentist_id, service_id, scheduled_date, start_time, end_time, status, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (data["patient_id"], data["dentist_id"], data["service_id"], data["scheduled_date"],
          data["start_time"], data["end_time"], "Scheduled", data.get("notes")))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"success": True, "message": "Appointment booked."}), 201

@app.route("/dentists", methods=["GET"])
def list_dentists():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT full_name, specialization, working_days, start_time, end_time FROM dentist")
    dentists = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(dentists), 200

@app.route("/appointments/<int:appointment_id>", methods=["PUT"])
def modify_appointment(appointment_id):
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE appointment
        SET scheduled_date=%s, start_time=%s, end_time=%s, status=%s, notes=%s
        WHERE appointment_id=%s
    """, (data["scheduled_date"], data["start_time"], data["end_time"], data["status"], data.get("notes"), appointment_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"success": True, "message": "Appointment updated."}), 200

@app.route("/treatment-history/<phone_number>", methods=["GET"])
def list_treatment_history(phone_number):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT patient_id FROM patient WHERE phone = %s", (phone_number,))
    result = cursor.fetchone()
    if not result:
        cursor.close()
        conn.close()
        return jsonify({"success": False, "message": "Patient not found."}), 404

    patient_id = result["patient_id"]
    cursor.execute("""
        SELECT th.treatment_date, s.name AS service_name, th.description, th.tooth_number, th.procedure_code
        FROM treatment_history th
        JOIN appointment a ON th.appointment_id = a.appointment_id
        JOIN service s ON th.service_id = s.service_id
        WHERE a.patient_id = %s
        ORDER BY th.treatment_date DESC
    """, (patient_id,))
    history = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(history), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

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
    if not data:
        return jsonify({"success": False, "message": "No data provided."}), 400

    allowed_fields = ["full_name", "phone", "email", "dob", "notes"]
    set_clauses = []
    values = []

    for field in allowed_fields:
        if field in data:
            set_clauses.append(f"{field} = %s")
            values.append(data[field])

    if not set_clauses:
        return jsonify({"success": False, "message": "No valid fields to update."}), 400

    conn = get_db()
    cursor = conn.cursor()

    # Check if phone number exists
    cursor.execute("SELECT 1 FROM patient WHERE phone = %s", (phone_number,))
    if cursor.fetchone() is None:
        cursor.close()
        conn.close()
        return jsonify({"success": False, "message": "Patient with given phone number not found."}), 404

    # Build and execute update
    values.append(phone_number)
    query = f"""
        UPDATE patient
        SET {', '.join(set_clauses)}
        WHERE phone = %s
    """
    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"success": True, "message": "Patient updated."}), 200


@app.route("/appointments", methods=["POST"])
def create_appointment():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO appointment (patient_id, schedule_id, service_id, status, notes)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        data["patient_id"],
        data["schedule_id"],
        data["service_id"],
        data.get("status", "Scheduled"),
        data.get("notes")
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"success": True, "message": "Appointment updated."}), 200

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
        return jsonify({"success": False, "message": "Appointment not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

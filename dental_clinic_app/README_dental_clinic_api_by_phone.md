
# 🦷 Dental Clinic API (Phone-Based)

This REST API allows managing patients, dentists, appointments, and treatment history for a dental clinic system, using **phone numbers** as the key for patient records.

---

## 📦 Features

- Create and update patients by phone number
- Book, update, and cancel appointments
- List dentists and their working hours
- View treatment history using patient phone number
- Built with Flask, MySQL, Docker

---

## 🚀 Running the System

Ensure your directory structure is:

```
project-root/
├── docker-compose.yml
├── init_dental_clinic/
│   └── init.sql
└── dental_clinic_app/
    ├── dental_api_by_phone.py
    └── requirements.txt
```

Start with:

```bash
docker-compose up --build
```

If exposed via NGINX:

```
https://coffeehome.ca/api/dental_clinic/
```

---

## 🔌 API Endpoints (by Phone)

### ✅ Create Patient

**POST** `/patients`

```json
{
  "full_name": "Alice Johnson",
  "phone": "6475551234",
  "email": "alice@example.com",
  "dob": "1985-04-15",
  "notes": "New patient"
}
```

---

### 🔍 Get Patient by Phone

**GET** `/patients/phone/6475551234`

---

### ✏️ Update Patient by Phone

**PUT** `/patients/phone/6475551234`

```json
{
  "full_name": "Alice Johnson",
  "phone": "6475555678",
  "email": "alice@newmail.com",
  "dob": "1985-04-15",
  "notes": "Updated info"
}
```

---

### 📅 Book Appointment

**POST** `/appointments`

```json
{
  "patient_id": 1,
  "dentist_id": 1,
  "service_id": 1,
  "scheduled_date": "2025-06-01",
  "start_time": "09:00:00",
  "end_time": "09:30:00",
  "notes": "Teeth cleaning"
}
```

---

### 🛠 Modify or Cancel Appointment

**PUT** `/appointments/<appointment_id>`

```json
{
  "scheduled_date": "2025-06-03",
  "start_time": "10:00:00",
  "end_time": "10:30:00",
  "status": "Cancelled",
  "notes": "Rescheduled"
}
```

---

### 🧑‍⚕️ List Dentists

**GET** `/dentists`

Returns a list of dentists and their working hours.

---

### 📜 Get Treatment History by Phone

**GET** `/treatment-history/6475551234`

Returns all treatments performed for the patient with this phone number.

---

## 🔐 Environment Configuration

Ensure `.env` or `docker-compose.yml` includes:

```env
MYSQL_USER=clinicuser
MYSQL_PASSWORD=clinicpass
MYSQL_DATABASE=dental_clinic
```

---

## 📬 Contact

Questions? Email `support@coffeehome.ca`

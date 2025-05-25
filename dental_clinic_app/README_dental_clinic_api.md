
# 🦷 Dental Clinic API

This is a lightweight REST API for managing dental clinic operations including patients, appointments, dentists, treatments, and communications.

## 📦 Features

- Create and update patients
- Book, update, and cancel appointments
- List dentists and their working hours
- View treatment history by patient
- Built with Flask, MySQL, Docker

---

## 🚀 Getting Started

### 🐳 Run with Docker

Ensure your project has the following structure:

```
project-root/
├── docker-compose.yml
├── init_dental_clinic/
│   └── init.sql
└── dental_clinic_app/
    ├── dental_api.py
    └── requirements.txt
```

Start services:

```bash
docker-compose up --build
```

If you're exposing via NGINX on a domain like `https://coffeehome.ca`, then access the API at:

```
https://coffeehome.ca/api/dental_clinic/
```

---

## 🛠 API Endpoints

> All endpoints assume a base path of `/api/dental_clinic` if behind a reverse proxy.

---

### 📍 Create a Patient

**POST** `/patients`

```json
{
  "full_name": "Alice Johnson",
  "phone": "6475551234",
  "email": "alice@example.com",
  "dob": "1985-04-15",
  "notes": "Allergic to penicillin"
}
```

---

### ✏️ Update a Patient

**PUT** `/patients/<patient_id>`

```json
{
  "full_name": "Alice Johnson",
  "phone": "6475555678",
  "email": "alice.j@example.com",
  "dob": "1985-04-15",
  "notes": "Updated allergy info"
}
```

---

### 📅 Book an Appointment

**POST** `/appointments`

```json
{
  "patient_id": 1,
  "dentist_id": 2,
  "service_id": 4,
  "scheduled_date": "2025-06-01",
  "start_time": "10:00:00",
  "end_time": "10:30:00",
  "notes": "Follow-up for braces"
}
```

---

### 🔁 Update or Cancel Appointment

**PUT** `/appointments/<appointment_id>`

```json
{
  "scheduled_date": "2025-06-03",
  "start_time": "11:00:00",
  "end_time": "11:30:00",
  "status": "Cancelled",
  "notes": "Rescheduled"
}
```

---

### 🧑‍⚕️ List Dentists

**GET** `/dentists`

Returns:

```json
[
  {
    "full_name": "Dr. Emily Adams",
    "specialization": "General Dentistry",
    "working_days": "Mon-Fri",
    "start_time": "09:00:00",
    "end_time": "17:00:00"
  }
]
```

---

### 🦷 Get Treatment History

**GET** `/treatment-history/<patient_id>`

Example:

```bash
curl https://coffeehome.ca/api/dental_clinic/treatment-history/1
```

Returns:

```json
[
  {
    "treatment_date": "2025-05-29",
    "service_name": "Cavity Filling",
    "description": "Filled cavity in upper left molar",
    "tooth_number": "26",
    "procedure_code": "FILL123"
  }
]
```

---

## 🔐 Environment Variables

Ensure the following environment is set in `docker-compose.yml`:

```env
MYSQL_USER=clinicuser
MYSQL_PASSWORD=clinicpass
MYSQL_DATABASE=dental_clinic
```

---

## 📬 Contact

For questions or support, contact: `support@coffeehome.ca`

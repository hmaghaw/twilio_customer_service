# Dental Clinic API

This API powers a dental clinic management system, allowing operations such as creating patients, booking appointments, managing schedules, and more.

## Base URL

```
https://<your-domain>/api/dental_clinic
```

---

## Endpoints

### 1. **Create Patient**
**POST** `/patients`

Create a new patient.

#### Body:
```json
{
  "full_name": "John Doe",
  "phone": "6471234567",
  "email": "john@example.com",
  "dob": "1990-01-01",
  "notes": "Has allergies"
}
```

#### Response:
```json
{
  "success": true,
  "message": "Patient created."
}
```

---

### 2. **Get Patient by Phone**
**GET** `/patients/<phone_number>`

Returns patient details by phone number.

#### Example:
`/patients/6471234567`

---

### 3. **Modify Patient**
**PUT** `/patients/modify`

Update patient details using phone as the identifier.

#### Body:
```json
{
  "phone": "6471234567",
  "full_name": "Johnny Doe",
  "email": "johnny@example.com"
}
```

---

### 4. **Create Appointment**
**POST** `/appointments`

Create an appointment. `dentist_name` is optional.

#### Body:
```json
{
  "phone": "6471234567",
  "date": "2025-06-05",
  "time": "10:30",
  "dentist_name": "Dr. Smith"
}
```

---

### 5. **List Appointments by Phone**
**POST** `/appointments/list/by_phone`

List upcoming appointments for a given phone.

#### Body:
```json
{
  "phone": "6471234567"
}
```

---

### 6. **Cancel Appointment by Phone**
**DELETE** `/appointments/cancel/by_phone`

Cancel a future appointment using patient phone, date, and time.

#### Body:
```json
{
  "phone": "6471234567",
  "date": "2025-06-05",
  "time": "10:30"
}
```

---

### 7. **Reschedule Appointment by Phone**
**PUT** `/appointments/reschedule/by_phone`

Reschedule an appointment to a new time and date.

#### Body:
```json
{
  "phone": "6471234567",
  "date": "2025-06-05",
  "time": "10:30",
  "new_date": "2025-06-07",
  "new_time": "11:00",
  "notes": "Change requested"
}
```

---

### 8. **Available Time Slots**
**POST** `/schedule/available`

Returns next 3 available time slots starting from a given date.

#### Body:
```json
{
  "date": "2025-06-05",
  "operator": "after",
  "time": "10:00"
}
```

---

### 9. **Generate Monthly Schedule**
**POST** `/schedule/generate_month`

Generate dentist schedules for a given month and year. Cannot be used if that month already exists.

#### Body:
```json
{
  "month": 6,
  "year": 2025
}
```
CREATE SCHEMA IF NOT EXISTS dental_clinic;
USE dental_clinic;

CREATE TABLE patient (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    dob DATE,
    notes TEXT
);

CREATE TABLE dentist (
    dentist_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100),
    working_days VARCHAR(50),
    start_time TIME,
    end_time TIME
);

CREATE TABLE service (
    service_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT
);

CREATE TABLE appointment (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    dentist_id INT NOT NULL,
    service_id INT NOT NULL,
    scheduled_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status ENUM('Scheduled', 'Cancelled', 'Completed') DEFAULT 'Scheduled',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id),
    FOREIGN KEY (dentist_id) REFERENCES dentist(dentist_id),
    FOREIGN KEY (service_id) REFERENCES service(service_id)
);

CREATE TABLE treatment_history (
    treatment_id INT AUTO_INCREMENT PRIMARY KEY,
    appointment_id INT NOT NULL,
    dentist_id INT NOT NULL,
    service_id INT NOT NULL,
    description TEXT NOT NULL,
    procedure_code VARCHAR(50),
    tooth_number VARCHAR(10),
    treatment_date DATE NOT NULL,
    FOREIGN KEY (appointment_id) REFERENCES appointment(appointment_id),
    FOREIGN KEY (dentist_id) REFERENCES dentist(dentist_id),
    FOREIGN KEY (service_id) REFERENCES service(service_id)
);

CREATE TABLE call_script (
    script_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    purpose TEXT,
    script_text TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE communication_log (
    communication_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    type ENUM('SMS', 'Email', 'Phone') NOT NULL,
    direction ENUM('Incoming', 'Outgoing') NOT NULL,
    subject VARCHAR(150),
    message TEXT NOT NULL,
    script_id INT,
    status ENUM('Queued', 'Sent', 'Failed') DEFAULT 'Queued',
    phone_used VARCHAR(20),
    email_used VARCHAR(150),
    sent_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    error_message TEXT,
    recording_url VARCHAR(255),
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id),
    FOREIGN KEY (script_id) REFERENCES call_script(script_id)
);

-- Sample Data

INSERT INTO patient (full_name, phone, email, dob, notes) VALUES
('Alice Johnson', '6475551234', 'alice@example.com', '1985-04-15', 'Allergic to penicillin'),
('Bob Smith', '6475555678', 'bob@example.com', '1990-07-30', NULL),
('Carol Lee', '6475559012', 'carol@example.com', '1978-12-10', 'Prefers morning appointments');

INSERT INTO dentist (full_name, specialization, working_days, start_time, end_time) VALUES
('Dr. Emily Adams', 'General Dentistry', 'Mon-Fri', '09:00:00', '17:00:00'),
('Dr. Raj Patel', 'Orthodontics', 'Tue-Sat', '10:00:00', '18:00:00');

INSERT INTO service (name, price, description) VALUES
('Teeth Cleaning', 120.00, 'Routine cleaning and plaque removal'),
('Cavity Filling', 200.00, 'Composite resin filling for small cavities'),
('Tooth Extraction', 300.00, 'Simple extraction of a single tooth'),
('Braces Consultation', 150.00, 'Initial evaluation for orthodontic treatment');

INSERT INTO appointment (patient_id, dentist_id, service_id, scheduled_date, start_time, end_time, status, notes) VALUES
(1, 1, 1, '2025-05-27', '09:00:00', '09:30:00', 'Scheduled', 'First visit'),
(2, 2, 4, '2025-05-28', '11:00:00', '11:45:00', 'Scheduled', NULL),
(3, 1, 2, '2025-05-29', '10:30:00', '11:00:00', 'Scheduled', 'Complaining about sensitivity');

INSERT INTO treatment_history (appointment_id, dentist_id, service_id, description, procedure_code, tooth_number, treatment_date) VALUES
(1, 1, 1, 'Full teeth cleaning using ultrasonic scaler', 'CLEAN001', NULL, '2025-05-27'),
(1, 1, 1, 'Performed routine cleaning with fluoride rinse', 'CLEAN002', NULL, '2025-05-27'),
(1, 1, 1, 'Polished teeth and provided oral hygiene instructions', 'CLEAN003', NULL, '2025-05-27'),
(1, 1, 1, 'Detected minor gingivitis, advised improved brushing routine', 'DIAGG01', NULL, '2025-05-27'),
(1, 1, 1, 'Noted sensitivity in upper canines, recommended sensitivity toothpaste', 'SENSI001', '13', '2025-05-27'),
(2, 2, 4, 'Initial braces consultation, advised full x-ray and records', 'CONS101', NULL, '2025-05-28'),
(2, 2, 4, 'Discussed treatment plan for metal braces, patient agreed', 'CONS102', NULL, '2025-05-28'),
(2, 2, 4, 'Took impressions for orthodontic modeling', 'ORTHO001', NULL, '2025-05-28'),
(3, 1, 2, 'Filled cavity in upper left molar', 'FILL123', '26', '2025-05-29'),
(3, 1, 2, 'Applied local anesthesia and filled a cavity on lower right premolar', 'FILL456', '44', '2025-05-29'),
(3, 1, 2, 'Checked bite alignment post-filling, no issues found', 'CHK001', NULL, '2025-05-29'),
(3, 1, 2, 'Scheduled follow-up in 2 weeks to monitor filling durability', 'FOLLW01', NULL, '2025-05-29');

INSERT INTO call_script (title, purpose, script_text, is_active) VALUES
('Appointment Reminder', 'Remind patients of upcoming appointments', 'Hello, this is a reminder from Smile Dental. Your appointment is on [DATE] at [TIME]. Please confirm or call us to reschedule.', TRUE),
('Missed Appointment Follow-up', 'Contact patients who missed their appointments', 'We noticed you missed your dental appointment. Please call us to reschedule at your convenience.', TRUE);

INSERT INTO communication_log (patient_id, type, direction, subject, message, script_id, status, phone_used, email_used, sent_at, recording_url) VALUES
(1, 'SMS', 'Outgoing', NULL, 'Reminder: Appointment at Smile Dental on May 27 at 9:00 AM.', NULL, 'Sent', '6475551234', NULL, '2025-05-26 08:00:00', NULL),
(2, 'Phone', 'Outgoing', NULL, 'Automated call made for braces consultation', 1, 'Sent', '6475555678', NULL, '2025-05-27 12:00:00', 'https://twilio.recordings/abc123'),
(3, 'Email', 'Outgoing', 'Appointment Confirmation', 'Your appointment for cavity filling is confirmed on May 29 at 10:30 AM.', NULL, 'Sent', NULL, 'carol@example.com', '2025-05-26 13:00:00', NULL);

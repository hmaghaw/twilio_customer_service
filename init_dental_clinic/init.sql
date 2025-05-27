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
    specialization VARCHAR(100)
);

CREATE TABLE service (
    service_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT
);

-- Dentist-Service Eligibility
CREATE TABLE dentist_service_eligibility (
    dentist_id INT NOT NULL,
    service_id INT NOT NULL,
    PRIMARY KEY (dentist_id, service_id),
    FOREIGN KEY (dentist_id) REFERENCES dentist(dentist_id),
    FOREIGN KEY (service_id) REFERENCES service(service_id)
);


-- Schedule Table
CREATE TABLE schedule (
    schedule_id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    shift ENUM('Morning', 'Afternoon') NOT NULL,
    slot_start TIME NOT NULL,  -- 30-minute slot start
    dentist_id INT NOT NULL,
    FOREIGN KEY (dentist_id) REFERENCES dentist(dentist_id)
);

-- Appointment Table
CREATE TABLE appointment (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    schedule_id INT NOT NULL,
    service_id INT NOT NULL,
    status ENUM('Scheduled', 'Cancelled', 'Completed') DEFAULT 'Scheduled',
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id),
    FOREIGN KEY (schedule_id) REFERENCES schedule(schedule_id),
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
('Alice Johnson', '6471111111', 'alice@example.com', '1990-01-15', 'N/A'),
('Bob Smith', '6472222222', 'bob@example.com', '1985-05-20', 'Prefers morning appointments'),
('Carol White', '6473333333', 'carol@example.com', '1978-09-30', 'Has insurance with Sun Life');


INSERT INTO dentist (full_name, specialization) VALUES
('Dr. Ahmed Hassan', 'General Dentistry'),
('Dr. Lisa Chen', 'Orthodontics');


INSERT INTO service (name, price, description) VALUES
('Cleaning', 100.00, 'Standard dental cleaning'),
('Whitening', 200.00, 'Teeth whitening treatment'),
('Braces Consultation', 150.00, 'Initial consultation for braces');


INSERT INTO dentist_service_eligibility (dentist_id, service_id) VALUES
(1, 1),
(1, 2),
(2, 3);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Morning', '09:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Morning', '09:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Morning', '09:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Morning', '09:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Morning', '10:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Morning', '10:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Morning', '10:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Morning', '10:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Morning', '11:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Morning', '11:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Morning', '11:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Morning', '11:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Morning', '12:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Morning', '12:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Morning', '12:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Morning', '12:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Morning', '13:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Morning', '13:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Morning', '13:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Morning', '13:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Afternoon', '14:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Afternoon', '14:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Afternoon', '14:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Afternoon', '14:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Afternoon', '15:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Afternoon', '15:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Afternoon', '15:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Afternoon', '15:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Afternoon', '16:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Afternoon', '16:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Afternoon', '16:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Afternoon', '16:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Afternoon', '17:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Afternoon', '17:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Afternoon', '17:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Afternoon', '17:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Afternoon', '18:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Afternoon', '18:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Afternoon', '18:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-27', 'Afternoon', '18:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Morning', '09:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Morning', '09:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Morning', '09:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Morning', '09:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Morning', '10:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Morning', '10:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Morning', '10:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Morning', '10:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Morning', '11:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Morning', '11:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Morning', '11:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Morning', '11:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Morning', '12:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Morning', '12:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Morning', '12:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Morning', '12:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Morning', '13:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Morning', '13:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Morning', '13:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Morning', '13:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Afternoon', '14:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Afternoon', '14:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Afternoon', '14:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Afternoon', '14:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Afternoon', '15:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Afternoon', '15:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Afternoon', '15:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Afternoon', '15:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Afternoon', '16:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Afternoon', '16:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Afternoon', '16:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Afternoon', '16:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Afternoon', '17:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Afternoon', '17:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Afternoon', '17:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Afternoon', '17:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Afternoon', '18:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Afternoon', '18:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Afternoon', '18:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-28', 'Afternoon', '18:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Morning', '09:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Morning', '09:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Morning', '09:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Morning', '09:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Morning', '10:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Morning', '10:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Morning', '10:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Morning', '10:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Morning', '11:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Morning', '11:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Morning', '11:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Morning', '11:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Morning', '12:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Morning', '12:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Morning', '12:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Morning', '12:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Morning', '13:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Morning', '13:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Morning', '13:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Morning', '13:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Afternoon', '14:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Afternoon', '14:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Afternoon', '14:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Afternoon', '14:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Afternoon', '15:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Afternoon', '15:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Afternoon', '15:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Afternoon', '15:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Afternoon', '16:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Afternoon', '16:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Afternoon', '16:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Afternoon', '16:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Afternoon', '17:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Afternoon', '17:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Afternoon', '17:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Afternoon', '17:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Afternoon', '18:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Afternoon', '18:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Afternoon', '18:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-29', 'Afternoon', '18:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Morning', '09:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Morning', '09:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Morning', '09:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Morning', '09:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Morning', '10:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Morning', '10:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Morning', '10:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Morning', '10:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Morning', '11:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Morning', '11:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Morning', '11:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Morning', '11:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Morning', '12:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Morning', '12:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Morning', '12:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Morning', '12:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Morning', '13:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Morning', '13:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Morning', '13:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Morning', '13:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Afternoon', '14:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Afternoon', '14:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Afternoon', '14:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Afternoon', '14:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Afternoon', '15:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Afternoon', '15:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Afternoon', '15:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Afternoon', '15:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Afternoon', '16:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Afternoon', '16:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Afternoon', '16:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Afternoon', '16:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Afternoon', '17:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Afternoon', '17:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Afternoon', '17:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Afternoon', '17:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Afternoon', '18:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Afternoon', '18:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Afternoon', '18:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-30', 'Afternoon', '18:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Morning', '09:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Morning', '09:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Morning', '09:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Morning', '09:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Morning', '10:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Morning', '10:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Morning', '10:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Morning', '10:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Morning', '11:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Morning', '11:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Morning', '11:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Morning', '11:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Morning', '12:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Morning', '12:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Morning', '12:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Morning', '12:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Morning', '13:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Morning', '13:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Morning', '13:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Morning', '13:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Afternoon', '14:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Afternoon', '14:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Afternoon', '14:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Afternoon', '14:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Afternoon', '15:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Afternoon', '15:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Afternoon', '15:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Afternoon', '15:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Afternoon', '16:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Afternoon', '16:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Afternoon', '16:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Afternoon', '16:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Afternoon', '17:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Afternoon', '17:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Afternoon', '17:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Afternoon', '17:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Afternoon', '18:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Afternoon', '18:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Afternoon', '18:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-05-31', 'Afternoon', '18:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Morning', '09:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Morning', '09:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Morning', '09:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Morning', '09:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Morning', '10:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Morning', '10:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Morning', '10:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Morning', '10:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Morning', '11:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Morning', '11:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Morning', '11:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Morning', '11:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Morning', '12:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Morning', '12:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Morning', '12:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Morning', '12:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Morning', '13:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Morning', '13:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Morning', '13:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Morning', '13:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Afternoon', '14:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Afternoon', '14:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Afternoon', '14:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Afternoon', '14:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Afternoon', '15:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Afternoon', '15:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Afternoon', '15:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Afternoon', '15:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Afternoon', '16:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Afternoon', '16:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Afternoon', '16:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Afternoon', '16:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Afternoon', '17:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Afternoon', '17:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Afternoon', '17:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Afternoon', '17:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Afternoon', '18:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Afternoon', '18:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Afternoon', '18:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-01', 'Afternoon', '18:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Morning', '09:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Morning', '09:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Morning', '09:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Morning', '09:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Morning', '10:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Morning', '10:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Morning', '10:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Morning', '10:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Morning', '11:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Morning', '11:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Morning', '11:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Morning', '11:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Morning', '12:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Morning', '12:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Morning', '12:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Morning', '12:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Morning', '13:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Morning', '13:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Morning', '13:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Morning', '13:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Afternoon', '14:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Afternoon', '14:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Afternoon', '14:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Afternoon', '14:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Afternoon', '15:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Afternoon', '15:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Afternoon', '15:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Afternoon', '15:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Afternoon', '16:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Afternoon', '16:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Afternoon', '16:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Afternoon', '16:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Afternoon', '17:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Afternoon', '17:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Afternoon', '17:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Afternoon', '17:30:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Afternoon', '18:00:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Afternoon', '18:00:00', 2);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Afternoon', '18:30:00', 1);


INSERT INTO schedule (date, shift, slot_start, dentist_id)
VALUES ('2025-06-02', 'Afternoon', '18:30:00', 2);


INSERT INTO appointment (patient_id, schedule_id, service_id, status, notes)
VALUES (1, 1, 1, 'Scheduled', 'Initial cleaning appointment');


INSERT INTO call_script (title, purpose, script_text, is_active)
VALUES ('Appointment Reminder', 'Remind patient of upcoming appointment', 'Hello, this is a reminder for your dental appointment.', TRUE);


INSERT INTO communication_log (
    patient_id, type, direction, subject, message, script_id,
    status, phone_used, email_used, sent_at, error_message, recording_url
) VALUES (
    1, 'Phone', 'Outgoing', NULL, 'Reminder call for appointment',
    1, 'Sent', '6471111111', 'alice@example.com', NOW(), NULL, NULL
);

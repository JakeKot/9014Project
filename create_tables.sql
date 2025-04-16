DROP DATABASE IF EXISTS clinic_db;
CREATE DATABASE clinic_db;
USE clinic_db;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS QueueInfo, Prescriptions, Billing, MedicalRecords, Appointments, Providers, Medications, Patients;
SET FOREIGN_KEY_CHECKS = 1;

-- Patients
CREATE TABLE Patients (
    PatientID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    DateOfBirth DATE,
    Gender ENUM('Male', 'Female', 'Other'),
    ContactInfo TEXT,
    InsuranceNumber VARCHAR(20)
);

-- Providers
CREATE TABLE Providers (
    ProviderID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Specialty VARCHAR(100),
    AvailableTime VARCHAR(100),
    ContactInfo TEXT
);

-- Medications
CREATE TABLE Medications (
    MedicationID INT AUTO_INCREMENT PRIMARY KEY,
    MedicationName VARCHAR(100) UNIQUE,
    Description TEXT,
    Manufacturer VARCHAR(100),
    Stock INT,
    ExpirationDate DATE
);

-- Appointments
CREATE TABLE Appointments (
    AppointmentID INT AUTO_INCREMENT PRIMARY KEY,
    PatientID INT,
    ProviderID INT,
    AppointmentDate DATETIME,
    Symptom TEXT,
    TimeSlot VARCHAR(50),
    Status ENUM('Scheduled', 'Completed', 'Cancelled'),
    Notes TEXT,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID),
    FOREIGN KEY (ProviderID) REFERENCES Providers(ProviderID)
);

-- MedicalRecords
CREATE TABLE MedicalRecords (
    RecordID INT AUTO_INCREMENT PRIMARY KEY,
    PatientID INT,
    Diagnosis VARCHAR(100),
    VisitDate DATETIME,
    MedicalHistory TEXT,
    MainSymptoms VARCHAR(255),
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
);

-- Prescriptions (enhanced: includes PatientID, Diagnosis, Medication)
CREATE TABLE Prescriptions (
    PrescriptionID INT AUTO_INCREMENT PRIMARY KEY,
    PatientID INT,
    RecordID INT,
    MedicationID INT,
    Diagnosis VARCHAR(100),
    MedicationName VARCHAR(100),
    Dosage VARCHAR(50),
    Duration VARCHAR(50),
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID),
    FOREIGN KEY (RecordID) REFERENCES MedicalRecords(RecordID),
    FOREIGN KEY (MedicationID) REFERENCES Medications(MedicationID)
);

-- Billing
CREATE TABLE Billing (
    BillID INT AUTO_INCREMENT PRIMARY KEY,
    PatientID INT,
    ExaminationFee DECIMAL(10,2),
    MedicationFee DECIMAL(10,2),
    TotalFee DECIMAL(10,2),
    PaymentStatus VARCHAR(20),
    PaymentTime DATETIME,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
);

-- New: QueueInfo
CREATE TABLE QueueInfo (
    QueueID INT AUTO_INCREMENT PRIMARY KEY,
    PatientID INT,
    ProviderID INT,
    QueueNumber INT,
    QueueStatus ENUM('Waiting', 'InProgress', 'Completed', 'Skipped'),
    QueueTime DATETIME,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID),
    FOREIGN KEY (ProviderID) REFERENCES Providers(ProviderID)
);
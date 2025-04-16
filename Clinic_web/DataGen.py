import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="9014-Project",  # ← replace with your actual password
    database="clinic_db"
)
cursor = conn.cursor()

# Generate patients
def generate_patients(n):
    for _ in range(n):
        cursor.execute("""
        INSERT INTO Patients (FirstName, LastName, DateOfBirth, Gender, ContactInfo, InsuranceNumber)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            fake.first_name(), fake.last_name(),
            fake.date_of_birth(minimum_age=0, maximum_age=100),
            random.choice(['Male', 'Female', 'Other']),
            fake.phone_number() + ", " + fake.email(),
            'INS' + str(fake.random_number(digits=6))
        ))

# Generate providers
def generate_providers():
    specialties = ['Cardiologist', 'Dentist', 'Pediatrician', 'Neurologist', 'Surgeon']
    for _ in range(10):
        cursor.execute("""
        INSERT INTO Providers (FirstName, LastName, Specialty, AvailableTime, ContactInfo)
        VALUES (%s, %s, %s, %s, %s)
        """, (
            "Dr. " + fake.first_name(), fake.last_name(),
            random.choice(specialties),
            random.choice(['9AM-5PM', '10AM-6PM']),
            fake.phone_number() + ", " + fake.email()
        ))

# Generate medications with manufacturer, stock, expiration
def generate_medications():
    meds = [
        'Tylenol', 'Advil', 'Ibuprofen', 'Amoxicillin', 'Ciprofloxacin',
        'Azithromycin', 'Paracetamol', 'Aspirin', 'Naproxen', 'Metformin',
        'Omeprazole', 'Lisinopril', 'Losartan', 'Atorvastatin', 'Albuterol',
        'Hydrochlorothiazide', 'Prednisone', 'Levothyroxine', 'Gabapentin', 'Zyrtec'
    ]
    for med in meds:
        cursor.execute("""
        INSERT INTO Medications (MedicationName, Description, Manufacturer, Stock, ExpirationDate)
        VALUES (%s, %s, %s, %s, %s)
        """, (
            med, fake.sentence(),
            fake.company(),
            random.randint(50, 500),
            fake.date_between(start_date="+30d", end_date="+365d")
        ))

# Generate appointments
def generate_appointments(n):
    cursor.execute("SELECT PatientID FROM Patients")
    patients = [r[0] for r in cursor.fetchall()]
    cursor.execute("SELECT ProviderID FROM Providers")
    providers = [r[0] for r in cursor.fetchall()]
    for _ in range(n):
        cursor.execute("""
        INSERT INTO Appointments (PatientID, ProviderID, AppointmentDate, Symptom, TimeSlot, Status, Notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            random.choice(patients), random.choice(providers),
            fake.date_time_between(start_date='-30d', end_date='+30d'),
            fake.sentence(), random.choice(['Morning', 'Afternoon', 'Evening']),
            random.choice(['Scheduled', 'Completed', 'Cancelled']),
            fake.sentence()
        ))

# Generate medical records
def generate_medical_records(n):
    cursor.execute("SELECT PatientID FROM Patients")
    patients = [r[0] for r in cursor.fetchall()]
    for _ in range(n):
        cursor.execute("""
        INSERT INTO MedicalRecords (PatientID, Diagnosis, VisitDate, MedicalHistory, MainSymptoms)
        VALUES (%s, %s, %s, %s, %s)
        """, (
            random.choice(patients),
            random.choice(['Cold', 'Fever', 'Injury', 'Headache']),
            fake.date_time_between(start_date='-60d', end_date='now'),
            fake.text(), fake.sentence()
        ))

# Generate prescriptions with embedded info
def generate_prescriptions(n):
    cursor.execute("SELECT RecordID, PatientID FROM MedicalRecords")
    records = cursor.fetchall()
    cursor.execute("SELECT MedicationID, MedicationName FROM Medications")
    meds = cursor.fetchall()
    for _ in range(n):
        record = random.choice(records)
        med = random.choice(meds)
        cursor.execute("""
        INSERT INTO Prescriptions (PatientID, RecordID, MedicationID, Diagnosis, MedicationName, Dosage, Duration)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            record[1], record[0], med[0],
            random.choice(['Cold', 'Fever', 'Injury', 'Headache']),
            med[1],
            random.choice(['500mg', '200mg', '1 tablet']),
            random.choice(['3 days', '1 week'])
        ))

# Generate billing
def generate_billing(n):
    cursor.execute("SELECT PatientID FROM Patients")
    patients = [r[0] for r in cursor.fetchall()]
    for _ in range(n):
        exam = round(random.uniform(50, 200), 2)
        med = round(random.uniform(10, 100), 2)
        cursor.execute("""
        INSERT INTO Billing (PatientID, ExaminationFee, MedicationFee, TotalFee, PaymentStatus, PaymentTime)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            random.choice(patients), exam, med, exam + med,
            random.choice(['Paid', 'Pending']),
            fake.date_time_between(start_date='-30d', end_date='now')
        ))

# Generate queue info
def generate_queue_info(n):
    cursor.execute("SELECT PatientID FROM Patients")
    patients = [r[0] for r in cursor.fetchall()]
    cursor.execute("SELECT ProviderID FROM Providers")
    providers = [r[0] for r in cursor.fetchall()]
    for i in range(n):
        cursor.execute("""
        INSERT INTO QueueInfo (PatientID, ProviderID, QueueNumber, QueueStatus, QueueTime)
        VALUES (%s, %s, %s, %s, %s)
        """, (
            random.choice(patients), random.choice(providers),
            i + 1,
            random.choice(['Waiting', 'InProgress', 'Completed', 'Skipped']),
            fake.date_time_between(start_date='-1d', end_date='now')
        ))

# Execute all generators
generate_patients(1000)
generate_providers()
generate_medications()
generate_appointments(3000)
generate_medical_records(1500)
generate_prescriptions(2000)
generate_billing(500)
generate_queue_info(500)

# Commit and close
conn.commit()
cursor.close()
conn.close()

print("✅ All fake data inserted successfully.")
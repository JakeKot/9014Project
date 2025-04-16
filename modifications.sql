-- Modification 1: Update the status of all 'Pending' bills to 'Paid'
UPDATE Billing
SET PaymentStatus = 'Paid'
WHERE PaymentStatus = 'Pending';

-- Modification 2: Delete all appointments that were 'Cancelled'
DELETE FROM Appointments
WHERE Status = 'Cancelled';

-- Modification 3: Insert prescriptions for patients who have a recent record using INSERT...SELECT
INSERT INTO Prescriptions (PatientID, RecordID, MedicationID, Diagnosis, MedicationName, Dosage, Duration)
SELECT 
    m.PatientID,
    m.RecordID,
    md.MedicationID,
    m.Diagnosis,
    md.MedicationName,
    '500mg',
    '5 days'
FROM MedicalRecords m
JOIN Medications md ON md.MedicationID IS NOT NULL
ORDER BY m.VisitDate DESC
LIMIT 10;
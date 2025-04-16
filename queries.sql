-- Query 1: Retrieve completed appointments with patient and doctor names
SELECT 
    p.FirstName AS PatientFirstName,
    p.LastName AS PatientLastName,
    d.FirstName AS DoctorFirstName,
    d.LastName AS DoctorLastName,
    a.AppointmentDate,
    a.Status
FROM Appointments a
JOIN Patients p ON a.PatientID = p.PatientID
JOIN Providers d ON a.ProviderID = d.ProviderID
WHERE a.Status = 'Completed'
ORDER BY a.AppointmentDate DESC
LIMIT 20;

-- Query 2: Count the number of appointments handled by each doctor
SELECT 
    pr.ProviderID,
    pr.FirstName,
    pr.LastName,
    COUNT(*) AS AppointmentCount
FROM Appointments a
JOIN Providers pr ON a.ProviderID = pr.ProviderID
GROUP BY a.ProviderID
ORDER BY AppointmentCount DESC;

-- Query 3: List patients who have spent more than $300 in total
SELECT 
    b.PatientID,
    CONCAT(p.FirstName, ' ', p.LastName) AS PatientName,
    SUM(b.TotalFee) AS TotalSpent
FROM Billing b
JOIN Patients p ON b.PatientID = p.PatientID
GROUP BY b.PatientID
HAVING SUM(b.TotalFee) > 300;

-- Query 4: Find patients who have at least one medical record
SELECT 
    PatientID, FirstName, LastName
FROM Patients p
WHERE EXISTS (
    SELECT 1
    FROM MedicalRecords m
    WHERE m.PatientID = p.PatientID
);

-- Query 5: List medications with low stock and upcoming expiration
SELECT 
    MedicationName, Manufacturer, Stock, ExpirationDate
FROM Medications
WHERE Stock < 100
  AND ExpirationDate < CURDATE() + INTERVAL 90 DAY;

-- Query 6: Count of waiting patients for each doctor (queue overview)
SELECT 
    pr.FirstName AS DoctorFirstName,
    pr.LastName AS DoctorLastName,
    COUNT(*) AS WaitingPatients
FROM QueueInfo q
JOIN Providers pr ON q.ProviderID = pr.ProviderID
WHERE q.QueueStatus = 'Waiting'
GROUP BY q.ProviderID
ORDER BY WaitingPatients DESC;
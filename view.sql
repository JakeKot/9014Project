-- View 1: Basic patient information view (updatable)
CREATE VIEW View_PatientBasic AS
SELECT PatientID, FirstName, LastName, Gender
FROM Patients;

-- This view is updatable because it selects from a single base table and does not use aggregation or joins.

-- View 2: Doctor schedule overview with appointment count (not updatable)
CREATE VIEW View_DoctorAppointments AS
SELECT 
    pr.ProviderID,
    pr.FirstName,
    pr.LastName,
    COUNT(a.AppointmentID) AS TotalAppointments
FROM Providers pr
JOIN Appointments a ON a.ProviderID = pr.ProviderID
GROUP BY pr.ProviderID;

-- This view is NOT updatable because it includes GROUP BY and an aggregate function (COUNT).

-- View 3: Medication summary for soon-to-expire and low-stock items (not updatable)
CREATE VIEW View_MedicationAlert AS
SELECT MedicationName, Stock, ExpirationDate
FROM Medications
WHERE Stock < 100 AND ExpirationDate < CURDATE() + INTERVAL 90 DAY;

-- This view is NOT updatable due to use of WHERE conditions and expressions on the base table.
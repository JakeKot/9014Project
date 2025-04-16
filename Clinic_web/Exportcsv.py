import pandas as pd
import mysql.connector

# Connect to your MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="9014-Project",  # ← Replace with your real password
    database="clinic_db"
)

# List of tables to export
tables = [
    'Patients',
    'Providers',
    'Medications',
    'Appointments',
    'MedicalRecords',
    'Prescriptions',
    'Billing',
    'QueueInfo'
]

# Export each table as CSV
for table in tables:
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    df.to_csv(f"{table}.csv", index=False)
    print(f"✅ Exported {table}.csv")

conn.close()
print("🎉 All tables exported to CSV successfully!")
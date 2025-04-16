from flask import Flask, render_template, request, redirect
import mysql.connector
from config import db_config  # Ensure config.py contains your db info

app = Flask(__name__)

# Connect to MySQL database
db = mysql.connector.connect(**db_config)
cursor = db.cursor(dictionary=True)

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Patient management page (view + add)
@app.route('/patients', methods=['GET', 'POST'])
def patients():
    if request.method == 'POST':
        # Form submitted: insert new patient
        first = request.form['first_name']
        last = request.form['last_name']
        dob = request.form['dob']
        gender = request.form['gender']
        contact = request.form['contact']
        insurance = request.form['insurance']
        cursor.execute("""
            INSERT INTO Patients (FirstName, LastName, DateOfBirth, Gender, ContactInfo, InsuranceNumber)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (first, last, dob, gender, contact, insurance))
        db.commit()
        return redirect('/patients')

    # GET method: show patient list
    cursor.execute("SELECT * FROM Patients")
    data = cursor.fetchall()
    return render_template('patients.html', patients=data)

@app.route('/doctors')
def doctors():
    cursor.execute("SELECT * FROM Providers")
    doctors_data = cursor.fetchall()
    return render_template('doctors.html', doctors=doctors_data)

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    # Dropdown data for patients and providers
    cursor.execute("SELECT PatientID, FirstName, LastName FROM Patients")
    patients = cursor.fetchall()
    cursor.execute("SELECT ProviderID, FirstName, LastName FROM Providers")
    providers = cursor.fetchall()

    if request.method == 'POST':
        pid = request.form['patient_id']
        prid = request.form['provider_id']
        date = request.form['appointment_date']
        slot = request.form['time_slot']
        symptom = request.form['symptom']
        status = request.form['status']
        notes = request.form['notes']
        cursor.execute("""
            INSERT INTO Appointments (PatientID, ProviderID, AppointmentDate, Symptom, TimeSlot, Status, Notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (pid, prid, date, symptom, slot, status, notes))
        db.commit()
        return redirect('/appointments')

    # Retrieve all appointments to display
    cursor.execute("""
        SELECT a.AppointmentID, a.AppointmentDate, a.TimeSlot, a.Status, a.Symptom, a.Notes,
               p.FirstName AS PatientFirstName, p.LastName AS PatientLastName,
               d.FirstName AS DoctorFirstName, d.LastName AS DoctorLastName
        FROM Appointments a
        JOIN Patients p ON a.PatientID = p.PatientID
        JOIN Providers d ON a.ProviderID = d.ProviderID
        ORDER BY a.AppointmentDate DESC
    """)
    appointments_data = cursor.fetchall()

    return render_template(
        'appointments.html',
        appointments=appointments_data,
        patients=patients,
        providers=providers
    )

from datetime import datetime, timedelta

@app.route('/medications')
def medications():
    # Query all medication records
    cursor.execute("""
        SELECT MedicationName, Manufacturer, Stock, ExpirationDate
        FROM Medications
        ORDER BY ExpirationDate ASC
    """)
    meds = cursor.fetchall()

    # Define a threshold date for "expiring soon" (within 90 days)
    soon_threshold = datetime.today().date() + timedelta(days=90)

    # Add a custom field 'IsWarning' to each row based on stock and expiration
    for med in meds:
        expiration = med['ExpirationDate']
        stock = med['Stock']
        med['IsWarning'] = (stock < 100 or expiration < soon_threshold)

    # Render the page with medication data
    return render_template('medications.html', medications=meds)

from datetime import datetime

# Route: Display all queue records
@app.route('/queue')
def queue():
    cursor.execute("""
        SELECT q.QueueID, q.QueueNumber, q.QueueStatus, q.QueueTime,
               p.FirstName AS PatientFirstName, p.LastName AS PatientLastName,
               d.FirstName AS DoctorFirstName, d.LastName AS DoctorLastName
        FROM QueueInfo q
        JOIN Patients p ON q.PatientID = p.PatientID
        JOIN Providers d ON q.ProviderID = d.ProviderID
        ORDER BY q.QueueTime ASC
    """)
    queue_data = cursor.fetchall()
    return render_template('queue.html', queue=queue_data)

# Route: Register a new patient in the queue
@app.route('/add-queue', methods=['GET', 'POST'])
def add_queue():
    cursor.execute("SELECT PatientID, FirstName, LastName FROM Patients")
    patients = cursor.fetchall()
    cursor.execute("SELECT ProviderID, FirstName, LastName FROM Providers")
    providers = cursor.fetchall()

    if request.method == 'POST':
        patient_id = request.form['patient_id']
        provider_id = request.form['provider_id']
        symptom = request.form['symptom']
        now = datetime.now()

        # Get the next queue number for this provider today
        cursor.execute("""
            SELECT MAX(QueueNumber) AS MaxQueue
            FROM QueueInfo
            WHERE DATE(QueueTime) = CURDATE() AND ProviderID = %s
        """, (provider_id,))
        result = cursor.fetchone()
        max_q = result['MaxQueue'] if result['MaxQueue'] else 0
        new_q_number = max_q + 1

        # Insert new queue record
        cursor.execute("""
            INSERT INTO QueueInfo (PatientID, ProviderID, QueueNumber, QueueStatus, QueueTime, Symptom)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (patient_id, provider_id, new_q_number, 'Waiting', now, symptom))
        db.commit()
        return redirect('/queue')

    return render_template('add_queue.html', patients=patients, providers=providers)

@app.route('/custom-query', methods=['GET', 'POST'])
def custom_query():
    results = []
    columns = []
    query = ''
    error = ''

    if request.method == 'POST':
        query = request.form['query']
        if query.strip().lower().startswith('select'):
            try:
                cursor.execute(query)
                results = cursor.fetchall()
                if results:
                    columns = results[0].keys()
            except Exception as e:
                error = str(e)
        else:
            error = 'Only SELECT statements are allowed.'

    return render_template('custom_query.html', query=query, results=results, columns=columns, error=error)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
# 9014Project
# Medical Management System (Flask + MySQL)

This is a web-based medical management system developed for ECE 9014 – Data Management and Applications. The system enables users to manage patients, doctors, appointments, medications, and queue information using a Python Flask frontend and a MySQL backend.

## 💡 Features

- ✅ Patient management (view, add)
- ✅ Doctor directory
- ✅ Appointment scheduling and viewing
- ✅ Medication inventory with stock and expiry alerts
- ✅ Queue management with live registration and tracking
- ✅ Custom SQL query interface for advanced users
- ✅ Pagination support for large datasets

## 🧱 Tech Stack

- **Backend**: Python 3 + Flask
- **Database**: MySQL
- **Frontend**: HTML (Jinja2 templates) + Bootstrap 5
- **Data Generator**: Python Faker (see `DataGen.py`)

## 📦 Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/clinic_web.git
cd clinic_web

2.	Install dependencies
pip install -r requirements.txt

3.	Set up the database

	•	Create a MySQL database named clinic_db
	•	Run your table creation script (or import provided schema)
	•	Update config.py with your MySQL username/password

# config.py
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '9014-Project',
    'database': 'clinic_db'
}

4.	Generate sample data
python DataGen.py

5.	Run the web app
python app.py
Visit: http://localhost:5000

📁 Project Structure
clinic_web/
├── app.py                # Main Flask app
├── config.py             # MySQL connection config
├── DataGen.py            # Sample data generator using Faker
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── patients.html
│   ├── doctors.html
│   ├── appointments.html
│   ├── medications.html
│   ├── queue.html
│   ├── add_queue.html
│   └── custom_query.html

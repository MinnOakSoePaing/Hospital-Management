import os
import csv
import json

def init_files():
    files = ['data/doctors.csv', 'data/patients.csv', 'data/appointments.csv']
    headers = [
        ['ID', 'Name', 'Specialty', 'Contact'],
        ['ID', 'Name', 'Age', 'Gender', 'Contact'],
        ['AppID', 'PatientID', 'DoctorID', 'Date', 'Time', 'Reason']
    ]

    os.makedirs('data', exist_ok=True)
    for file, header in zip(files, headers):
        if not os.path.exists(file):
            with open(file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)

    # Initialize user data if not exists
    user_file = 'data/users.json'
    if not os.path.exists(user_file):
        default_users = {
            "admin": {"password": "admin123", "role": "admin"},
            "dr.john": {"password": "doc123", "role": "doctor"},
            "patient1": {"password": "pat123", "role": "patient"}
        }
        with open(user_file, 'w') as f:
            json.dump(default_users, f, indent=4)

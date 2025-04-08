import tkinter as tk
from tkinter import ttk
import csv

class PatientDashboard:
    def __init__(self, master, patient_username):
        self.master = master
        self.patient_username = patient_username

        self.frame = ttk.Frame(master)
        self.frame.pack(expand=True, fill='both')

        ttk.Label(self.frame, text=f"Welcome, {patient_username}", font=('Helvetica', 16)).pack(pady=10)

        self.tree = ttk.Treeview(self.frame, columns=['AppID', 'DoctorID', 'Date', 'Time', 'Reason'], show='headings')
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
        self.tree.pack(expand=True, fill='both')

        self.load_appointments()

    def load_appointments(self):
        try:
            with open('data/appointments.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['PatientID'] == self.patient_username:
                        self.tree.insert('', 'end', values=(
                            row['AppID'],
                            row['DoctorID'],
                            row['Date'],
                            row['Time'],
                            row['Reason']
                        ))
        except FileNotFoundError:
            pass

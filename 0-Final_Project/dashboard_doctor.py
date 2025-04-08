import tkinter as tk
from tkinter import ttk
import csv

class DoctorDashboard:
    def __init__(self, master, doctor_username):
        self.master = master
        self.doctor_username = doctor_username

        self.frame = ttk.Frame(master)
        self.frame.pack(expand=True, fill='both')

        ttk.Label(self.frame, text=f"Welcome, Dr. {doctor_username}", font=('Helvetica', 16)).pack(pady=10)

        self.tree = ttk.Treeview(self.frame, columns=['AppID', 'PatientID', 'Date', 'Time', 'Reason'], show='headings')
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
        self.tree.pack(expand=True, fill='both')

        self.load_appointments()

    def load_appointments(self):
        try:
            with open('data/appointments.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['DoctorID'] == self.doctor_username:
                        self.tree.insert('', 'end', values=(
                            row['AppID'],
                            row['PatientID'],
                            row['Date'],
                            row['Time'],
                            row['Reason']
                        ))
        except FileNotFoundError:
            pass
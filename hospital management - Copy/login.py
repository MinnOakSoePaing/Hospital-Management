import tkinter as tk
from tkinter import ttk, messagebox
from dashboard_admin import AdminDashboard
from dashboard_doctor import DoctorDashboard
from dashboard_patient import PatientDashboard
import json

# Load user-role dictionary from external file
with open('data/users.json', 'r') as f:
    users = json.load(f)

class LoginScreen:
    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(master)
        self.frame.pack(pady=100)

        ttk.Label(self.frame, text="Username:").grid(row=0, column=0, pady=5)
        self.username = ttk.Entry(self.frame)
        self.username.grid(row=0, column=1)

        ttk.Label(self.frame, text="Password:").grid(row=1, column=0, pady=5)
        self.password = ttk.Entry(self.frame, show='*')
        self.password.grid(row=1, column=1)

        ttk.Button(self.frame, text="Login", command=self.login).grid(row=2, columnspan=2, pady=10)

    def login(self):
        user = self.username.get()
        pwd = self.password.get()

        if user in users and users[user]["password"] == pwd:
            role = users[user]["role"]
            self.frame.destroy()
            if role == 'admin':
                AdminDashboard(self.master)
            elif role == 'doctor':
                DoctorDashboard(self.master, user)
            elif role == 'patient':
                PatientDashboard(self.master, user)
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")
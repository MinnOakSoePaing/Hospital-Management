import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

class DoctorDashboard:
    def __init__(self, master, doctor_username):
        self.master = master
        self.doctor_username = doctor_username

        self.frame = ttk.Notebook(master)
        self.frame.pack(expand=True, fill='both')

        self.appointment_tab = ttk.Frame(self.frame)
        self.patient_tab = ttk.Frame(self.frame)

        self.frame.add(self.appointment_tab, text="Appointments")
        self.frame.add(self.patient_tab, text="Patients")

        self.build_appointments_tab()
        self.build_patients_tab()

    # ---------------- Appointments Tab -------------------
    def build_appointments_tab(self):
        ttk.Label(self.appointment_tab, text=f"Dr. {self.doctor_username} - Appointments", font=('Helvetica', 14)).pack(pady=5)

        self.app_tree = ttk.Treeview(self.appointment_tab, columns=['AppID', 'PatientID', 'Date', 'Time', 'Reason'], show='headings')
        for col in self.app_tree['columns']:
            self.app_tree.heading(col, text=col)
        self.app_tree.pack(fill='both', expand=True)

        # Entry Fields
        entry_frame = ttk.Frame(self.appointment_tab)
        entry_frame.pack(pady=5)
        self.app_entries = {}
        for i, col in enumerate(self.app_tree['columns']):
            ttk.Label(entry_frame, text=col).grid(row=0, column=i)
            ent = ttk.Entry(entry_frame)
            ent.grid(row=1, column=i)
            self.app_entries[col] = ent

        # Buttons
        ttk.Button(entry_frame, text="Add", command=self.add_appointment).grid(row=2, column=0, pady=5)
        ttk.Button(entry_frame, text="Update", command=self.update_appointment).grid(row=2, column=1)
        ttk.Button(entry_frame, text="Delete", command=self.delete_appointment).grid(row=2, column=2)

        self.app_tree.bind('<<TreeviewSelect>>', self.fill_appointment_fields)

        self.load_appointments()

    def load_appointments(self):
        self.app_tree.delete(*self.app_tree.get_children())
        if os.path.exists('data/appointments.csv'):
            with open('data/appointments.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['DoctorID'] == self.doctor_username:
                        self.app_tree.insert('', 'end', values=(row['AppID'], row['PatientID'], row['Date'], row['Time'], row['Reason']))

    def add_appointment(self):
        values = [self.app_entries[col].get() for col in self.app_tree['columns']]
        if any(not v for v in values):
            messagebox.showwarning("Validation", "All fields required.")
            return
        with open('data/appointments.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([*values[:2], self.doctor_username, *values[2:]])
        self.load_appointments()
        self.clear_entries(self.app_entries)

    def update_appointment(self):
        selected = self.app_tree.selection()
        if not selected:
            return
        values = [self.app_entries[col].get() for col in self.app_tree['columns']]
        all_rows = []
        with open('data/appointments.csv', 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                if row[0] == values[0] and row[2] == self.doctor_username:
                    all_rows.append([*values[:2], self.doctor_username, *values[2:]])
                else:
                    all_rows.append(row)
        with open('data/appointments.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(all_rows)
        self.load_appointments()
        self.clear_entries(self.app_entries)

    def delete_appointment(self):
        selected = self.app_tree.selection()
        if not selected:
            return
        item = self.app_tree.item(selected[0])['values']
        app_id = item[0]
        new_rows = []
        with open('data/appointments.csv', 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                if not (row[0] == app_id and row[2] == self.doctor_username):
                    new_rows.append(row)
        with open('data/appointments.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(new_rows)
        self.load_appointments()

    def fill_appointment_fields(self, event):
        selected = self.app_tree.selection()
        if selected:
            values = self.app_tree.item(selected[0], 'values')
            for i, col in enumerate(self.app_tree['columns']):
                self.app_entries[col].delete(0, 'end')
                self.app_entries[col].insert(0, values[i])

    # ---------------- Patients Tab -------------------
    def build_patients_tab(self):
        ttk.Label(self.patient_tab, text="Manage Patient Info", font=('Helvetica', 14)).pack(pady=5)

        # Search bar
        search_frame = ttk.Frame(self.patient_tab)
        search_frame.pack(pady=5)

        ttk.Label(search_frame, text="Search:").pack(side='left')
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side='left')
        search_entry.bind('<Return>', lambda e: self.load_patients())

        # Treeview
        self.patient_tree = ttk.Treeview(self.patient_tab, columns=['ID', 'Name', 'Age', 'Gender', 'Contact'], show='headings')
        for col in self.patient_tree['columns']:
            self.patient_tree.heading(col, text=col)
        self.patient_tree.pack(fill='both', expand=True)

        # Entry form
        entry_frame = ttk.Frame(self.patient_tab)
        entry_frame.pack(pady=5)
        self.patient_entries = {}
        for i, col in enumerate(self.patient_tree['columns']):
            ttk.Label(entry_frame, text=col).grid(row=0, column=i)
            ent = ttk.Entry(entry_frame)
            ent.grid(row=1, column=i)
            self.patient_entries[col] = ent

        # Buttons
        ttk.Button(entry_frame, text="Add Patient", command=self.add_patient).grid(row=2, column=0, pady=5)
        ttk.Button(entry_frame, text="Update Patient", command=self.update_patient).grid(row=2, column=1)

        self.patient_tree.bind('<<TreeviewSelect>>', self.fill_patient_fields)

        self.load_patients()

    def load_patients(self):
        self.patient_tree.delete(*self.patient_tree.get_children())
        patient_ids = {self.app_tree.item(child)['values'][1] for child in self.app_tree.get_children()}

        keyword = self.search_var.get().lower().strip()

        if os.path.exists('data/patients.csv'):
            with open('data/patients.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if (not keyword or keyword in row['Name'].lower() or keyword in row['ID'].lower()):
                        if row['ID'] in patient_ids or not patient_ids:
                            self.patient_tree.insert('', 'end', values=(row['ID'], row['Name'], row['Age'], row['Gender'], row['Contact']))

    def add_patient(self):
        values = [self.patient_entries[col].get() for col in self.patient_tree['columns']]
        if any(not val for val in values):
            messagebox.showwarning("Validation", "All fields required.")
            return

        if os.path.exists('data/patients.csv'):
            with open('data/patients.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['ID'] == values[0]:
                        messagebox.showerror("Duplicate", "Patient ID already exists.")
                        return

        with open('data/patients.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            if os.stat('data/patients.csv').st_size == 0:
                writer.writerow(self.patient_tree['columns'])  # write header if empty
            writer.writerow(values)
        self.load_patients()
        self.clear_entries(self.patient_entries)

    def update_patient(self):
        selected = self.patient_tree.selection()
        if not selected:
            return
        values = [self.patient_entries[col].get() for col in self.patient_tree['columns']]
        all_rows = []
        with open('data/patients.csv', 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                if row[0] == values[0]:
                    all_rows.append(values)
                else:
                    all_rows.append(row)
        with open('data/patients.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(all_rows)
        self.load_patients()
        self.clear_entries(self.patient_entries)

    def fill_patient_fields(self, event):
        selected = self.patient_tree.selection()
        if selected:
            values = self.patient_tree.item(selected[0], 'values')
            for i, col in enumerate(self.patient_tree['columns']):
                self.patient_entries[col].delete(0, 'end')
                self.patient_entries[col].insert(0, values[i])

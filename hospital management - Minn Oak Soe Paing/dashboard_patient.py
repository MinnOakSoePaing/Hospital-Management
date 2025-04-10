import tkinter as tk
from tkinter import ttk, messagebox
import csv

class PatientDashboard:
    def __init__(self, master, patient_username, logout_callback=None):
        self.master = master
        self.patient_username = patient_username
        self.logout_callback = logout_callback

        # Create the main frame
        self.frame = ttk.Frame(master)
        self.frame.pack(expand=True, fill='both')

        # Top bar with welcome and logout
        top = ttk.Frame(self.frame)
        top.pack(fill='x', pady=5)
        ttk.Label(top, text=f"Welcome, {patient_username}", font=('Helvetica', 14)).pack(side='left', padx=10)
        ttk.Button(top, text="Logout", command=self.logout).pack(side='right', padx=10)

        # Tabbed interface
        self.tabs = ttk.Notebook(self.frame)
        self.tabs.pack(expand=True, fill='both')

        # Appointment Tab
        self.appointment_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.appointment_tab, text='Appointments')

        # Doctor Tab
        self.doctor_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.doctor_tab, text='Doctors')

        # Appointment TreeView
        self.tree = ttk.Treeview(self.appointment_tab, columns=['AppID','PatientID', 'DoctorID', 'Date', 'Time', 'Reason'], show='headings')
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
        self.tree.pack(expand=True, fill='both')
        self.tree.bind('<<TreeviewSelect>>', self.populate_fields)

        # Entry Form for Appointments
        self.entries = {}
        entry_frame = ttk.Frame(self.appointment_tab)
        entry_frame.pack(pady=10)

        for i, col in enumerate(self.tree['columns']):
            ttk.Label(entry_frame, text=col).grid(row=0, column=i)
            ent = ttk.Entry(entry_frame)
            ent.grid(row=1, column=i)
            self.entries[col] = ent

        # Appointment buttons
        ttk.Button(entry_frame, text='Add', command=self.add_appointment).grid(row=2, column=0, pady=5)
        ttk.Button(entry_frame, text='Update', command=self.update_appointment).grid(row=2, column=1)
        ttk.Button(entry_frame, text='Delete', command=self.delete_appointment).grid(row=2, column=2)

        # Load appointments
        self.load_appointments()

        # Load doctors into the doctor tab
        self.load_doctors()

    def logout(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        if self.logout_callback:
            self.logout_callback()


    def load_appointments(self):
        try:
            with open('data/appointments.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['PatientID'] :
                        self.tree.insert('', 'end', values=(
                            row['AppID'],
                            row['PatientID'],
                            row['DoctorID'],
                            row['Date'],
                            row['Time'],
                            row['Reason']
                        ))
        except FileNotFoundError:
            pass

    def add_appointment(self):
        new_values = [self.entries[col].get() for col in self.tree['columns']]
        if any(not val for val in new_values):
            messagebox.showwarning("Validation", "All fields required.")
            return
        with open('data/appointments.csv', 'a', newline='') as f:
            csv.writer(f).writerow(new_values)
        self.tree.insert('', 'end', values=new_values)
        self.clear_entries()

    def update_appointment(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Update", "Please select an appointment to update.")
            return
        new_values = [self.entries[col].get() for col in self.tree['columns']]
        if any(not val for val in new_values):
            messagebox.showwarning("Validation", "All fields required.")
            return
        self.tree.item(selected, values=new_values)
        self.update_csv()
        self.clear_entries()

    def delete_appointment(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Delete", "Please select an appointment to delete.")
            return
        self.tree.delete(selected)
        self.update_csv()

    def populate_fields(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], 'values')
            for i, val in enumerate(values):
                self.entries[self.tree['columns'][i]].delete(0, 'end')
                self.entries[self.tree['columns'][i]].insert(0, val)

    def clear_entries(self):
        for entry in self.entries.values():
            entry.delete(0, 'end')

    def update_csv(self):
        rows = [self.tree.item(child)['values'] for child in self.tree.get_children()]
        with open('data/appointments.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.tree['columns'])  # Write header
            writer.writerows(rows)

    def load_doctors(self):
        doctor_tree = ttk.Treeview(self.doctor_tab, columns=['DoctorID', 'Name', 'Specialty', 'Contact'], show='headings')
        for col in doctor_tree['columns']:
            doctor_tree.heading(col, text=col)
        doctor_tree.pack(expand=True, fill='both')

        try:
            with open('data/doctors.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    doctor_tree.insert('', 'end', values=(
                        row['ID'],
                        row['Name'],
                        row['Specialty'],
                        row['Contact']
                    ))
        except FileNotFoundError:
            messagebox.showwarning("File Not Found", "Doctor data not found.")

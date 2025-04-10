import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

class DoctorDashboard:
    def __init__(self, master, doctor_username, logout_callback=None):
        self.master = master
        self.doctor_username = doctor_username
        self.logout_callback = logout_callback
        
        # Frame setup
        self.frame = ttk.Frame(master)
        self.frame.pack(expand=True, fill='both')

        # Top bar
        top = ttk.Frame(self.frame)
        top.pack(fill='x', pady=5)
        ttk.Label(top, text=f"Welcome, Dr. {doctor_username}", font=('Helvetica', 14)).pack(side='left', padx=10)
        # tk.Label(top, text=f"Welcome, Dr. {doctor_username}", font=('Helvetica', 14), relief='ridge').pack(side='left', padx=10)
        tk.Button(top, text="Logout", command=self.logout, bg='red', fg='white', relief='raised').pack(side='right', padx=10)

        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(expand=True, fill='both')

        self.patients_tab = ttk.Frame(self.notebook)
        self.appointments_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.patients_tab, text="Patients")
        self.notebook.add(self.appointments_tab, text="Appointments")

        # Corrected method names
        self.build_patient_tab()  # Should match the method name
        self.build_appointment_tab()

    def logout(self):
        # Clear the current window content
        for widget in self.master.winfo_children():
            widget.destroy()

        # Call the logout callback function, if provided
        if self.logout_callback:
            self.logout_callback()

    def build_patient_tab(self):
        self.patient_tree = self.create_tree(self.patients_tab, ['ID', 'Name', 'Age', 'Gender', 'Contact'])
        self.create_crud_controls(self.patients_tab, self.patient_tree, 'data/patients.csv')

    def build_appointment_tab(self):
        self.appointment_tree = self.create_tree(self.appointments_tab, ['AppID', 'PatientID', 'DoctorID', 'Date', 'Time', 'Reason'])
        self.create_crud_controls(self.appointments_tab, self.appointment_tree, 'data/appointments.csv')

    def create_tree(self, parent, columns):
        tree = ttk.Treeview(parent, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
        tree.pack(fill='both', expand=True)
        return tree

    def create_crud_controls(self, parent, tree, filepath):
        entry_frame = ttk.Frame(parent)
        entry_frame.pack()

        entries = []
        for i, col in enumerate(tree['columns']):
            ttk.Label(entry_frame, text=col).grid(row=0, column=i)
            ent = ttk.Entry(entry_frame)
            ent.grid(row=1, column=i)
            entries.append(ent)

        def clear_entries():
            for e in entries:
                e.delete(0, 'end')

        def add_record():
            record = [e.get() for e in entries]
            if any(not val for val in record):
                messagebox.showwarning("Validation", "All fields required.")
                return
            with open(filepath, 'a', newline='') as f:
                csv.writer(f).writerow(record)
            tree.insert('', 'end', values=record)
            clear_entries()

        def delete_record():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Delete", "Please select a record to delete.")
                return
            tree.delete(selected)
            update_csv()

        def update_record():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Update", "Please select a record to update.")
                return
            new_values = [e.get() for e in entries]
            if any(not val for val in new_values):
                messagebox.showwarning("Validation", "All fields required.")
                return
            tree.item(selected, values=new_values)
            update_csv()
            clear_entries()

        def populate_fields(event):
            selected = tree.selection()
            if selected:
                values = tree.item(selected[0], 'values')
                for i, val in enumerate(values):
                    entries[i].delete(0, 'end')
                    entries[i].insert(0, val)

        def update_csv():
            rows = [tree.item(child)['values'] for child in tree.get_children()]
            with open(filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(tree['columns'])  # Write header
                writer.writerows(rows)

        ttk.Button(entry_frame, text='Add', command=add_record).grid(row=2, column=0, pady=5)
        ttk.Button(entry_frame, text='Update', command=update_record).grid(row=2, column=1, pady=5)
        ttk.Button(entry_frame, text='Delete', command=delete_record).grid(row=2, column=2, pady=5)

        tree.bind('<<TreeviewSelect>>', populate_fields)

        # Load existing records
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    tree.insert('', 'end', values=row)

        return tree





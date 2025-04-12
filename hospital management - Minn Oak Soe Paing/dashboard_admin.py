import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

class AdminDashboard:
    def __init__(self, master, logout_callback=None):
        self.master = master
        self.logout_callback = logout_callback

        self.add_profile_button()  # Add the profile button instead of logout button

        self.frame = ttk.Notebook(master)
        self.frame.pack(expand=1, fill='both')

        self.doctor_tab = ttk.Frame(self.frame)
        self.patient_tab = ttk.Frame(self.frame)
        self.appointment_tab = ttk.Frame(self.frame)

        self.frame.add(self.doctor_tab, text='Doctors')
        self.frame.add(self.patient_tab, text='Patients')
        self.frame.add(self.appointment_tab, text='Appointments')

        self.build_doctor_tab()
        self.build_patient_tab()
        self.build_appointment_tab()

    def add_profile_button(self):
        top = ttk.Frame(self.master)
        top.pack(fill='x', pady=5)

        ttk.Label(top, text="Welcome, Admin", font=('Helvetica', 14)).pack(side='left', padx=10, pady=5)

        style = ttk.Style()
        style.configure('TButton', bg='blue', fg='white', relief='raised',padding=(10, 5), font=('Helvetica', 12))
        # Profile Button 
        self.profile_btn = ttk.Button(top,text="Profile",style='TButton', command=self.show_profile_popup, compound='left')
        self.profile_btn.pack(side='right', padx=10)

        

    def show_profile_popup(self):
        # Create a new Toplevel window for profile info
        profile_popup = tk.Toplevel(self.master)
        profile_popup.title("Profile Information")
        profile_popup.geometry("300x200")
        # Get the position of the profile button
        x = self.master.winfo_rootx() + self.profile_btn.winfo_x()
        y = self.master.winfo_rooty() + self.profile_btn.winfo_y()
        offset_x = 300
        x = x - offset_x

        # Set the popup's geometry near the button
        profile_popup.geometry(f"300x200+{x}+{y}")

        # User Profile Info
        username = "Admin"  # Replace with dynamic user variable
        role = "Admin"  # Replace with dynamic role variable

        ttk.Label(profile_popup, text=f"Username: {username}", font=('Helvetica', 12)).pack(pady=10)
        ttk.Label(profile_popup, text=f"Role: {role}", font=('Helvetica', 12)).pack(pady=5)

        # Logout Button inside profile popup
        logout_btn = ttk.Button(profile_popup, text="Logout", command=self.logout)
        logout_btn.pack(pady=10)

    def logout(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        if self.logout_callback:
            self.logout_callback()

    def build_doctor_tab(self):
        self.doctor_tree = self.create_tree(self.doctor_tab, ['ID', 'Name', 'Specialty', 'Contact'])
        self.create_crud_controls(self.doctor_tab, self.doctor_tree, 'data/doctors.csv')

    def build_patient_tab(self):
        self.patient_tree = self.create_tree(self.patient_tab, ['ID', 'Name', 'Age', 'Gender', 'Contact'])
        self.create_crud_controls(self.patient_tab, self.patient_tree, 'data/patients.csv')

    def build_appointment_tab(self):
        self.appointment_tree = self.create_tree(self.appointment_tab, ['AppID', 'PatientID', 'DoctorID', 'Date', 'Time', 'Reason'])
        self.create_crud_controls(self.appointment_tab, self.appointment_tree, 'data/appointments.csv')

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
        
        style = ttk.Style()
        style.configure('TButton', bg='blue', fg='white', relief='raised',padding=(10, 5), font=('Helvetica', 12))

        ttk.Button(entry_frame, text='Add', style='TButton', command=add_record).grid(row=2, column=0, pady=5)
        ttk.Button(entry_frame, text='Update', style='TButton', command=update_record).grid(row=2, column=1, pady=5)
        ttk.Button(entry_frame, text='Delete', style='TButton', command=delete_record).grid(row=2, column=2, pady=5)

        tree.bind('<<TreeviewSelect>>', populate_fields)

        # Load existing records
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    tree.insert('', 'end', values=row)

        return tree

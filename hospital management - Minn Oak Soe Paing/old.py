import tkinter as tk
# from tkinter import ttk, messagebox
# import csv
# import os

# class DoctorDashboard:
#     def __init__(self, master, doctor_username, logout_callback):
#         self.master = master
#         self.doctor_username = doctor_username
#         self.logout_callback = logout_callback

#         self.frame = ttk.Frame(master)
#         self.frame.pack(expand=True, fill='both')

#         # Top bar
#         top = ttk.Frame(self.frame)
#         top.pack(fill='x', pady=5)
#         ttk.Label(top, text=f"Welcome, Dr. {doctor_username}", font=('Helvetica', 14)).pack(side='left', padx=10)
#         ttk.Button(top, text="Logout", command=self.logout).pack(side='right', padx=10)

#         # Notebook tabs
#         self.notebook = ttk.Notebook(self.frame)
#         self.notebook.pack(expand=True, fill='both')

#         self.patients_tab = ttk.Frame(self.notebook)
#         self.appointments_tab = ttk.Frame(self.notebook)

#         self.notebook.add(self.patients_tab, text="Patients")
#         self.notebook.add(self.appointments_tab, text="Appointments")

#         self.build_patients_tab()
#         self.build_appointments_tab()

#     def logout(self):
#         for widget in self.master.winfo_children():
#             widget.destroy()
#         self.logout_callback()

#     def build_patients_tab(self):
#         columns = ['ID', 'Name', 'Age', 'Gender', 'Contact']
#         self.patient_tree = ttk.Treeview(self.patients_tab, columns=columns, show='headings')
#         for col in columns:
#             self.patient_tree.heading(col, text=col)
#         self.patient_tree.pack(fill='both', expand=True)

#         self.patient_entries = []
#         entry_frame = ttk.Frame(self.patients_tab)
#         entry_frame.pack(pady=5)
#         for i, col in enumerate(columns):
#             ttk.Label(entry_frame, text=col).grid(row=0, column=i)
#             ent = ttk.Entry(entry_frame)
#             ent.grid(row=1, column=i)
#             self.patient_entries.append(ent)

#         def add_patient():
#             record = [e.get() for e in self.patient_entries]
#             if any(not val for val in record):
#                 messagebox.showwarning("Validation", "All fields are required.")
#                 return
#             with open('data/patients.csv', 'a', newline='') as f:
#                 csv.writer(f).writerow(record)
#             self.patient_tree.insert('', 'end', values=record)
#             for e in self.patient_entries:
#                 e.delete(0, 'end')

#         ttk.Button(entry_frame, text='Add Patient', command=add_patient).grid(row=2, column=0, columnspan=2, pady=5)

#         # Load existing patients
#         if os.path.exists('data/patients.csv'):
#             with open('data/patients.csv', 'r') as f:
#                 reader = csv.reader(f)
#                 for row in reader:
#                     if row:
#                         self.patient_tree.insert('', 'end', values=row)

#     def save_appointments_to_csv(self):
#         if not os.path.exists('data/appointments.csv'):
#             return
#         updated_rows = []
#         for item in self.appointment_tree.get_children():
#             values = self.appointment_tree.item(item)['values']
#             updated_rows.append({
#                 'AppID': values[0],
#                 'DoctorID': self.doctor_username,
#                 'PatientID': values[1],
#                 'Date': values[2],
#                 'Time': values[3],
#                 'Reason': values[4]
#             })

#         with open('data/appointments.csv', 'w', newline='') as f:
#             writer = csv.DictWriter(f, fieldnames=['AppID', 'DoctorID', 'PatientID', 'Date', 'Time', 'Reason'])
#             writer.writeheader()
#             writer.writerows(updated_rows)

#     def build_appointments_tab(self):
#         columns = ['AppID', 'PatientID', 'Date', 'Time', 'Reason']
#         self.appointment_tree = ttk.Treeview(self.appointments_tab, columns=columns, show='headings')
#         for col in columns:
#             self.appointment_tree.heading(col, text=col)
#         self.appointment_tree.pack(fill='both', expand=True)

#         self.appointment_entries = []
#         entry_frame = ttk.Frame(self.appointments_tab)
#         entry_frame.pack(pady=5)
#         for i, col in enumerate(columns):
#             ttk.Label(entry_frame, text=col).grid(row=0, column=i)
#             ent = ttk.Entry(entry_frame)
#             ent.grid(row=1, column=i)
#             self.appointment_entries.append(ent)

#         def update_appointment():
#             selected = self.appointment_tree.selection()
#             if not selected:
#                 messagebox.showwarning("Update", "Please select an appointment to update.")
#                 return
#             new_values = [entry.get() for entry in self.appointment_entries]
#             if any(not val for val in new_values):
#                 messagebox.showwarning("Validation", "All fields are required.")
#                 return
#             self.appointment_tree.item(selected, values=new_values)
#             self.save_appointments_to_csv()

#         def delete_appointment():
#             selected = self.appointment_tree.selection()
#             if not selected:
#                 messagebox.showwarning("Delete", "Please select an appointment to delete.")
#                 return
#             self.appointment_tree.delete(selected)
#             self.save_appointments_to_csv()  # Save the changes to CSV

#         ttk.Button(entry_frame, text='Update Appointment', command=update_appointment).grid(row=2, column=0, pady=5)
#         ttk.Button(entry_frame, text='Delete Appointment', command=delete_appointment).grid(row=2, column=1, pady=5)

#         # Load appointments
#         if os.path.exists('data/appointments.csv'):
#             with open('data/appointments.csv', 'r') as f:
#                 reader = csv.DictReader(f)
#                 for row in reader:
#                     if row['DoctorID']:
#                         self.appointment_tree.insert('', 'end', values=[
#                             row['AppID'],
#                             row['PatientID'],
#                             row['Date'],
#                             row['Time'],
#                             row['Reason']
#                         ])
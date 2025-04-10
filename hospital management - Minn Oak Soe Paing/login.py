import tkinter as tk
from tkinter import ttk, messagebox
from dashboard_admin import AdminDashboard
from dashboard_doctor import DoctorDashboard
from dashboard_patient import PatientDashboard
import json
from dashboard_doctor import DoctorDashboard


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
        ttk.Button(self.frame, text="Register", command=self.register_screen).grid(row=3, columnspan=2, pady=10)

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


  # Create a new window for registration UI
    def register_screen(self):
      
        self.register_window = tk.Toplevel(self.master)
        self.register_window.title("Register")

        ttk.Label(self.register_window, text="Username:").grid(row=0, column=0, pady=5)
        self.register_username = ttk.Entry(self.register_window)
        self.register_username.grid(row=0, column=1)

        ttk.Label(self.register_window, text="Password:").grid(row=1, column=0, pady=5)
        self.register_password = ttk.Entry(self.register_window, show='*')
        self.register_password.grid(row=1, column=1)

        ttk.Label(self.register_window, text="Role:").grid(row=2, column=0, pady=5)
        self.register_role = ttk.Combobox(self.register_window, values=["admin", "doctor", "patient"])
        self.register_role.grid(row=2, column=1)
        self.register_role.set("doctor")  # Default role set to doctor

        ttk.Button(self.register_window, text="Register", command=self.register).grid(row=3, columnspan=2, pady=10)

# Register Function
    def register(self):
        # Get the user inputs
        username = self.register_username.get()
        password = self.register_password.get()
        role = self.register_role.get()

        # Check if the username already exists
        if username in users:
            messagebox.showerror("Registration Failed", "Username already exists.")
            return

        # Validate inputs
        if not username or not password or not role:
            messagebox.showerror("Registration Failed", "All fields are required.")
            return

        # Add new user to the users dictionary
        users[username] = {
            "password": password,
            "role": role
        }

        # Save the updated users data to the users.json file
        with open('data/users.json', 'w') as f:
            json.dump(users, f, indent=4)

        messagebox.showinfo("Registration Successful", f"Account created successfully for {role}!")
        self.register_window.destroy()

        # Optionally, you can auto-login after registration
        self.username.delete(0, 'end')
        self.password.delete(0, 'end')
        self.username.insert(0, username)
        self.password.insert(0, password)
    
    def login(self):
        user = self.username.get()
        pwd = self.password.get()

        if user in users and users[user]["password"] == pwd:
            role = users[user]["role"]
            self.frame.destroy()
        
        if role == 'admin':
            AdminDashboard(self.master, logout_callback=self.on_logout)
        elif role == 'doctor':
            # Fix the logout_callback issue
            DoctorDashboard(self.master, user, logout_callback=self.on_logout)
        elif role == 'patient':
            PatientDashboard(self.master, user, logout_callback=self.on_logout)

# Callback method to handle the logout and navigate to the login screen
    def on_logout(self):
    # Code to navigate to the login screen or perform any other logout logic
        self.frame.destroy()  # Close the current dashboard frame
        LoginScreen(self.master)  # Open the login screen again

import tkinter as tk
from PIL import Image, ImageTk  
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
        self.master.title("Hospital Management System")
        self.master.configure(bg='white')

        self.frame = tk.Frame(master, bg='white')
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # === LEFT: Image Frame ===
        img = Image.open("img/login.png")
        img = img.resize((500, 500))
        self.logo = ImageTk.PhotoImage(img)

        self.left_frame = tk.Frame(self.frame, bg='white')
        self.left_frame.grid(row=0, column=0)

        tk.Label(self.left_frame, image=self.logo, bg='white').pack()

        # === RIGHT: Login Form ===
        self.right_frame = tk.Frame(self.frame, bg='white')
        self.right_frame.grid(row=0, column=1, padx=80)

        # Sign in title
        tk.Label(self.right_frame, text="Sign in", font=('Arial', 30, 'bold'), bg='white', fg='#007BFF').grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Username
        tk.Label(self.right_frame, text="Username",fg="gray", bg="white",font=('Helvetica', 11)).grid(row=1, column=0, sticky="w", columnspan=2)
        self.username = tk.Entry(self.right_frame,width=35, bd=0, bg='white', highlightthickness=0, font=('Arial', 11)) # Entry widget for userdata pass
        self.username.grid(row=2, column=0, columnspan=2, sticky="ew", padx=0, pady=10) 
        underline1 = tk.Frame(self.right_frame, height=1, bg="black")
        underline1.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        # Password
        tk.Label(self.right_frame, text="Password",fg="gray", bg="white",font=('Helvetica', 11)).grid(row=4, column=0, sticky="w", columnspan=2)
        self.password = tk.Entry(self.right_frame,width=35, show='*', bd=0, bg='white', highlightthickness=0, font=('Arial', 11)) # Entry widget for password pass
        self.password.grid(row=5, column=0, columnspan=2, sticky="ew", padx=0, pady=10)
        underline2 = tk.Frame(self.right_frame, height=1, bg="black")
        underline2.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(0, 20))

        # Login Button (Centered)
        login_btn = tk.Button(self.right_frame,
        text="Login",
        command=self.login,
        font=('Helvetica', 11, 'bold'),
        bg='#007BFF',        # Button background
        fg='white',          # Text color
        activebackground='#2196F3',
        activeforeground='white',  # On click bg
        padx=10,
        pady=8,
        bd=0,                # No border
        relief="flat"
        )
        login_btn.grid(row=7, column=0, columnspan=2, pady=(0, 20), sticky="ew")

        # Register link
        tk.Label(self.right_frame, text="Don't have an account?", font=('Helvetica', 10), bg='white').grid(row=8, column=0, sticky='e')
        register_btn = tk.Button(self.right_frame,
        text="Sign up",
        command=self.register_screen,
        font=('Helvetica', 10, 'bold'),
        border=0,
        fg='#007BFF',
        activebackground='white',
        activeforeground='#2196F3',
        bg='white',
        relief="flat"
        )
        register_btn.grid(row=8, column=1, sticky='w')
        

    # def login(self):
    #     user = self.username.get()
    #     pwd = self.password.get()
        
    #     # self.icon_image = tk.PhotoImage(file="img/login.png")
    #     # self.master.iconphoto(False, self.icon_image)

    #     if user in users and users[user]["password"] == pwd:
    #         role = users[user]["role"]
    #         self.frame.destroy()

    #         if role == 'admin':
    #             AdminDashboard(self.master)
    #         elif role == 'doctor':
    #             DoctorDashboard(self.master, user)
    #         elif role == 'patient':
    #             PatientDashboard(self.master, user)
    #     else:
    #         messagebox.showerror("Login Failed", "Incorrect username or password.")


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
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")

# Callback method to handle the logout and navigate to the login screen
    def on_logout(self):
    # Code to navigate to the login screen or perform any other logout logic
        self.frame.destroy()  # Close the current dashboard frame
        LoginScreen(self.master)  # Open the login screen again

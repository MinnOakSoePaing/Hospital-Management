import tkinter as tk
from login import LoginScreen
from utils import init_files

def main():
    init_files()  # Ensure CSVs exist
    root = tk.Tk()
    root.title("Hospital Management System")
    root.state('zoomed')
    app = LoginScreen(root)
    root.mainloop()

if __name__ == '__main__':
    main()
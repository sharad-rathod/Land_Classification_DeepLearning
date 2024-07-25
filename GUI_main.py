import tkinter as tk
from tkinter import messagebox
import sqlite3
from subprocess import call
import tkinter as tk

from PIL import Image, ImageTk
from tkinter import ttk
from tkvideo import tkvideo


class GUI:
    def __init__(self, master):
        self.master = master
        master.title("GUI")

        w, h = master.winfo_screenwidth(), master.winfo_screenheight()
        master.geometry("%dx%d+0+0" % (w, h))

        self.video_label = tk.Label(master)
        self.video_label.pack()
        # Assuming you have a video named "plant.mp4" in the current directory
        # Commented out for demonstration purposes as tkvideo may not be installed
        self.player = tkvideo("plant.mp4", self.video_label, loop=1, size=(w, h))
        self.player.play()

        lbl = tk.Label(master, text="Land Classification on Satellite Images", font=('times', 35, 'bold'), height=1, width=32, bg="black", fg="white")
        lbl.place(x=300, y=10)

        button2 = tk.Button(master, foreground="white", background="black", font=("Tempus Sans ITC", 14, "bold"),
                            text="Login", command=self.log, width=15, height=2)
        button2.place(x=5, y=90)

        button3 = tk.Button(master, foreground="white", background="black", font=("Tempus Sans ITC", 14, "bold"),
                            text="Registration", command=self.reg, width=15, height=2)
        button3.place(x=5, y=170)

        forget_btn = tk.Button(master, text="Forgot Password", command=self.forget_password, width=15, height=2, font=('times', 15, 'bold'), bg="blue", fg="white")
        forget_btn.place(x=5, y=250)

        exit_btn = tk.Button(master, text="Exit", command=self.window, width=15, height=2, font=('times', 15, 'bold'), bg="red", fg="white")
        exit_btn.place(x=5, y=330)

        # Dictionary to store user credentials
        # Commented out for demonstration purposes
        # self.user_credentials = {}

    def log(self):
        from subprocess import call
        call(["python", "login.py"])

    def reg(self):
        from subprocess import call
        call(["python", "registration.py"])

    def window(self):
        self.master.destroy()

    def forget_password(self):
        self.forget_password_window = tk.Toplevel(self.master)
        self.forget_password_window.title("Forget Password")

        tk.Label(self.forget_password_window, text="Enter Mobile Number or Email ID:").pack()
        self.email_or_mobile_entry = tk.Entry(self.forget_password_window)
        self.email_or_mobile_entry.pack()

        tk.Label(self.forget_password_window, text="Enter New Password:").pack()
        self.new_password_entry = tk.Entry(self.forget_password_window, show="*")
        self.new_password_entry.pack()

        tk.Button(self.forget_password_window, text="Reset Password", command=self.reset_password).pack()

    def reset_password(self):
        email_or_mobile = self.email_or_mobile_entry.get()
        new_password = self.new_password_entry.get()

        # Connect to SQLite database
        conn = sqlite3.connect('evaluation.db')
        with conn:
            cursor = conn.cursor()
            # Update password in the database
            cursor.execute("UPDATE registration SET password = ? WHERE Email = ? OR Phoneno = ?", (new_password, email_or_mobile, email_or_mobile))

            # Check if any row was updated
            if cursor.rowcount > 0:
                messagebox.showinfo("Password Reset", "Password reset successful.")
                self.forget_password_window.destroy()
            else:
                messagebox.showerror("Error", "User not found or password not updated.")

root = tk.Tk()
app = GUI(root)
root.mainloop()

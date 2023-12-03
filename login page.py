import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess

def create_table():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_user(username, password):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

def check_user(username, password):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def show_sign_up_page():
    sign_up_window = tk.Toplevel(root)
    sign_up_window.title('Sign Up')
    sign_up_window.geometry("700x300")

    # Username and password entry widgets for sign-up
    username_label = tk.Label(sign_up_window, text="Enter Username:", font=("Monsterret", 11), fg="black")
    username_label.place(x=100, y=50)
    password_label = tk.Label(sign_up_window, text="Enter Password:", font=("Monsterret", 11), fg="black")
    password_label.place(x=100, y=100)
    confirm_password_label = tk.Label(sign_up_window, text="Confirm Password:", font=("Monsterret", 11), fg="black")
    confirm_password_label.place(x=100, y=150)

    # Entries
    username_entry = tk.Entry(sign_up_window, width=20, font=("Monsterret", 12))
    username_entry.place(x=370, y=53)
    password_entry = tk.Entry(sign_up_window, width=20, font=("Monsterret", 12), show="*")
    password_entry.place(x=370, y=103)
    confirm_password_entry = tk.Entry(sign_up_window, width=20, font=("Monsterret", 12), show="*")
    confirm_password_entry.place(x=370, y=153)

    # Sign-up button for the sign-up page
    sign_up_button = tk.Button(sign_up_window, text='Sign Up', height=2, width=10,
                               command=lambda: sign_up(sign_up_window, username_entry.get(), password_entry.get(),
                                                      confirm_password_entry.get()))
    sign_up_button.place(x=300, y=200)

def sign_up(window, username, password, confirm_password):
    if username and password and confirm_password:
        if password == confirm_password:
            create_table()
            insert_user(username, password)
            messagebox.showinfo('Success', 'Account created successfully!')
            window.destroy()
        else:
            messagebox.showerror('Error', 'Passwords do not match.')
    else:
        messagebox.showerror('Error', 'Username, password, and confirm password are required.')

def sign_in():
    username = username_entry.get()
    password = password_entry.get()

    if username and password:
        user = check_user(username, password)
        if user:
            messagebox.showinfo('Success', 'Login successful!')
            menu_page_path = "Menu Page.py"
            subprocess.run(["python", menu_page_path])
        else:
            messagebox.showerror('Error', 'Invalid username or password.')
    else:
        messagebox.showerror('Error', 'Username and password are required.')

# Main GUI setup
root = tk.Tk()
root.title('Expense Tracker')
root.geometry("700x300")

# Label
username_label = tk.Label(root, text="Enter your user name:", font=("Monsterret", 11), fg="black")
username_label.place(x=100, y=50)

# Label
password_label = tk.Label(root, text="Enter your password:", font=("Monsterret", 11), fg="black")
password_label.place(x=100, y=100)

# Entry widget (input bar)
username_entry = tk.Entry(root, width=20, font=("Monsterret", 12))
username_entry.place(x=370, y=53)
password_entry = tk.Entry(root, width=20, font=("Monsterret", 12), show="*")
password_entry.place(x=370, y=103)

# Button
Sign_in = tk.Button(root, text="Sign In", command=sign_in, font=("Monsterret", 10), height=2, width=10)
Sign_in.place(x=200, y=150)
Sign_up = tk.Button(root, text="Sign Up", command=show_sign_up_page, font=("Monsterret", 10), height=2, width=10)
Sign_up.place(x=400, y=150)

root.mainloop()

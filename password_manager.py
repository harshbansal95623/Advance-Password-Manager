import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import random
import string
import pyperclip

# Database setup
def init_db():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

# Authentication
def authenticate():
    passcode = "1234"  # Change this to your desired passcode
    while True:
        user_input = simpledialog.askstring("Authentication", "Enter passcode:", show='*')
        if user_input == passcode:
            return
        messagebox.showerror("Access Denied", "Incorrect passcode! Please try again.")

# Save password
def save_password():
    account = account_entry.get()
    password = password_entry.get()
    if account and password:
        conn = sqlite3.connect("passwords.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO passwords (account, password) VALUES (?, ?)", (account, password))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Password saved successfully!")
        account_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter both account name and password!")

# Retrieve password
def retrieve_password():
    def search_accounts(event):
        search_term = account_search_var.get()
        listbox.delete(0, tk.END)
        if search_term:
            conn = sqlite3.connect("passwords.db")
            cursor = conn.cursor()
            cursor.execute("SELECT account FROM passwords WHERE account LIKE ?", (f"%{search_term}%",))
            accounts = cursor.fetchall()
            conn.close()
            for acc in accounts:
                listbox.insert(tk.END, acc[0])

    def select_account():
        selected_account = listbox.get(tk.ACTIVE)
        if selected_account:
            conn = sqlite3.connect("passwords.db")
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM passwords WHERE account = ?", (selected_account,))
            result = cursor.fetchone()
            conn.close()
            if result:
                pyperclip.copy(result[0])
                messagebox.showinfo("Success", f"Password copied to clipboard: {result[0]}")
            else:
                messagebox.showerror("Error", "Account not found!")
        search_window.destroy()

    search_window = tk.Toplevel(root)
    search_window.title("Search Account")
    search_window.geometry("300x250")

    account_search_var = tk.StringVar()
    account_search_entry = tk.Entry(search_window, textvariable=account_search_var, width=30)
    account_search_entry.pack(pady=5)
    account_search_entry.bind("<KeyRelease>", search_accounts)
    
    listbox = tk.Listbox(search_window, width=40, height=10)
    listbox.pack(pady=5)
    
    tk.Button(search_window, text="Select", command=select_account).pack(pady=5)

# Generate custom password
def generate_password():
    try:
        length = int(simpledialog.askstring("Password Length", "Enter the password length:"))
        num_upper = int(simpledialog.askstring("Uppercase Letters", "Enter number of uppercase letters:"))
        num_lower = int(simpledialog.askstring("Lowercase Letters", "Enter number of lowercase letters:"))
        num_digits = int(simpledialog.askstring("Numbers", "Enter number of digits:"))
        num_symbols = int(simpledialog.askstring("Symbols", "Enter number of symbols:"))
        num_specials = int(simpledialog.askstring("Special Characters", "Enter number of special characters (e.g., @, #, $):"))

        assigned_length = num_upper + num_lower + num_digits + num_symbols + num_specials
        remaining_length = length - assigned_length

        if remaining_length < 0:
            messagebox.showerror("Error", "The sum of character counts exceeds the total length!")
            return
        
        special_chars = "@#$%^&*()_+={}[]|:;<>,.?/~"

        password_chars = (
            random.choices(string.ascii_uppercase, k=num_upper) +
            random.choices(string.ascii_lowercase, k=num_lower) +
            random.choices(string.digits, k=num_digits) +
            random.choices(string.punctuation, k=num_symbols) +
            random.choices(special_chars, k=num_specials) +
            random.choices(string.ascii_letters + string.digits + string.punctuation + special_chars, k=remaining_length)
        )
        random.shuffle(password_chars)
        password = ''.join(password_chars)

        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)
        pyperclip.copy(password)
        messagebox.showinfo("Generated", "Password copied to clipboard!")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values!")

# Toggle password visibility
def toggle_password_visibility():
    if password_entry.cget('show') == '*':
        password_entry.config(show='')
        toggle_button.config(text='Hide')
    else:
        password_entry.config(show='*')
        toggle_button.config(text='Show')

# GUI Setup
init_db()
root = tk.Tk()
root.withdraw()
authenticate()
root.deiconify()
root.title("Password Manager")
root.geometry("400x300")

# UI Elements
tk.Label(root, text="Account:").pack(pady=5)
account_entry = tk.Entry(root, width=30)
account_entry.pack(pady=5)

tk.Label(root, text="Password:").pack(pady=5)
password_entry = tk.Entry(root, width=30, show="*")
password_entry.pack(pady=5)

toggle_button = tk.Button(root, text="Show", command=toggle_password_visibility)
toggle_button.pack(pady=5)

tk.Button(root, text="Save Password", command=save_password).pack(pady=5)
tk.Button(root, text="Retrieve Password", command=retrieve_password).pack(pady=5)
tk.Button(root, text="Generate Password", command=generate_password).pack(pady=5)

tk.Button(root, text="Exit", command=root.quit).pack(pady=10)

root.mainloop()

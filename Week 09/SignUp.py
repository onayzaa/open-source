import tkinter as tk
from tkinter import messagebox


def save_credentials():
    """Save username and password to credentials.txt"""
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        messagebox.showwarning("Input Error", "Username and password cannot be empty.")
        return

    # Check if username already exists
    try:
        with open("credentials.txt", "r") as f:
            for line in f:
                saved_user, _ = line.strip().split(",", 1)
                if saved_user == username:
                    messagebox.showerror("Error", "Username already exists.")
                    return
    except FileNotFoundError:
        pass  # File doesn't exist yet, that's fine

    with open("credentials.txt", "a") as f:
        f.write(f"{username},{password}\n")

    messagebox.showinfo("Success", "Account created successfully!")


def check_credentials():
    """Check if entered credentials match any saved ones"""
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        messagebox.showwarning("Input Error", "Please enter username and password.")
        return

    try:
        with open("credentials.txt", "r") as f:
            for line in f:
                saved_user, saved_pass = line.strip().split(",", 1)
                if saved_user == username and saved_pass == password:
                    messagebox.showinfo("Success", f"Welcome, {username}!")
                    return
        messagebox.showerror("Error", "Invalid username or password.")
    except FileNotFoundError:
        messagebox.showerror("Error", "No accounts found. Please sign up first.")


def signin_window():
    """Build the UI"""
    global username_entry, password_entry

    tk.Label(root, text="Login", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(root, text="Username").pack()
    username_entry = tk.Entry(root)
    username_entry.pack(pady=2)

    tk.Label(root, text="Password").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=2)

    tk.Button(root, text="Sign In", width=15, command=check_credentials).pack(pady=5)
    tk.Button(root, text="Sign Up", width=15, command=save_credentials).pack()


# ── entry point ────────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Sign In")
root.geometry("300x250")

signin_window()       # ← was never called in your original code

root.mainloop()
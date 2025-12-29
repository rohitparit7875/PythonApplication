#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import sqlite3

# ---------- Database ----------
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL
)
""")
conn.commit()

# ---------- Functions ----------
def add_user():
    name = name_entry.get()
    email = email_entry.get()

    if name == "" or email == "":
        messagebox.showerror("Error", "All fields are required")
        return

    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    clear_fields()
    load_users()

def load_users():
    user_list.delete(0, tk.END)
    cursor.execute("SELECT * FROM users")
    for row in cursor.fetchall():
        user_list.insert(tk.END, row)

def select_user(event):
    try:
        selected = user_list.get(user_list.curselection())
        name_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        name_entry.insert(tk.END, selected[1])
        email_entry.insert(tk.END, selected[2])
    except:
        pass

def update_user():
    selected = user_list.get(user_list.curselection())
    cursor.execute(
        "UPDATE users SET name=?, email=? WHERE id=?",
        (name_entry.get(), email_entry.get(), selected[0])
    )
    conn.commit()
    clear_fields()
    load_users()

def delete_user():
    selected = user_list.get(user_list.curselection())
    cursor.execute("DELETE FROM users WHERE id=?", (selected[0],))
    conn.commit()
    clear_fields()
    load_users()

def clear_fields():
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)


# ---------- UI ----------
root = tk.Tk()
root.title("Simple CRUD App - Tkinter")
root.geometry("400x400")

tk.Label(root, text="Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Email").pack()
email_entry = tk.Entry(root)
email_entry.pack()

tk.Button(root, text="Add User", command=add_user).pack(pady=5)
tk.Button(root, text="Update User", command=update_user).pack(pady=5)
tk.Button(root, text="Delete User", command=delete_user).pack(pady=5)

user_list = tk.Listbox(root)
user_list.pack(fill=tk.BOTH, expand=True)
user_list.bind("<<ListboxSelect>>", select_user)

load_users()
root.mainloop()
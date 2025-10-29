import tkinter as tk
from tkinter import ttk, messagebox
import database

# Initialize Database
database.connect_db()

root = tk.Tk()
root.title("📘 Practical File Submission Tracker")
root.geometry("800x500")
root.config(bg="#f7f7f7")

# ---------- Title ----------
tk.Label(root, text="Practical File Submission Tracker", 
         font=("Arial", 18, "bold"), bg="#f7f7f7", fg="#333").pack(pady=10)

# ---------- Input Frame ----------
frame = tk.Frame(root, bg="#f7f7f7")
frame.pack(pady=5)

tk.Label(frame, text="Name:", bg="#f7f7f7").grid(row=0, column=0, padx=5)
name_entry = tk.Entry(frame, width=25)
name_entry.grid(row=0, column=1, padx=5)

tk.Label(frame, text="Subject:", bg="#f7f7f7").grid(row=0, column=2, padx=5)
subject_entry = tk.Entry(frame, width=25)
subject_entry.grid(row=0, column=3, padx=5)

tk.Label(frame, text="Status:", bg="#f7f7f7").grid(row=0, column=4, padx=5)
status_box = ttk.Combobox(frame, values=["Submitted", "Pending"], width=10)
status_box.set("Pending")
status_box.grid(row=0, column=5, padx=5)

# ---------- Button Frame ----------
btn_frame = tk.Frame(root, bg="#f7f7f7")
btn_frame.pack(pady=5)

def add_submission():
    name = name_entry.get().strip()
    subject = subject_entry.get().strip()
    status = status_box.get()
    
    if not name or not subject:
        messagebox.showwarning("Input Error", "Please fill all fields!")
        return

    database.add_submission(name, subject, status)
    messagebox.showinfo("Success", "Submission added successfully!")
    name_entry.delete(0, tk.END)
    subject_entry.delete(0, tk.END)
    status_box.set("Pending")
    load_data()

def delete_record():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select Record", "Please select a record to delete.")
        return
    values = tree.item(selected, 'values')
    record_id = values[0]
    database.delete_record(record_id)
    load_data()
    messagebox.showinfo("Deleted", "Record deleted successfully!")

def view_database():
    data = database.fetch_all()
    if not data:
        messagebox.showinfo("Database", "No records found in the database.")
        return

    # Create a new window to display data
    new_window = tk.Toplevel(root)
    new_window.title("Database Records")
    new_window.geometry("600x400")

    table = ttk.Treeview(new_window, columns=("ID", "Name", "Subject", "Status"), show="headings")
    table.heading("ID", text="ID")
    table.heading("Name", text="Name")
    table.heading("Subject", text="Subject")
    table.heading("Status", text="Status")
    table.pack(fill=tk.BOTH, expand=True)

    # Insert data into the table
    for row in data:
        table.insert("", tk.END, values=row)

tk.Button(btn_frame, text="Add", command=add_submission, width=10, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Delete", command=delete_record, width=10, bg="#f44336", fg="white").grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="View Database", command=view_database, width=12, bg="#2196F3", fg="white").grid(row=0, column=2, padx=5)

# ---------- Search and Filter ----------
filter_frame = tk.Frame(root, bg="#f7f7f7")
filter_frame.pack(pady=5)

tk.Label(filter_frame, text="Filter:", bg="#f7f7f7").grid(row=0, column=0)
filter_box = ttk.Combobox(filter_frame, values=["All", "Submitted", "Pending"], width=12)
filter_box.set("All")
filter_box.grid(row=0, column=1, padx=5)

tk.Label(filter_frame, text="Search by Name:", bg="#f7f7f7").grid(row=0, column=2)
search_entry = tk.Entry(filter_frame, width=25)
search_entry.grid(row=0, column=3, padx=5)

def filter_data(event=None):
    status = filter_box.get()
    data = database.filter_by_status(status)
    update_tree(data)

def search_data(event=None):
    name = search_entry.get().strip()
    if name == "":
        load_data()
    else:
        data = database.search_by_name(name)
        update_tree(data)

filter_box.bind("<<ComboboxSelected>>", filter_data)
search_entry.bind("<KeyRelease>", search_data)

# ---------- Treeview ----------
tree_frame = tk.Frame(root)
tree_frame.pack(pady=10)

columns = ("ID", "Name", "Subject", "Status")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=180)

tree.column("ID", width=50)
tree.pack()

# ---------- Load Data ----------
def update_tree(data):
    tree.delete(*tree.get_children())
    for row in data:
        tree.insert("", tk.END, values=row)

def load_data():
    data = database.fetch_all()
    update_tree(data)

load_data()

root.mainloop()
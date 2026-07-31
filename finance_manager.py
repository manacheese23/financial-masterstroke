import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import os
from datetime import datetime


# ==========================
# Constants
# ==========================

CSV_FILE = "transactions.csv"

# ==========================
# Main Window
# ==========================

root = tk.Tk()
root.title("FinTrack")
root.geometry("600x500")
root.resizable(False, False)

# ==========================
# Helper Functions
# ==========================

def coming_soon():
    messagebox.showinfo(
        "Coming Soon",
        "This feature will be implemented in the next phase."
    )


def create_menu_button(parent, text, command):
    button = tk.Button(
        parent,
        text=text,
        width=25,
        height=2,
        font=("Segoe UI", 11),
        command=command
    )
    button.pack(pady=5)


def initialize_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "ID",
                "Date",
                "Type",
                "Category",
                "Amount",
                "Description"
            ])


# ==========================
# Add Transaction Window
# ==========================
def save_transaction(
    add_window,
    date_entry,
    type_combo,
    category_combo,
    amount_entry,
    description_entry
):
    date = date_entry.get()
    transaction_type = type_combo.get()
    category = category_combo.get()
    amount = amount_entry.get()
    description = description_entry.get()

    # Check for empty fields
    if amount == "" or description == "":
        messagebox.showerror(
            "Error",
            "Please fill all fields."
        )
        return

    # Validate amount
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror(
            "Invalid Amount",
            "Amount must be a valid number."
        )
        return

    # Generate next transaction ID
    transaction_id = 1

    with open(CSV_FILE, "r", newline="") as file:
        reader = csv.reader(file)
        rows = list(reader)

        if len(rows) > 1:
            transaction_id = len(rows)

    # Save transaction
    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            transaction_id,
            date,
            transaction_type,
            category,
            amount,
            description
        ])

    messagebox.showinfo(
        "Success",
        "Transaction saved successfully."
    )

    add_window.destroy()
def open_add_window():

    add_window = tk.Toplevel(root)
    add_window.title("Add Transaction")
    add_window.geometry("400x350")
    add_window.resizable(False, False)

    # Labels
    tk.Label(add_window, text="Date").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    tk.Label(add_window, text="Type").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    tk.Label(add_window, text="Category").grid(row=2, column=0, padx=10, pady=10, sticky="w")
    tk.Label(add_window, text="Amount").grid(row=3, column=0, padx=10, pady=10, sticky="w")
    tk.Label(add_window, text="Description").grid(row=4, column=0, padx=10, pady=10, sticky="w")

# Date Entry (Today's date by default)
    today = datetime.now().strftime("%d-%m-%Y")

    date_entry = tk.Entry(add_window, width=25)
    date_entry.grid(row=0, column=1, padx=10, pady=10)

    date_entry.insert(0, today)
    # Type Dropdown
    type_combo = ttk.Combobox(
        add_window,
        values=["Income", "Expense"],
        state="readonly",
        width=22
    )
    type_combo.grid(row=1, column=1, padx=10, pady=10)
    type_combo.current(0)

    # Category Dropdown
    category_combo = ttk.Combobox(
        add_window,
        values=[
            "Food",
            "Transport",
            "Shopping",
            "Bills",
            "Entertainment",
            "Education",
            "Salary",
            "Freelance",
            "Other"
        ],
        state="readonly",
        width=22
    )
    category_combo.grid(row=2, column=1, padx=10, pady=10)
    category_combo.current(0)

    # Amount Entry
    amount_entry = tk.Entry(add_window, width=25)
    amount_entry.grid(row=3, column=1, padx=10, pady=10)

    # Description Entry
    description_entry = tk.Entry(add_window, width=25)
    description_entry.grid(row=4, column=1, padx=10, pady=10)

    # Save Button
    save_button = tk.Button(
        add_window,
        text="Save",
        width=15,
        command=lambda: save_transaction(
            add_window,
            date_entry,
            type_combo,
            category_combo,
            amount_entry,
            description_entry
        )
    )
    save_button.grid(
    row=5,
    column=0,
    columnspan=2,
    pady=20
    )


# ==========================
# Main Window
# ==========================

def create_main_window():

    header_frame = tk.Frame(root)
    header_frame.pack(pady=20)

    title_label = tk.Label(
        header_frame,
        text="FinTrack",
        font=("Segoe UI", 22, "bold")
    )
    title_label.pack()

    subtitle_label = tk.Label(
        header_frame,
        text="Personal Finance Manager",
        font=("Segoe UI", 12)
    )
    subtitle_label.pack()

    menu_frame = tk.Frame(root)
    menu_frame.pack(pady=30)

    create_menu_button(menu_frame, "Add Transaction", open_add_window)
    create_menu_button(menu_frame, "View Transactions", coming_soon)
    create_menu_button(menu_frame, "Monthly Summary", coming_soon)
    create_menu_button(menu_frame, "Delete Transaction", coming_soon)
    create_menu_button(menu_frame, "Exit", root.destroy)


# ==========================
# Start Application
# ==========================

initialize_csv()
create_main_window()

root.mainloop()
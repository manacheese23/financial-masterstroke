import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import os
from datetime import datetime

CSV_FILE = "transactions.csv"

root = tk.Tk()
root.title("FinTrack")
root.geometry("600x500")
root.resizable(False, False)



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

# Transaction Window

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

def search_transactions(search_text):

    results = []

    with open(CSV_FILE, "r", newline="") as file:

        reader = csv.reader(file)

        next(reader)

        for row in reader:

            for value in row:

                if search_text.lower() in value.lower():

                    results.append(row)

                    break

    return results
def perform_search(transaction_table, search_text):

    # Clear current rows
    for item in transaction_table.get_children():
        transaction_table.delete(item)

    # Decide what to show
    if search_text == "":
        with open(CSV_FILE, "r", newline="") as file:
            reader = csv.reader(file)
            next(reader)
            rows = list(reader)
    else:
        rows = search_transactions(search_text)

    # Insert rows
    for row in rows:
        transaction_table.insert(
            "",
            tk.END,
            values=row
        )

def open_manage_window():

    manage_window = tk.Toplevel(root)

    manage_window.title("Manage Transactions")
    manage_window.geometry("900x500")
    manage_window.resizable(False, False)

    search_frame = tk.Frame(manage_window)
    search_frame.pack(pady=10)

    tk.Label(
        search_frame,
        text="Search:"
    ).pack(side="left", padx=5)

    search_entry = tk.Entry(
        search_frame,
        width=30
    )
    search_entry.pack(side="left", padx=5)

    table = create_transaction_table(manage_window)

    tk.Button(
        search_frame,
        text="Search",
        command=lambda: perform_search(
            table,
            search_entry.get()
        )
    ).pack(side="left", padx=5)

    tk.Button(
        search_frame,
        text="Show All",
        command=lambda: perform_search(
            table,
            ""
        )
    ).pack(side="left", padx=5)

    button_frame = tk.Frame(manage_window)
    button_frame.pack(pady=10)

    tk.Button(
        button_frame,
        text="Edit Selected",
        width=18
    ).pack(side="left", padx=10)

    tk.Button(
        button_frame,
        text="Delete Selected",
        width=18,
        command=lambda: delete_transaction(
            manage_window,
            table
        )
    ).pack(side="left", padx=10)

    tk.Button(
        button_frame,
        text="Refresh",
        width=18,
        command=lambda: perform_search(
            table,
            ""
        )
    ).pack(side="left", padx=10)

def delete_transaction(delete_window, transaction_table):
    selected_item = transaction_table.selection()

    if not selected_item:
        messagebox.showwarning(
            "No Selection",
            "Please select a transaction."
        )
        return

    selected_values = transaction_table.item(
        selected_item,
        "values"
    )

    transaction_id = selected_values[0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this transaction?"
    )

    if not confirm:
        return

    # Read all rows
    with open(CSV_FILE, "r", newline="") as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Keep header and renumber IDs
    updated_rows = [rows[0]]
    new_id = 1

    for row in rows[1:]:
        if row[0] != transaction_id:
            row[0] = str(new_id)
            updated_rows.append(row)
            new_id += 1

    # Rewrite CSV
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)

    messagebox.showinfo(
        "Success",
        "Transaction deleted successfully."
    )

    perform_search(
    transaction_table,
    ""
)


def open_summary_window():

    summary_window = tk.Toplevel(root)

    summary_window.title("Monthly Summary")
    summary_window.geometry("400x300")
    summary_window.resizable(False, False)

    total_income = 0
    total_expense = 0
    transaction_count = 0

    with open(CSV_FILE, "r", newline="") as file:

        reader = csv.reader(file)

        next(reader)

        for row in reader:

            transaction_count += 1

            transaction_type = row[2]
            amount = float(row[4])

            if transaction_type == "Income":
                total_income += amount
            else:
                total_expense += amount

    net_balance = total_income - total_expense

    tk.Label(
        summary_window,
        text="Monthly Summary",
        font=("Segoe UI", 18, "bold")
    ).pack(pady=15)

    tk.Label(
        summary_window,
        text=f"Total Income : ₹{total_income:.2f}",
        font=("Segoe UI", 11)
    ).pack(pady=5)

    tk.Label(
        summary_window,
        text=f"Total Expense : ₹{total_expense:.2f}",
        font=("Segoe UI", 11)
    ).pack(pady=5)

    tk.Label(
        summary_window,
        text=f"Net Balance : ₹{net_balance:.2f}",
        font=("Segoe UI", 11)
    ).pack(pady=5)

    tk.Label(
        summary_window,
        text=f"Transactions : {transaction_count}",
        font=("Segoe UI", 11)
    ).pack(pady=5)
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
    create_menu_button(
    menu_frame,
    "Manage Transactions",
    open_manage_window
)
    create_menu_button(menu_frame, "Monthly Summary", open_summary_window)
    create_menu_button(menu_frame, "Exit", root.destroy)

def create_transaction_table(parent, rows=None):

    table_frame = tk.Frame(parent)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = (
        "ID",
        "Date",
        "Type",
        "Category",
        "Amount",
        "Description"
    )

    transaction_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    headings = [
        "ID",
        "Date",
        "Type",
        "Category",
        "Amount",
        "Description"
    ]

    for heading in headings:
        transaction_table.heading(heading, text=heading)

    transaction_table.column("ID", width=50, anchor="center")
    transaction_table.column("Date", width=100, anchor="center")
    transaction_table.column("Type", width=100, anchor="center")
    transaction_table.column("Category", width=120, anchor="center")
    transaction_table.column("Amount", width=100, anchor="center")
    transaction_table.column("Description", width=250)

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=transaction_table.yview
    )

    transaction_table.configure(
        yscrollcommand=scrollbar.set
    )

    if rows is None:

        with open(CSV_FILE, "r", newline="") as file:
            reader = csv.reader(file)

            next(reader)

            rows = list(reader)

    for row in rows:
        transaction_table.insert(
            "",
            tk.END,
            values=row
        )

    transaction_table.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    return transaction_table 

# Start Application
initialize_csv()
create_main_window()

root.mainloop()
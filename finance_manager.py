from statistics import mode
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

CSV_FILE = "transactions.csv"

# Theme
PRIMARY = "#8B5CF6"
SECONDARY = "#A78BFA"

BACKGROUND = "#111827"
CARD = "#1F2937"

TEXT = "#F9FAFB"
SUBTEXT = "#D1D5DB"

SUCCESS = "#22C55E"
DANGER = "#EF4444"

FONT_TITLE = ("SF Pro Display", 34, "bold")
FONT_HEADING = ("Segoe UI", 15, "bold")
FONT_BODY = ("Segoe UI", 11)
FONT_SMALL = ("Segoe UI", 10)
FONT_BUTTON = ("Segoe UI Semibold", 11)
BORDER = "#374151"
TABLE_HEADER = "#312E81"
TABLE_ROW = "#1F2937"


#Main
root = tk.Tk()
root.title("FinTrack")
root.geometry("720x650")
root.resizable(False, False)
root.configure(bg=BACKGROUND)



def coming_soon():
    messagebox.showinfo(
        "Coming Soon",
        "This feature will be implemented in the next phase."
    )


def create_menu_button(parent, text, command):
    button = tk.Button(
        parent,
        text=text,
        command=command,
        font=FONT_BODY,
        bg=PRIMARY,
        fg="white",
        activebackground=SECONDARY,
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        width=26,
        height=2
    )

    button.pack(pady=10)


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
def update_transaction(
    window,
    transaction_id,
    date_entry,
    type_combo,
    category_combo,
    amount_entry,
    description_entry,
    manage_window,
    transaction_table
):

    date = date_entry.get()
    transaction_type = type_combo.get()
    category = category_combo.get()
    amount = amount_entry.get()
    description = description_entry.get()

    if amount == "" or description == "":
        messagebox.showerror(
            "Error",
            "Please fill all fields."
        )
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror(
            "Invalid Amount",
            "Amount must be a valid number."
        )
        return

    with open(CSV_FILE, "r", newline="") as file:
        rows = list(csv.reader(file))

    for row in rows[1:]:
        if row[0] == transaction_id:
            row[1] = date
            row[2] = transaction_type
            row[3] = category
            row[4] = amount
            row[5] = description

    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    perform_search(
        transaction_table,
        "",
        "All",
        "All",
        "All"
)

    messagebox.showinfo(
        "Success",
        "Transaction updated successfully."
    )

    window.destroy()



def open_transaction_window(
    mode="add",
    selected_row=None,
    manage_window=None,
    transaction_table=None
):

    window = tk.Toplevel(root)
    window.configure(bg=BACKGROUND)
    
    if mode == "add":
        window.title("Add Transaction")
    else:
        window.title("Edit Transaction")
    window.geometry("400x350")
    window.resizable(False, False)

    # Labels
    tk.Label(window, text="Date",bg=BACKGROUND,fg=TEXT,font=FONT_BODY).grid(row=0, column=0, padx=18, pady=12, sticky="w")
    tk.Label(window, text="Type", bg=BACKGROUND, fg=TEXT, font=FONT_BODY).grid(row=1, column=0, padx=18, pady=12, sticky="w")
    tk.Label(window, text="Category", bg=BACKGROUND, fg=TEXT, font=FONT_BODY).grid(row=2, column=0, padx=18, pady=12, sticky="w")
    tk.Label(window, text="Amount", bg=BACKGROUND, fg=TEXT, font=FONT_BODY).grid(row=3, column=0, padx=18, pady=12, sticky="w")
    tk.Label(window, text="Description", bg=BACKGROUND, fg=TEXT, font=FONT_BODY).grid(row=4, column=0, padx=18, pady=12, sticky="w")

# Date Entry (Today's date by default)
    today = datetime.now().strftime("%d-%m-%Y")

    date_entry = tk.Entry(window,bg=BACKGROUND,fg=TEXT,font=FONT_BODY,width=25)
    date_entry.grid(row=0, column=1, padx=18, pady=12)

    date_entry.insert(0, today)
    # Type Dropdown
    type_combo = ttk.Combobox(
        window,
        values=["Income", "Expense"],
        state="readonly",
        width=22
    )
    type_combo.configure(font=FONT_BODY)
    type_combo.grid(row=1, column=1, padx=18, pady=12)
    type_combo.current(0)

    # Category Dropdown
    category_combo = ttk.Combobox(
        window,
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
    category_combo.configure(font=FONT_BODY)
    category_combo.grid(row=2, column=1, padx=18, pady=12)
    category_combo.current(0)

    # Amount Entry
    amount_entry = tk.Entry(window,bg=BACKGROUND, fg=TEXT, font=FONT_BODY, width=25)
    amount_entry.grid(row=3, column=1, padx=18, pady=12)

    # Description Entry
    description_entry = tk.Entry(window, bg=BACKGROUND, fg=TEXT, font=FONT_BODY, width=25)
    description_entry.grid(row=4, column=1, padx=18, pady=12)

        # Save Button
    button_text = "Save"

    if mode == "edit":
        button_text = "Update"
    if mode == "edit":

        date_entry.delete(0, tk.END)
        date_entry.insert(0, selected_row[1])

        type_combo.set(selected_row[2])

        category_combo.set(selected_row[3])

        amount_entry.insert(0, selected_row[4])

        description_entry.insert(0, selected_row[5])

    button_text = "Save"

    if mode == "edit":
        button_text = "Update"

    if mode == "add":

         button_command = lambda: save_transaction(
            window,
            date_entry,
             type_combo,
            category_combo,
             amount_entry,
            description_entry
    )

    else:

        button_command = lambda: update_transaction(
            window,
            selected_row[0],
            date_entry,
            type_combo,
            category_combo,
            amount_entry,
            description_entry,
            manage_window,
            transaction_table
    )

    save_button = tk.Button(
        window,
        text=button_text,
        command=button_command,
        font=FONT_BODY,
        bg=PRIMARY,
        fg="white",
        activebackground=SECONDARY,
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        width=18,
        pady=6
)

    save_button.grid(
        row=5,
        column=0,
        columnspan=2,
        pady=20
)

def search_transactions(
    search_text,
    search_by,
    type_filter,
    category_filter
):

    results = []

    column_map = {
        "ID": 0,
        "Date": 1,
        "Type": 2,
        "Category": 3,
        "Amount": 4,
        "Description": 5
    }

    with open(CSV_FILE, "r", newline="") as file:

        reader = csv.reader(file)
        next(reader)

        for row in reader:

            # Type Filter
            if type_filter != "All" and row[2] != type_filter:
                continue

            # Category Filter
            if category_filter != "All" and row[3] != category_filter:
                continue

            # Text Search
            if search_text == "":
                results.append(row)

            elif search_by == "All":

                for value in row:

                    if search_text.lower() in value.lower():
                        results.append(row)
                        break

            else:

                column = column_map[search_by]

                if search_text.lower() in row[column].lower():
                    results.append(row)

    return results

def perform_search(
    transaction_table,
    search_text,
    type_filter,
    category_filter,
    search_by
):

    for item in transaction_table.get_children():
        transaction_table.delete(item)

    rows = search_transactions(
        search_text,
        search_by,
        type_filter,
        category_filter
    )

    for row in rows:
        transaction_table.insert(
            "",
            tk.END,
            values=row
        )

def edit_selected(
    manage_window,
    transaction_table
):

    selected = transaction_table.selection()

    if not selected:
        messagebox.showwarning(
            "No Selection",
            "Please select a transaction."
        )
        return

    values = transaction_table.item(
        selected,
        "values"
    )

    open_transaction_window(
        mode="edit",
        selected_row=values,
        manage_window=manage_window,
        transaction_table=transaction_table
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
        text="Search By:"
    ).pack(side="left", padx=5)

    search_by = ttk.Combobox(
        search_frame,
        values=[
            "All",
            "ID",
            "Date",
            "Type",
            "Category",
            "Amount",
            "Description"
        ],
        state="readonly",
        width=12
)

    search_by.current(0)
    search_by.pack(side="left", padx=5)

    tk.Label(
    search_frame,
    text="Type:"
).pack(side="left", padx=5)

    type_filter = ttk.Combobox(
        search_frame,
        values=[
            "All",
            "Income",
            "Expense"
        ],
    state="readonly",
    width=10
)

    type_filter.current(0)
    type_filter.pack(side="left", padx=5)

    tk.Label(
        search_frame,
        text="Category:"
    ).pack(side="left", padx=5)

    category_filter = ttk.Combobox(
        search_frame,
        values=[
            "All",
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
        width=12
)

    category_filter.current(0)
    category_filter.pack(side="left", padx=5)
    

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
            search_entry.get(),
            type_filter.get(),
            category_filter.get(),
            search_by.get()
        )
    ).pack(side="left", padx=5)

    tk.Button(
        search_frame,
        text="Show All",
        command=lambda: (
            search_entry.delete(0, tk.END),
            search_by.current(0),
            type_filter.current(0),
            category_filter.current(0),
            perform_search(
                table,
                "",
                "All",
                "All",
                "All"
        )
    )
).pack(side="left", padx=5)

    button_frame = tk.Frame(manage_window)
    button_frame.pack(pady=10)

    tk.Button(
    button_frame,
    text="Edit Selected",
    width=18,
    command=lambda: edit_selected(
        manage_window,
        table
    )
).pack(
    side="left",
    padx=10
)

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
            "",
            "All",
            "All",
            "All"
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
        "",
        "All",
        "All",
        "All"
)


def open_summary_window():

    summary_window = tk.Toplevel(root)
    summary_window.title("Monthly Summary")
    summary_window.geometry("600x700")
    summary_window.resizable(False, False)

    canvas = tk.Canvas(summary_window)
    scrollbar = ttk.Scrollbar(
        summary_window,
        orient="vertical",
        command=canvas.yview
    )

    content = tk.Frame(canvas)

    content.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
    )
)

    canvas.create_window(
        (0, 0),
        window=content,
        anchor="nw"
)

    canvas.configure(
        yscrollcommand=scrollbar.set
)

    canvas.pack(
        side="left",
        fill="both",
        expand=True
)

    scrollbar.pack(
        side="right",
        fill="y"
    
)
    canvas.bind_all(
        "<MouseWheel>",
        lambda event: canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )
)

    total_income = 0
    total_expense = 0
    transaction_count = 0

    income_count = 0
    expense_count = 0

    highest_income = 0
    highest_expense = 0

    expense_categories = {}

    with open(CSV_FILE, "r", newline="") as file:

        reader = csv.reader(file)
        next(reader)

        for row in reader:

            transaction_count += 1

            transaction_type = row[2].strip().lower()
            category = row[3].strip().title()
            amount = float(row[4])

            if transaction_type == "income":

                total_income += amount
                income_count += 1

                if amount > highest_income:
                    highest_income = amount

            elif transaction_type == "expense":

                total_expense += amount
                expense_count += 1

                if amount > highest_expense:
                    highest_expense = amount

                if category not in expense_categories:
                    expense_categories[category] = 0

                expense_categories[category] += amount

    net_balance = total_income - total_expense

    average_income = 0
    average_expense = 0

    if income_count > 0:
        average_income = total_income / income_count

    if expense_count > 0:
        average_expense = total_expense / expense_count

    largest_category = ""
    largest_amount = 0

    for category, amount in expense_categories.items():

        if amount > largest_amount:
            largest_amount = amount
            largest_category = category

    tk.Label(
        content,
        text="Monthly Summary",
        font=("Segoe UI", 18, "bold")
    ).pack(pady=15)

    tk.Label(
        content,
        text=f"Total Income : ₹{total_income:.2f}",
        font=("Segoe UI", 11)
    ).pack(pady=5)

    tk.Label(
        content,
        text=f"Total Expense : ₹{total_expense:.2f}",
        font=("Segoe UI", 11)
    ).pack(pady=5)

    tk.Label(
        content,
        text=f"Net Balance : ₹{net_balance:.2f}",
        font=("Segoe UI", 11)
    ).pack(pady=5)

    tk.Label(
        content,
        text=f"Transactions : {transaction_count}",
        font=("Segoe UI", 11)
    ).pack(pady=5)

    tk.Label(
        content,
        text=f"Income Transactions : {income_count}",
        font=("Segoe UI", 11)
    ).pack(pady=5)

    tk.Label(
        content,
        text=f"Expense Transactions : {expense_count}",
        font=("Segoe UI", 11)
    ).pack(pady=5)

    tk.Label(
        content,
        text=f"Highest Income : ₹{highest_income:.2f}",
        font=("Segoe UI", 11)
    ).pack(pady=5)

    tk.Label(
        content,
        text=f"Highest Expense : ₹{highest_expense:.2f}",
        font=("Segoe UI", 11)
    ).pack(pady=5)

    tk.Label(
        content,
        text=f"Average Income : ₹{average_income:.2f}",
        font=("Segoe UI", 11)
    ).pack(pady=5)

    tk.Label(
        content,
        text=f"Average Expense : ₹{average_expense:.2f}",
        font=("Segoe UI", 11)
    ).pack(pady=5)

    tk.Label(
        content,
        text=f"Highest Spending Category : {largest_category}",
        font=("Segoe UI", 11, "bold")
    ).pack(pady=5)

    tk.Label(
        content,
        text=f"Spent : ₹{largest_amount:.2f}",
        font=("Segoe UI", 11)
    ).pack(pady=5)

    tk.Label(
        content,
        text=""
    ).pack()

    content.update_idletasks()

    canvas.configure(
        scrollregion=canvas.bbox("all")
    )

    # ----------------------------
# Expenses by Category
# ----------------------------

    tk.Label(
        content,
        text="Expenses by Category",
        font=("Segoe UI", 12, "bold")
    ).pack(pady=(15,5))

    category_table = ttk.Treeview(
        content,
        columns=("Category", "Amount"),
        show="headings",
        height=6
        )

    category_table.heading("Category", text="Category")
    category_table.heading("Amount", text="Amount")

    category_table.column("Category", width=170)
    category_table.column("Amount", width=120, anchor="center")

    for category, amount in sorted(
        expense_categories.items(),
        key=lambda x: x[1],
        reverse=True):

        category_table.insert(
            "",
            tk.END,
            values=(
                category,
                f"₹{amount:.2f}"
        )
    )

    category_table.pack(pady=5)
    button_frame = tk.Frame(content)
    button_frame.pack(pady=15)

    tk.Button(  
        button_frame,
        text="Expense Pie Chart",
        width=18,
        command=show_expense_pie_chart
    ).pack(side="left", padx=5)

    tk.Button(
        content,
        text="Show Expense Bar Chart",
        width=18,
        command=show_bar_chart
    ).pack(pady=10)
    tk.Button(
        button_frame,
        text="Income vs Expense",
        width=18,
        command=show_income_expense_chart
    ).pack(side="left", padx=5)

def show_bar_chart():

    category_totals = {}

    with open(CSV_FILE, "r", newline="") as file:

        reader = csv.reader(file)
        next(reader)

        for row in reader:

            transaction_type = row[2].strip().lower()

            if transaction_type == "expense":

                category = row[3].strip().title()
                amount = float(row[4])

                if category not in category_totals:
                    category_totals[category] = 0

                category_totals[category] += amount

    if len(category_totals) == 0:
        messagebox.showinfo(
            "No Data",
            "No expense transactions found."
        )
        return

    categories = list(category_totals.keys())
    amounts = list(category_totals.values())

    plt.figure(figsize=(8, 5))

    plt.bar(categories, amounts)

    plt.title("Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount (₹)")

    plt.xticks(rotation=30)

    plt.tight_layout()

    plt.show()

def show_expense_pie_chart():

    expense_categories = {}

    with open(CSV_FILE, "r", newline="") as file:

        reader = csv.reader(file)
        next(reader)

        for row in reader:

            if row[2].strip().lower() == "expense":

                category = row[3]
                amount = float(row[4])

                if category not in expense_categories:
                    expense_categories[category] = 0

                expense_categories[category] += amount

    if len(expense_categories) == 0:
        messagebox.showinfo(
            "No Data",
            "No expense transactions found."
        )
        return

    plt.figure(figsize=(6,6))

    plt.pie(
        expense_categories.values(),
        labels=expense_categories.keys(),
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("Expenses by Category")

    plt.tight_layout()

    plt.show()


def show_income_expense_chart():

    total_income = 0
    total_expense = 0

    with open(CSV_FILE, "r", newline="") as file:

        reader = csv.reader(file)
        next(reader)

        for row in reader:

            amount = float(row[4])

            if row[2].strip().lower() == "income":
                total_income += amount
            else:
                total_expense += amount

    plt.figure(figsize=(5,4))

    plt.bar(
        ["Income", "Expense"],
        [total_income, total_expense]
    )

    plt.ylabel("Amount (₹)")
    plt.title("Income vs Expense")

    plt.tight_layout()

    plt.show()


def setup_styles():

    style = ttk.Style()

    style.theme_use("clam")

    # Treeview
    style.configure(
        "Treeview",
        background=CARD,
        foreground=TEXT,
        fieldbackground=CARD,
        rowheight=30,
        font=FONT_BODY,
        borderwidth=0
    )

    # Selected row
    style.map(
        "Treeview",
        background=[("selected", PRIMARY)],
        foreground=[("selected", "white")]
    )

    # Header
    style.configure(
        "Treeview.Heading",
        background=PRIMARY,
        foreground="white",
        font=("Segoe UI", 11, "bold"),
        relief="flat"
    )

    style.map(
        "Treeview.Heading",
        background=[("active", SECONDARY)]
    )



# ==========================
# Main Window
# ==========================

def create_main_window():

    header_frame = tk.Frame(
        root,
        bg=BACKGROUND
)
    header_frame.pack(pady=(45, 20))

    title_label = tk.Label(
        header_frame,
        text="FinTrack",
        font=FONT_TITLE,
        fg=PRIMARY,
        bg=BACKGROUND
)
    title_label.pack()

    subtitle_label = tk.Label(
        header_frame,
        text="Personal Finance Manager",
        font=FONT_BODY,
        fg="#666666",
        bg=BACKGROUND
)
    subtitle_label.pack()
    

    menu_frame = tk.Frame(
        root,
        bg=BACKGROUND
)
    menu_frame.pack(pady=45)

    create_menu_button(
    menu_frame,
    "Add Transaction",
    lambda: open_transaction_window("add")
)
    create_menu_button(
    menu_frame,
    "Manage Transactions",
    open_manage_window
)
    create_menu_button(menu_frame, "Monthly Summary", open_summary_window)
    create_menu_button(menu_frame, "Exit", root.destroy)

def create_transaction_table(parent, rows=None):

    table_frame = tk.Frame(
        parent,
        bg=BACKGROUND
)
    table_frame.pack(fill="both", expand=True, padx=18, pady=10)

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

    transaction_table.column("ID", width=60, anchor="center")
    transaction_table.column("Date", width=110, anchor="center")
    transaction_table.column("Type", width=110, anchor="center")
    transaction_table.column("Category", width=130, anchor="center")
    transaction_table.column("Amount", width=110, anchor="center")
    transaction_table.column("Description", width=260)

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
setup_styles()
create_main_window()

root.mainloop()
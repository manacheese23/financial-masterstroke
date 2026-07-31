import tkinter as tk
from tkinter import messagebox
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

# ==========================
# GUI Functions
# ==========================
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

def create_main_window():
    # Header Frame
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

    # Menu Frame
    menu_frame = tk.Frame(root)
    menu_frame.pack(pady=30)

    create_menu_button(menu_frame, "Add Transaction", open_add_window)
    create_menu_button(menu_frame, "View Transactions", coming_soon)
    create_menu_button(menu_frame, "Monthly Summary", coming_soon)
    create_menu_button(menu_frame, "Delete Transaction", coming_soon)
    create_menu_button(menu_frame, "Exit", root.destroy)

def open_add_window():
    add_window = tk.Toplevel(root)

    add_window.title("Add Transaction")
    add_window.geometry("400x350")
    add_window.resizable(False, False)

# ==========================
# Start Application
# ==========================
initialize_csv()
create_main_window()

root.mainloop()
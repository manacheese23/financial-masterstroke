import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import csv
import os
from datetime import datetime

CSV_FILE = "transactions.csv"

root = tk.Tk()
root.title("FinTrack")
root.geometry("600x500")
root.resizable(False, False)


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


create_main_window()

root.mainloop()
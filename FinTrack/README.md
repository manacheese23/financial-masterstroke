# 💰 FinTrack

A Python-based personal finance management application built using **Python, Tkinter and Matplotlib**.

FinTrack provides a graphical interface to record, manage and analyse personal financial transactions. It allows users to track income and expenses, review monthly financial summaries and visualise spending patterns.

## ✨ Features

- **Transaction Management** — Add, edit and delete financial transactions.
- **Income and Expense Tracking** — Record and organise income and expenses.
- **Search and Filtering** — Search and filter transaction records.
- **Monthly Financial Summary** — View total income, expenses, net balance and other financial statistics.
- **Category Analysis** — Identify spending patterns across different expense categories.
- **Data Visualisation** — Generate charts to analyse financial activity.
- **CSV-Based Storage** — Maintain transaction records in an accessible CSV file.
- **Graphical User Interface** — Interactive desktop interface developed using Tkinter.

## 🖥️ Application Screenshots

### Main Menu

![FinTrack Main Menu](screenshots/Main%20menu.png)

### Add Transaction

![Add Transaction](screenshots/add%20transaction.png)

### Manage Transactions

![Manage Transactions](screenshots/manage%20transaction.png)

### Monthly Summary

**Financial Overview**

![Monthly Summary Overview](screenshots/Monthly%20summary%201.png)

**Category-wise Analysis**

![Category Analysis](screenshots/monthly%20summary%202%3B%20category.png)

**Financial Charts**

![Financial Charts](screenshots/monthly%20summary%203%3B%20charts.png)

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Tkinter | Graphical user interface |
| CSV | Transaction data storage |
| Matplotlib | Charts and data visualisation |

## 📂 Project Structure

```text
FinTrack/
│
├── README.md
├── finance_manager.py
├── transactions.csv
├── requirements.txt
│
├── assets/
│   ├── fintrack.ico
│   └── README.md
│
└── screenshots/
    ├── README.md
    ├── Main menu.png
    ├── add transaction.png
    ├── manage transaction.png
    ├── Monthly summary 1.png
    ├── monthly summary 2; category.png
    └── monthly summary 3; charts.png
```

## 🚀 Getting Started

### Option 1: Download the Windows Application

1. Visit the [FinTrack Releases](https://github.com/manacheese23/financial-masterstroke/releases) page.
2. Download `FinTrack-v1.0-Windows.zip`.
3. Extract the downloaded ZIP file.
4. Open the extracted folder.
5. Run `FinTrack.exe`.

**Note:** Keep all bundled files and folders together when running the application.

### Option 2: Run from Source Code

**Prerequisites:**
- Python 3
- pip (Python package installer)

**Installation:**

1. Clone the repository:

   ```bash
   git clone https://github.com/manacheese23/financial-masterstroke.git
   ```

2. Navigate to the application directory:

   ```bash
   cd financial-masterstroke/FinTrack
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python finance_manager.py
   ```

## 💾 Data Storage

FinTrack uses a CSV file named `transactions.csv` to store transaction records.

Each transaction contains the following fields:

- ID
- Date
- Type
- Category
- Amount
- Description

This allows financial records to be stored in a simple, accessible format.

## 🎯 Project Objectives

- Apply Python programming concepts to a practical application.
- Develop a desktop graphical user interface using Tkinter.
- Implement file handling and CSV-based data storage.
- Perform financial calculations and data analysis.
- Visualise financial information using Matplotlib.

## 📌 Future Improvements

- Budget planning and spending limits.
- More detailed financial reports.
- Data backup and restoration.
- Additional financial visualisations.
- Improved user interface and experience.

---

**FinTrack v1.0 | Windows Release**

Part of the [Financial Masterstroke](https://github.com/manacheese23/financial-masterstroke) project.

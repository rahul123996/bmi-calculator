import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt

# Database setup
def setup_database():
    conn = sqlite3.connect("bmi_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bmi_records (
            id INTEGER PRIMARY KEY,
            weight REAL,
            height REAL,
            bmi REAL,
            category TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_to_database(weight, height, bmi, category):
    conn = sqlite3.connect("bmi_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bmi_records (weight, height, bmi, category) VALUES (?, ?, ?, ?)",
                   (weight, height, bmi, category))
    conn.commit()
    conn.close()

# BMI Calculation
def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        if weight <= 0 or height <= 0:
            messagebox.showerror("Input Error", "Weight and height must be positive numbers.")
            return
        bmi = weight / (height ** 2)
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Normal weight"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obesity"
        result_label.config(text=f"BMI: {bmi:.2f}\nCategory: {category}")
        save_to_database(weight, height, bmi, category)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")

# Historical Data Visualization
def show_bmi_history():
    conn = sqlite3.connect("bmi_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT bmi FROM bmi_records")
    records = cursor.fetchall()
    conn.close()
    if not records:
        messagebox.showinfo("No Data", "No historical data found.")
        return
    bmis = [record[0] for record in records]
    plt.plot(bmis, marker='o')
    plt.title("BMI History")
    plt.xlabel("Entries")
    plt.ylabel("BMI")
    plt.show()

# GUI Setup
root = tk.Tk()
root.title("BMI Calculator")

tk.Label(root, text="Weight (kg):").grid(row=0, column=0)
weight_entry = tk.Entry(root)
weight_entry.grid(row=0, column=1)

tk.Label(root, text="Height (m):").grid(row=1, column=0)
height_entry = tk.Entry(root)
height_entry.grid(row=1, column=1)

calculate_button = tk.Button(root, text="Calculate BMI", command=calculate_bmi)
calculate_button.grid(row=2, column=0, columnspan=2)

result_label = tk.Label(root, text="BMI and Category will appear here.")
result_label.grid(row=3, column=0, columnspan=2)

history_button = tk.Button(root, text="Show BMI History", command=show_bmi_history)
history_button.grid(row=4, column=0, columnspan=2)

setup_database()
root.mainloop()


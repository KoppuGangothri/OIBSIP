# ----------------------------------------
# Import Required Libraries
# ----------------------------------------
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import os
import csv

# ----------------------------------------
# Create CSV File for Data Storage (if not exists)
# ----------------------------------------
if not os.path.exists("bmi_data.csv"):
    with open("bmi_data.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Weight (kg)", "Height (m)", "BMI", "Category"])

# ----------------------------------------
# BMI Category Function - Returns Category and Color Based on BMI
# ----------------------------------------
def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight", "blue"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight", "green"
    elif 25 <= bmi < 29.9:
        return "Overweight", "orange"
    else:
        return "Obese", "red"

# ----------------------------------------
# Function to Calculate BMI and Display the Result
# ----------------------------------------
def calculate_bmi():
    try:
        # Get data from entry fields
        name = entry_name.get().strip()
        weight = float(entry_weight.get())
        height = float(entry_height.get())

        # Validate inputs
        if not name or weight <= 0 or height <= 0:
            raise ValueError

        # Calculate BMI
        bmi = round(weight / (height ** 2), 2)
        category, color = get_bmi_category(bmi)

        # Display BMI and category in label
        label_result.config(text=f"BMI: {bmi} ({category})", fg=color)

        # Save the result in CSV file
        with open("bmi_data.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, weight, height, bmi, category])

        # Clear the input fields after submission
        entry_name.delete(0, tk.END)
        entry_weight.delete(0, tk.END)
        entry_height.delete(0, tk.END)

    except ValueError:
        # Show error message for invalid input
        messagebox.showerror("Invalid Input", "Please enter a valid name, weight, and height.")

# ----------------------------------------
# Function to Show BMI Trend in a Graph
# ----------------------------------------
def show_trend():
    names, bmis = [], []

    # Read data from the CSV file
    with open("bmi_data.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            names.append(row["Name"])
            bmis.append(float(row["BMI"]))

    # Check if data exists
    if names:
        # Optional: sort by BMI for better visualization
        combined = sorted(zip(names, bmis), key=lambda x: x[1])
        names, bmis = zip(*combined)

        # Plotting the BMI trend using matplotlib
        plt.figure(figsize=(10, 5))
        plt.plot(names, bmis, marker='o', color='purple')
        plt.title("BMI Trend Over Users", fontsize=14)
        plt.xlabel("User", fontsize=12)
        plt.ylabel("BMI", fontsize=12)
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        # Show info message if no data is found
        messagebox.showinfo("No Data", "No BMI records found.")

# ----------------------------------------
# GUI Setup using Tkinter
# ----------------------------------------
root = tk.Tk()
root.title("Advanced BMI Calculator")
root.geometry("400x500")
root.configure(bg="#f2f2f2")  # Light gray background

# ----------------------------------------
# Title Label
# ----------------------------------------
label_title = tk.Label(root, text="BMI Calculator", font=("Arial", 20, "bold"), bg="#f2f2f2")
label_title.pack(pady=20)

# ----------------------------------------
# Frame for Input Fields
# ----------------------------------------
frame = tk.Frame(root, bg="#f2f2f2")
frame.pack(pady=10)

# Helper Function to Create Label and Entry Together
def create_label_entry(text):
    label = tk.Label(frame, text=text, font=("Arial", 14), bg="#f2f2f2")
    label.pack(pady=5)
    entry = tk.Entry(frame, font=("Arial", 14), width=20)
    entry.pack(pady=5)
    return entry

# Entry fields for name, weight and height
entry_name = create_label_entry("Name:")
entry_weight = create_label_entry("Weight (kg):")
entry_height = create_label_entry("Height (m):")

# ----------------------------------------
# Button to Calculate BMI
# ----------------------------------------
btn_calculate = tk.Button(root, text="Calculate BMI", command=calculate_bmi,
                          font=("Arial", 14), bg="lightblue", width=20)
btn_calculate.pack(pady=15)

# ----------------------------------------
# Label to Show Result
# ----------------------------------------
label_result = tk.Label(root, text="", font=("Arial", 16, "bold"), bg="#f2f2f2")
label_result.pack(pady=10)

# ----------------------------------------
# Button to Show BMI Trend Graph
# ----------------------------------------
btn_trend = tk.Button(root, text="Show BMI Trend", command=show_trend,
                      font=("Arial", 14), bg="lightgreen", width=20)
btn_trend.pack(pady=10)

# ----------------------------------------
# Start the GUI Event Loop
# ----------------------------------------
root.mainloop()

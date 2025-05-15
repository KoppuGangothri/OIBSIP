# ------------------ 1. Importing Required Libraries ------------------ #
import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip

# ------------------ 2. Function to Generate Password ------------------ #
def generate_password():
    length = length_slider.get()
    include_letters = var_letters.get()
    include_digits = var_digits.get()
    include_symbols = var_symbols.get()

    if not (include_letters or include_digits or include_symbols):
        messagebox.showwarning("Selection Error", "Please select at least one character set.")
        return

    characters = ""
    if include_letters:
        characters += string.ascii_letters
    if include_digits:
        characters += string.digits
    if include_symbols:
        characters += string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

# ------------------ 3. Function to Copy Password to Clipboard ------------------ #
def copy_to_clipboard():
    password = password_entry.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showwarning("No Password", "Generate a password first.")

# ------------------ 4. GUI Window Setup ------------------ #
root = tk.Tk()
root.title("Random Password Generator")
root.geometry("400x300")
root.resizable(False, False)

# ------------------ 5. Heading Label ------------------ #
tk.Label(root, text="Password Generator", font=("Arial", 16, "bold")).pack(pady=10)

# ------------------ 6. Password Entry Box ------------------ #
password_entry = tk.Entry(root, font=("Arial", 14), width=30, justify='center')
password_entry.pack(pady=5)

# ------------------ 7. Options Frame (Character Set Selection) ------------------ #
options_frame = tk.Frame(root)
options_frame.pack(pady=10)

# Character type options
var_letters = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=True)

tk.Checkbutton(options_frame, text="Letters", variable=var_letters).grid(row=0, column=0, padx=5)
tk.Checkbutton(options_frame, text="Digits", variable=var_digits).grid(row=0, column=1, padx=5)
tk.Checkbutton(options_frame, text="Symbols", variable=var_symbols).grid(row=0, column=2, padx=5)

# ------------------ 8. Password Length Selection (Slider) ------------------ #
tk.Label(root, text="Password Length:").pack()
length_slider = tk.Scale(root, from_=4, to=32, orient=tk.HORIZONTAL)
length_slider.set(12)
length_slider.pack()

# ------------------ 9. Buttons for Generating and Copying Password ------------------ #
tk.Button(root, text="Generate Password", command=generate_password, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=5)
tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard, font=("Arial", 12)).pack()

# ------------------ 10. Starting the GUI Main Loop ------------------ #
root.mainloop()

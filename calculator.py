import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os

HISTORY_FILE = "history.txt"

root = tk.Tk()
root.title("Modern Calculator")
root.geometry("360x560")
root.resizable(False, False)
root.configure(bg="#1e1e1e")

expression = ""

display_var = tk.StringVar()

# ---------------------------
# History Functions
# ---------------------------

def save_history(entry):
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")

def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("Calculation History")
    history_window.geometry("700x400")
    history_window.configure(bg="#1e1e1e")

    text = tk.Text(
        history_window,
        bg="#252526",
        fg="white",
        font=("Consolas", 11)
    )
    text.pack(fill="both", expand=True)

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            text.insert("1.0", f.read())
    else:
        text.insert("1.0", "No history available.")

def clear_history():
    open(HISTORY_FILE, "w").close()
    messagebox.showinfo("History", "History cleared!")

# ---------------------------
# Calculator Logic
# ---------------------------

def click(value):
    global expression
    expression += str(value)
    display_var.set(expression)

def clear():
    global expression
    expression = ""
    display_var.set("")

def backspace():
    global expression
    expression = expression[:-1]
    display_var.set(expression)

def calculate():
    global expression

    try:
        result = str(eval(expression))

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history_entry = f"[{timestamp}] {expression} = {result}"
        save_history(history_entry)

        display_var.set(result)
        expression = result

    except:
        display_var.set("Error")
        expression = ""

# ---------------------------
# Display
# ---------------------------

display = tk.Entry(
    root,
    textvariable=display_var,
    font=("Segoe UI", 28),
    bg="#252526",
    fg="white",
    bd=0,
    justify="right",
    insertbackground="white"
)

display.pack(fill="x", padx=10, pady=20, ipady=20)

# ---------------------------
# Top Buttons
# ---------------------------

top_frame = tk.Frame(root, bg="#1e1e1e")
top_frame.pack(fill="x", padx=10)

tk.Button(
    top_frame,
    text="History",
    command=show_history,
    bg="#3a3a3a",
    fg="white",
    font=("Segoe UI", 10),
    relief="flat"
).pack(side="left", padx=5)

tk.Button(
    top_frame,
    text="Clear History",
    command=clear_history,
    bg="#3a3a3a",
    fg="white",
    font=("Segoe UI", 10),
    relief="flat"
).pack(side="right", padx=5)

# ---------------------------
# Calculator Buttons
# ---------------------------

buttons = [
    ["C", "⌫", "/", "*"],
    ["7", "8", "9", "-"],
    ["4", "5", "6", "+"],
    ["1", "2", "3", "="],
    ["0", ".", "(", ")"]
]

button_frame = tk.Frame(root, bg="#1e1e1e")
button_frame.pack(expand=True, fill="both", padx=10, pady=10)

for r, row in enumerate(buttons):
    for c, text in enumerate(row):

        if text == "=":
            cmd = calculate
        elif text == "C":
            cmd = clear
        elif text == "⌫":
            cmd = backspace
        else:
            cmd = lambda t=text: click(t)

        btn = tk.Button(
            button_frame,
            text=text,
            command=cmd,
            font=("Segoe UI", 18, "bold"),
            bg="#2d2d30",
            fg="white",
            activebackground="#404040",
            activeforeground="white",
            relief="flat",
            bd=0
        )

        btn.grid(
            row=r,
            column=c,
            sticky="nsew",
            padx=4,
            pady=4
        )

for i in range(5):
    button_frame.rowconfigure(i, weight=1)

for i in range(4):
    button_frame.columnconfigure(i, weight=1)

# ---------------------------
# Keyboard Support
# ---------------------------

def key_press(event):
    key = event.char

    if key in "0123456789+-*/().":
        click(key)

    elif event.keysym == "Return":
        calculate()

    elif event.keysym == "BackSpace":
        backspace()

root.bind("<Key>", key_press)

root.mainloop()
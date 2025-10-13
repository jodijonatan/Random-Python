import tkinter as tk

def click_button(value):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(tk.END, current + value)

def calculate():
    try:
        result = eval(entry.get())
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")

def clear():
    entry.delete(0, tk.END)

def backspace():
    current = entry.get()
    entry.delete(len(current)-1, tk.END)

root = tk.Tk()
root.title("Kalkulator")
root.geometry("400x550")
root.config(bg="#333333")

entry = tk.Entry(root, width=15, font=("Helvetica", 24), borderwidth=2, relief="solid", justify="right", bd=10, fg="white", bg="#222222")
entry.grid(row=0, column=0, columnspan=4, pady=20)

button_style = {
    "font": ("Helvetica", 18),
    "width": 4,
    "height": 2,
    "relief": "solid",
    "bd": 5,
    "fg": "white",
    "bg": "#4CAF50",
    "activebackground": "#45a049",
    "activeforeground": "white"
}

buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
    ('C', 5, 0), ('<-', 5, 1)
]

for (text, row, col) in buttons:
    if text == "=":
        button = tk.Button(root, text=text, command=calculate, font=("Helvetica", 18), width=4, height=2, relief="solid", bd=5, fg="black", bg="#FF6347", activebackground="#FF4500", activeforeground="white")
    elif text == "C":
        button = tk.Button(root, text=text, command=clear, **button_style)
    elif text == "<-":
        button = tk.Button(root, text=text, command=backspace, **button_style)
    else:
        button = tk.Button(root, text=text, command=lambda value=text: click_button(value), **button_style)
    button.grid(row=row, column=col, padx=10, pady=10)

root.mainloop()
k
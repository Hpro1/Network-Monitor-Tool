import tkinter as tk
from tkinter import ttk
import os
import threading
import platform

# Placeholder for values
class PlaceholderEntry(ttk.Entry):
    def __init__(self, container, placeholder, **kwargs):
        super().__init__(container, **kwargs)
        self.placeholder = placeholder
        self.insert(0, self.placeholder)
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)

    def _clear_placeholder(self, e):
        if self.get() == self.placeholder:
            self.delete(0, "end")

    def _add_placeholder(self, e=None):
        if not self.get():
            self.insert(0, self.placeholder)

# Check the connectivity
def ping_ip(ip, canvas, indicator):
    # Check OS
    current_os = platform.system().lower()
    if current_os == "windows":
        # Windows: '-n' is the count of echo requests to send
        response = os.system(f"ping -n 1 -w 1000 {ip}")
    else:
        # macOS and others: '-c' is the count of pings
        response = os.system(f"ping -c 1 -W 1000 {ip}")
    
    color = 'green1' if response == 0 else 'red1'
    canvas.itemconfig(indicator, fill=color)

def start_ping_thread(ip, canvas, indicator):
    threading.Thread(target=ping_ip, args=(ip, canvas, indicator), daemon=True).start()

def update_status(rows):
    for row in rows:
        ip_or_hostname = row['entry'].get().strip()
        canvas = row['canvas']
        indicator = row['indicator']
        # Check if the IP address or hostname field is empty
        if not ip_or_hostname or ip_or_hostname == "IP Address":
            canvas.itemconfig(indicator, fill='red1')
            continue
        # Attempt to ping the IP or hostname
        start_ping_thread(ip_or_hostname, canvas, indicator)
    root.after(12000, lambda: update_status(rows))

def toggle_lock(row):
    # Check current state of the entry field
    if row['entry']['state'] == tk.NORMAL:
        # If it's normal (editable), change it to disabled
        new_state = tk.DISABLED
        lock_text = '🔒'
    else:
        # If it's disabled, change it to normal (editable)
        new_state = tk.NORMAL
        lock_text = '🔓'

    # Apply the new state to all relevant widgets in the row
    for widget in ['entry', 'name_entry', 'desc_entry']:
        row[widget]['state'] = new_state
    row['lock_btn']['text'] = lock_text

def add_row(tab, rows):
    row = create_row(tab, rows)
    rows.append(row)
    update_status(rows)

def remove_row(rows, row):
    row['frame'].destroy()
    rows.remove(row)

def create_row(tab, rows):
    row = {}
    frame = ttk.Frame(tab)
    frame.pack(fill='x', padx=5, pady=5)

    dark_theme_background_color = '#3a3a3a'

    # Canvas with the same bg color
    canvas = tk.Canvas(frame, width=16, height=16, bg=dark_theme_background_color, highlightthickness=0)
    canvas.pack(side='left', padx=(5, 0))
    indicator = canvas.create_oval(3, 3, 13, 13, fill='red1', outline='')

    entry = PlaceholderEntry(frame, "IP Address")
    entry.pack(side='left', fill='x', expand=True)

    name_entry = PlaceholderEntry(frame, "Name")
    name_entry.pack(side='left', fill='x', expand=True)

    desc_entry = PlaceholderEntry(frame, "Description")
    desc_entry.pack(side='left', fill='x', expand=True)

    lock_btn = ttk.Button(frame, text='🔓', command=lambda: toggle_lock(row))
    lock_btn.pack(side='left', padx=5)

    remove_btn = ttk.Button(frame, text='-', command=lambda: remove_row(rows, row))
    remove_btn.pack(side='left', padx=5)

    row.update({'frame': frame, 'canvas': canvas, 'indicator': indicator, 
                'entry': entry, 'name_entry': name_entry, 'desc_entry': desc_entry, 'lock_btn': lock_btn})
    return row

def add_row_to_current_tab():
    current_tab = notebook.nametowidget(notebook.select())
    rows = pages[current_tab]
    add_row(current_tab, rows)

# Clear focus from entry fields
def clear_focus(event=None):
    root.focus_set()

# GUI setup
root = tk.Tk()
root.title("Network Monitor Tool")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both', padx=5, pady=5)

pages = {}
for i in range(1, 4):
    page_name = f"Page{i}"
    tab = ttk.Frame(notebook)
    notebook.add(tab, text=page_name)
    pages[tab] = []

add_btn = ttk.Button(root, text='+', command=add_row_to_current_tab)
add_btn.pack(side='bottom', padx=5, pady=5)

root.bind("<Escape>", clear_focus)

root.mainloop()

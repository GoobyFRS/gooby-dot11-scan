#!/usr/bin/env python3
# Shebang is not needed for Windows.
import tkinter as tk
from tkinter import ttk
import subprocess
import re

def scan_wifi():
    command = "netsh wlan show networks mode=bssid"
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    
    networks = []
    ssid = None
    
    for line in result.stdout.split("\n"):
        line = line.strip()
        ssid_match = re.match(r"SSID \d+ : (.+)", line)
        mac_match = re.match(r"BSSID \d+ *: ([0-9A-Fa-f:-]+)", line)
        signal_match = re.search(r"Signal *: (\d+)%", line)
        
        if ssid_match:
            ssid = ssid_match.group(1)
        elif mac_match and ssid:
            mac = mac_match.group(1)
            if signal_match:
                signal_percent = int(signal_match.group(1))
                signal_dbm = (signal_percent / 2) - 100  # Convert percentage to dBm
            else:
                signal_dbm = -100  # Default to lowest signal if not found
            networks.append((ssid, mac, signal_dbm))
    
    networks.sort(key=lambda x: x[2], reverse=True)
    
    for row in tree.get_children():
        tree.delete(row)
    
    for net in networks:
        tree.insert("", tk.END, values=net)

root = tk.Tk()
root.title("Dot11 Scan")
root.geometry("720x340")

columns = ("SSID", "MAC Address", "Signal Strength (-dBm)")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=300)

tree.pack(expand=True, fill="both")

scan_button = tk.Button(root, text="Scan for DOT11", command=scan_wifi)
scan_button.pack(pady=10)

root.mainloop()

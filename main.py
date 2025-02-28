#!/usr/bin/env python3
# shebang is not needed for Windows. Leaving for basic Unix support.
import tkinter as tk
from tkinter import ttk
import subprocess
import re

def scan_wifi():
    command = "netsh wlan show networks mode=bssid" #PowerShell Command
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    
    networks = []
    #ssid = None
    #mac = None
    #channel = None

    lines = result.stdout.split("\n")
    for i in range(len(lines)):
        line = lines[i].strip()

        ssid_match = re.match(r"SSID \d+ : (.+)", line)
        mac_match = re.match(r"BSSID \d+ *: ([0-9A-Fa-f:-]+)", line)
        #channel_match = re.search(r"Channel\s*:\s*(\d+)", line)

        if ssid_match:
            ssid = ssid_match.group(1) if ssid_match.group(1).strip() else "Hidden SSID"
        
        elif mac_match:
            mac = mac_match.group(1)
            # The next line should contain the Signal Strength
            if i + 1 < len(lines):
                signal_match = re.search(r"Signal\s*:\s*(\d+)%", lines[i + 1].strip())
                if signal_match:
                    signal = f"{signal_match.group(1)}%"
                else:
                    signal = "No Data"
                networks.append((ssid, mac, signal))

    # Clear the table
    for row in tree.get_children():
        tree.delete(row)
    
    # Insert new scan results
    for net in sorted(networks, key=lambda x: int(x[2].replace('%', '')), reverse=True):
        tree.insert("", tk.END, values=net)

root = tk.Tk()
root.title("Goobys Wi-Fi Scanner")
root.geometry("720x480")

columns = ("BSSID", "BSSID MAC Address", "Signal Strength")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.pack(expand=True, fill="both")

scan_button = tk.Button(root, text="Scan DOT11 RF", command=scan_wifi)
scan_button.pack(padx=10, pady=10)

root.mainloop()

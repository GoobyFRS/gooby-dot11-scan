import tkinter as tk
from tkinter import ttk
import subprocess
import re

def scan_wifi():
    """ Powershell command example output
    SSID 2 : THE_NEIGHBORS_WIFI
    Network type            : Infrastructure
    Authentication          : WPA2-Personal
    Encryption              : CCMP
    BSSID 1                 : a0:b1:c2:d3:e4:cb
         Signal             : 24%
         Radio type         : 802.11ax
         Channel            : 44
         Basic rates (Mbps) : 6 12 24
         Other rates (Mbps) : 9 18 36 48 54
    BSSID 2                 : a0:b1:c2:d3:e4:ca
         Signal             : 38%
         Radio type         : 802.11ac
         Channel            : 1
         Basic rates (Mbps) : 1 2 5.5 11
         Other rates (Mbps) : 6 9 12 18 24 36 48 54
    BSSID 3                 : a0:b1:c2:d3:e4:3b
    """
    command = "netsh wlan show networks mode=bssid"
    ps_cmd_output = subprocess.run(command, capture_output=True, text=True, shell=True)
    
    networks = []
    current_ssid = None  # Stores the current SSID while parsing
    current_bssid = None  # Stores the last BSSID encountered

    for line in ps_cmd_output.stdout.split("\n"):
        line = line.strip()

        # Match SSID, BSSID, Signal Strength, and Channel using regex.
        ssid_match = re.match(r"SSID \d+ : (.+)", line)
        mac_match = re.match(r"BSSID \d+ *: ([0-9A-Fa-f:-]+)", line)
        signal_match = re.match(r"Signal\s*:\s*(\d+)%", line)
        channel_match = re.match(r"Channel\s*:\s*(\d+)", line)

        if ssid_match:
            # If an SSID is empty, label it as "Hidden SSID"
            current_ssid = ssid_match.group(1).strip() or "Hidden SSID"
        elif mac_match and current_ssid:
            # Start a new BSSID entry
            current_bssid = mac_match.group(1)
            networks.append([current_ssid, current_bssid, "N/A", "N/A"])  # Default values
        elif signal_match and current_bssid:
            # Update the last added entry with signal strength
            networks[-1][2] = f"{signal_match.group(1)}%"
        elif channel_match and current_bssid:
            # Update the last added entry with channel
            networks[-1][3] = channel_match.group(1)

    # Clear existing data before inserting new results.
    tree.delete(*tree.get_children())

    # Sort networks by signal strength (descending), treating "N/A" as the weakest.
    sorted_networks = sorted(networks, key=lambda x: int(x[2].strip('%')) if x[2] != "N/A" else -1, reverse=True)

    # Populate the table with sorted networks.
    for net in sorted_networks:
        tree.insert("", tk.END, values=net)

    # Schedule the next scan every 15 seconds.
    root.after(15000, scan_wifi)

# Initialize the main Tkinter window.
root = tk.Tk()
root.title("Matts Wi-Fi Scanner")
root.geometry("720x480")  # Set default window size

# Define table columns
columns = ("SSID", "MAC Address", "Signal Strength", "Channel")
tree = ttk.Treeview(root, columns=columns, show="headings")

# Configure column headings and widths.
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=140)

# Add the table to the GUI
tree.pack(expand=True, fill="both")

# Add a manual scan button.
scan_button = tk.Button(root, text="Scan Wi-Fi", command=scan_wifi)
scan_button.pack(pady=10)

# Run the first scan when the application starts.
scan_wifi()

# Start the Tkinter event loop.
root.mainloop()

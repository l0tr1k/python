import nmap
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import os

def run_scan():
    target = target_entry.get()
    scan_type = scan_type_var.get()
    
    # Ensure Nmap is in the PATH
    os.environ['PATH'] += r";C:\Program Files (x86)\Nmap"
    nm = nmap.PortScanner()
    
    try:
        # Perform the scan based on user selection
        if scan_type == "Basic":
            nm.scan(target, arguments="-sV")
        elif scan_type == "Vulnerability":
            nm.scan(target, arguments="-sV --script vuln")
        
        # Process the results
        result = ""
        for host in nm.all_hosts():
            result += f"Host: {host}\n"
            result += f"State: {nm[host].state()}\n"
            for proto in nm[host].all_protocols():
                result += f"Protocol: {proto}\n"
                ports = nm[host][proto].keys()
                for port in ports:
                    result += f"Port: {port}\n"
                    result += f"State: {nm[host][proto][port]['state']}\n"
                    result += f"Service: {nm[host][proto][port]['name']}\n"
                    if 'script' in nm[host][proto][port]:
                        result += "Vulnerabilities:\n"
                        for script, output in nm[host][proto][port]['script'].items():
                            result += f"{script}: {output}\n"
                    result += "\n"
        
        # Display results in a new window with a ScrolledText widget
        result_window = tk.Toplevel(root)
        result_window.title("Scan Results")
        result_window.geometry("600x400")
        
        result_text = scrolledtext.ScrolledText(result_window, wrap=tk.WORD, width=70, height=20)
        result_text.pack(expand=True, fill='both', padx=10, pady=10)
        result_text.insert(tk.END, result)
        result_text.config(state=tk.DISABLED)  # Make the text widget read-only
        
    except nmap.PortScannerError as e:
        messagebox.showerror("Error", f"Nmap scan failed: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("Nmap Scanner")
root.geometry("300x200")

# Create and pack the input fields
tk.Label(root, text="Target IP/Host:").pack(pady=5)
target_entry = tk.Entry(root, width=30)
target_entry.pack()

tk.Label(root, text="Scan Type:").pack(pady=5)
scan_type_var = tk.StringVar(value="Basic")
tk.Radiobutton(root, text="Basic", variable=scan_type_var, value="Basic").pack()
tk.Radiobutton(root, text="Vulnerability", variable=scan_type_var, value="Vulnerability").pack()

# Create and pack the scan button
scan_button = tk.Button(root, text="Run Scan", command=run_scan)
scan_button.pack(pady=10)

# Start the GUI event loop
root.mainloop()

import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
import folium
import webbrowser
import tempfile

# ------------------------------
# Function to do the lookup
def lookup_ip():
    ip = ip_entry.get().strip()
    if not ip:
        messagebox.showerror("Error", "Please enter an IP address")
        return

    url = f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,zip,lat,lon,isp,org,as"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("status") != "success":
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, f"Error: {data.get('message', 'Unknown error')}")
            return

        # Show results in text box
        output_text.delete(1.0, tk.END)
        for key, value in data.items():
            output_text.insert(tk.END, f"{key}: {value}\n")

        # Show map in browser if coordinates exist
        lat = data.get("lat")
        lon = data.get("lon")
        if lat and lon:
            fmap = folium.Map(location=[lat, lon], zoom_start=5)
            folium.Marker([lat, lon], tooltip=ip).add_to(fmap)

            # Save map to temp HTML and open in browser
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
            fmap.save(tmp_file.name)
            webbrowser.open(f"file://{tmp_file.name}")

    except Exception as e:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Request failed: {str(e)}")

# ------------------------------
# GUI Setup
root = tk.Tk()
root.title("IP Lookup Tool by p6sd")
root.geometry("600x500")

tk.Label(root, text="Enter IP Address:").pack(pady=5)
ip_entry = tk.Entry(root, width=30)
ip_entry.pack(pady=5)

lookup_button = tk.Button(root, text="Lookup", command=lookup_ip)
lookup_button.pack(pady=10)

output_text = scrolledtext.ScrolledText(root, width=70, height=20)
output_text.pack(pady=5)

root.mainloop()

from tkinter import simpledialog, messagebox
from geopy.geocoders import Nominatim
from typing import Dict, Optional


def geocode_location(query: str) -> Optional[Dict[str, str]]:
    geolocator = Nominatim(user_agent="ai-cloudops-geo")
    location = geolocator.geocode(query)
    if not location:
        return None
    address_parts = [p.strip() for p in location.address.split(",")]
    city = address_parts[-3] if len(address_parts) >= 3 else address_parts[0]
    return {
        "latitude": str(location.latitude),
        "longitude": str(location.longitude),
        "city": city,
        "address": location.address,
    }


def prompt_and_show_location():
    location_input = simpledialog.askstring(
        "Location Input", "Enter your location (address or city):"
    )
    if not location_input:
        messagebox.showerror("Error", "Location input is empty.")
        return

    data = geocode_location(location_input)
    if not data:
        messagebox.showerror("Error", "Unable to retrieve location details.")
        return

    message = f"Latitude: {data['latitude']}\nLongitude: {data['longitude']}\nCity: {data['city']}"
    messagebox.showinfo("Location Details", message)


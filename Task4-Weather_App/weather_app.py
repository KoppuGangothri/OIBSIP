import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io

# -------------------- API KEY --------------------
API_KEY = "your_api_key"  # Your API key

# -------------------- Weather Fetching Function --------------------
def get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    unit_type = "metric" if temp_unit.get() == "C" else "imperial"
    temp_sign = "°C" if unit_type == "metric" else "°F"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={unit_type}"

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            messagebox.showerror("Error", data["message"])
            return

        weather_data = {
            "city": f"{data['name']}, {data['sys']['country']}",
            "temp": f"{data['main']['temp']} {temp_sign}",
            "condition": data['weather'][0]['description'].title(),
            "humidity": f"{data['main']['humidity']}%",
            "wind": f"{data['wind']['speed']} m/s",
            "icon": data['weather'][0]['icon']
        }

        display_weather(weather_data)

    except Exception as e:
        messagebox.showerror("Error", f"Could not get weather data.\n{str(e)}")

# -------------------- Display Weather Function --------------------
def display_weather(weather):
    result_label.config(text=f"📍 {weather['city']}\n"
                             f"🌡️ Temp: {weather['temp']}\n"
                             f"☁️ Condition: {weather['condition']}\n"
                             f"💧 Humidity: {weather['humidity']}\n"
                             f"🌬️ Wind: {weather['wind']}")

    icon_url = f"http://openweathermap.org/img/wn/{weather['icon']}@2x.png"
    icon_response = requests.get(icon_url)
    img_data = icon_response.content
    img = Image.open(io.BytesIO(img_data))
    icon_photo = ImageTk.PhotoImage(img)

    icon_label.config(image=icon_photo)
    icon_label.image = icon_photo

# -------------------- GUI Setup --------------------
app = tk.Tk()
app.title("Weather App")
app.geometry("420x550")
app.configure(bg="#f0f8ff")

# Title Label
tk.Label(app, text="🌦️ Weather App", font=("Arial", 24, "bold"), bg="#f0f8ff").pack(pady=15)

# City Entry
city_entry = tk.Entry(app, font=("Arial", 16), justify="center", width=25)
city_entry.pack(pady=10)
city_entry.insert(0, "Enter city name")

# Get Weather Button
tk.Button(app, text="Get Weather", font=("Arial", 14), command=get_weather, bg="#4CAF50", fg="white", width=20).pack(pady=10)

# Unit selection
temp_unit = tk.StringVar(value="C")
tk.Radiobutton(app, text="Celsius", variable=temp_unit, value="C", bg="#f0f8ff", font=("Arial", 12)).pack()
tk.Radiobutton(app, text="Fahrenheit", variable=temp_unit, value="F", bg="#f0f8ff", font=("Arial", 12)).pack()

# Icon Label
icon_label = tk.Label(app, bg="#f0f8ff")
icon_label.pack(pady=10)

# Result Label
result_label = tk.Label(app, text="", font=("Arial", 14), justify="left", bg="#f0f8ff")
result_label.pack(pady=10)

# Footer (Remove or edit name as needed)
tk.Label(app, text="Project by [Your Name Here]", font=("Arial", 11), fg="gray", bg="#f0f8ff").pack(side="bottom", pady=10)

# Start the App
app.mainloop()

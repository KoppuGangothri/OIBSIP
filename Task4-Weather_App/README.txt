Weather App - Python Project

Technology Used: Python, Tkinter, OpenWeatherMap API  

Description:
-------------
This is a graphical Weather App built using Python and the Tkinter library. It allows users to enter a city name and view the current weather information, such as temperature, condition, humidity, and wind speed. The data is fetched live from the OpenWeatherMap API.

Features:
----------
- GUI using Tkinter
- Live weather data based on city input
- Temperature unit selection (Celsius/Fahrenheit)
- Weather condition icon display
- Error handling for invalid cities or empty input

Requirements:
--------------
- Python 3.x
- requests
- pillow

Install required libraries:
----------------------------
Run the following command in your terminal:
pip install requests pillow

How to Run:
------------
1. Replace `YOUR_API_KEY` in `weather_app.py` with your actual API key from OpenWeatherMap.
2. Run the script:
   python weather_app.py
3. Enter your city and click "Get Weather".

Note:
-----
You must be connected to the internet to retrieve live data.

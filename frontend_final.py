import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import pandas as pd
import requests
from datetime import datetime

# Load the dataset
df = pd.read_csv("predicted.csv")

def get_aqi():
    selected_date = cal.get_date()
    selected_date_for_query = datetime.strptime(selected_date, "%m/%d/%Y").strftime("%d-%m-%Y")
    selected_data = df[df['Date'] == selected_date_for_query]
    if not selected_data.empty:
        aqi_label.config(text="AQI: " + str(selected_data['AQI'].values[0]))
        aqi_bucket_label.config(text="AQI Bucket: " + selected_data['AQI_Bucket'].values[0])
    else:
        aqi_label.config(text="No data available for selected date")
        aqi_bucket_label.config(text="")


def get_weather():
    try:
        city = city_entry.get()
        selected_date = cal.get_date()
        selected_date_for_request = datetime.strptime(selected_date, "%m/%d/%Y").strftime("%Y-%m-%d")
        api_key = "5c8dc031f9134683ada131004242103"
        weather = fetch_weather(api_key, city, selected_date_for_request)
        if weather:
            weather_label.config(text=f"Weather in {city} on {selected_date}:\n"
                                      f"Description: {weather.get('description')}\n"
                                      f"Temperature: {weather.get('temperature')}°C\n"
                                      f"Humidity: {weather.get('humidity')}%\n"
                                      f"Wind Speed: {weather.get('wind_speed')} km/h\n"
                                      # f"AQI: {weather.get('aqi')}"
                                      )
        else:
            weather_label.config(text="Failed to fetch weather data.")
    except Exception as e:
        print("Error:", e)
        weather_label.config(text="An error occurred while fetching weather data.")


def fetch_weather(api_key, city, selected_date):
    url = f"http://api.weatherapi.com/v1/history.json?key={api_key}&q={city}&dt={selected_date}&aqi=yes"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        try:
            weather_info = {
                "description": data["forecast"]["forecastday"][0]["day"]["condition"]["text"],
                "temperature": data["forecast"]["forecastday"][0]["day"]["avgtemp_c"],
                "humidity": data["forecast"]["forecastday"][0]["day"]["avghumidity"],
                "wind_speed": data["forecast"]["forecastday"][0]["day"]["maxwind_kph"],
                # "aqi": data["forecast"]["forecastday"][0]["day"]["air_quality"]
                
            }
            return weather_info
        except KeyError as e:
            print("Error: Could not fetch weather data. Missing key:", e)
            print("Response data:", data)
            return None
    else:
        print("Error fetching weather data:", data.get("error", {}).get("message", "Unknown error"))
        return None

# Create tkinter window
root = tk.Tk()
root.title("AQI Lookup")
root.minsize(600, 700)
root.resizable()

# Create calendar widget
cal = Calendar(root, selectmode="day", date_pattern="mm/dd/yyyy", foreground='#000000', background='orange')
cal.pack(pady=10)

def grad_date():
    date.config(text="Selected Date is: " + cal.get_date())

# Add Button and Label
ttk.Button(root, text="Get Date", command=grad_date).pack(pady=10)

date = tk.Label(root, text="")
date.pack(pady=20)

# Create button to get AQI
get_aqi_button = ttk.Button(root, text="Get AQI", command=get_aqi)
get_aqi_button.pack(pady=5)

# Labels to display AQI and AQI Bucket
aqi_label = tk.Label(root, text="")
aqi_label.pack(pady=5)
aqi_bucket_label = tk.Label(root, text="")
aqi_bucket_label.pack()


# def grad_date():
#     date.config(text="Selected Date is: " + cal.get_date())

# # Add Button and Label
# tk.Button(root, text="Get Date", command=grad_date).pack(pady=10)

# date = tk.Label(root, text="")
# date.pack(pady=20)

# Create label and entry for city name input
city_label = tk.Label(root, text="Enter city name:")
city_label.pack(side="left", padx=(10, 5))

city_entry = tk.Entry(root, width=30)
city_entry.pack(side="left", padx=(0, 5))

# Create button to fetch weather
get_weather_button = ttk.Button(root, text="Get Weather", command=get_weather)
get_weather_button.pack(side="left", padx=(0, 5))

# Create label to display weather information
weather_label = tk.Label(root, text="Weather Information", justify="left")
weather_label.pack(side="left", padx=(0, 5), pady=0)

root.mainloop()
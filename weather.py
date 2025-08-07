# weather.py
import requests

def get_weather(city: str):
    url = f"http://wttr.in/{city}?format=3"
    response = requests.get(url)
    if response.status_code == 200:
        print(response.text)
    else:
        print("Failed to retrieve weather data.")

if __name__ == "__main__":
    get_weather("Taipei")

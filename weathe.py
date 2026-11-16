import requests 

def get_coordinates(city_name):
    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city_name,
        "count": 1
    }

    response = requests.get(url, params=params, timeout=5)
    response.raise_for_status()

    data = response.json()

    if not data.get("results"):
        return None

    latitude = data["results"][0]["latitude"]
    longitude = data["results"][0]["longitude"]

    return latitude, longitude

def get_weather(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "temperature_m2,windspeed_10m",
    }

    response = requests.get(url, params=params, timeout=5)
    response.raise_for_status()

    data = response.json()

    return data["current"]



import sys 

def main():
    if len(sys.argv) < 2:
        print("Usage: python weathe.py <city_name>")
        return
    city = " ".join(sys.argv[1:])

    try:
        coordinates = get_coordinates(city)

        if not coordinates:
            print(f"Ciudad no encontrada: {city}")
            return

        latitude, longitude = coordinates
        weather = get_weather(latitude, longitude)

        print(f"\nClima en {city.title()}")
        print(f"Temperatura: {weather['temperature_2m']}°C")
        print(f"Velocidad del viento: {weather['wind_speed_10m']} km/h")

    except requests.exceptions.RequestException:
        print("No se pudo cargar los datos intente nuevamente mas tarde.")

    except (KeyError, ValueError):
        print("Algo salio mal mientras cargaba el clima.")

if __name__ == "__main__":
    main()
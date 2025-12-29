import requests
import pandas as pd
from datetime import datetime
import pytz
import os
from dotenv import load_dotenv

load_dotenv()
#OPENWEATHER API KEY
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_airport_info(iata_code):
    try:
        df = pd.read_csv("airports.csv")
        airport = df[df["iata_code"].str.upper() == iata_code.upper()]

        if not airport.empty:
            airport_name = airport.iloc[0]["name"]
            icao_code = airport.iloc[0]["ident"]
            city_name = airport.iloc[0]["municipality"]
            timezone = "UTC"  #Using UTC
            return airport_name, icao_code, city_name, timezone
        else:
            print("Airport not found in database.")
            return None, None, None, "UTC"
    except FileNotFoundError:
        print(" airports.csv file not found.")
        return None, None, None, "UTC"

def get_weather_data(city_name):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        wind_direction = data["wind"].get("deg", None)
        temperature = data["main"]["temp"]
        weather_condition = data["weather"][0]["description"].capitalize()
        return wind_direction, temperature, weather_condition
    else:
        print(f"Error fetching weather data for {city_name}. Please try again.")
        return None, None, None

def get_current_utc_time(timezone):
    try:
        airport_timezone = pytz.timezone(timezone)
        utc_time = datetime.now(airport_timezone).strftime("%Y-%m-%d %H:%M:%S UTC")
        return utc_time
    except:
        return "Unknown Timezone"

def format_runway(heading):
    runway_num = round(heading / 10) % 36
    opp_runway = (runway_num + 18) % 36

    if runway_num == 0:
        runway_num = 36
    if opp_runway == 0:
        opp_runway = 36

    return f"{str(runway_num).zfill(2)}/{str(opp_runway).zfill(2)}"

def get_runways(icao_code):
    try:
        df = pd.read_csv("runways_cleaned.csv")
        df["airport_ident"] = df["airport_ident"].str.upper()
        runways = df[df["airport_ident"] == icao_code][["le_heading_degT", "he_heading_degT"]].values.tolist()

        if not runways:
            print(" No runways found for this airport.")
            return []

        formatted_runways = [(format_runway(r[0]), format_runway(r[1])) for r in runways]
        print("\n✈ Available Runways:")
        for r in formatted_runways:
            print(f"  → Runway {r[0]} / {r[1]}")

        return runways
    except FileNotFoundError:
        print("Runway dataset not found. Ensure runways_cleaned.csv exists.")
        return []

def select_best_runway(wind_direction, runways):
    best_runway = None
    min_diff = float("inf")

    for runway in runways:
        for heading in runway:
            diff = abs(wind_direction - heading)
            if diff > 180:
                diff = 360 - diff

            if diff <= 90 and diff < min_diff:
                min_diff = diff
                best_runway = heading

    if best_runway is None:
        print("⚠ No ideal runway found. Selecting the closest available runway.")
        best_runway = min(runways[0], key=lambda x: abs(wind_direction - x))

    return best_runway

def main():
    airport_code = input("\nEnter airport IATA code (e.g., JFK, LAX, DEL): ").upper()

    airport_name, icao_code, city_name, timezone = get_airport_info(airport_code)
    if not icao_code:
        return

    wind_direction, temperature, weather_condition = get_weather_data(city_name)
    if wind_direction is None:
        print("Could not fetch weather data. Exiting...")
        return

    runways = get_runways(icao_code)
    if not runways:
        print("Runway data not found for this airport.")
        return

    best_runway = select_best_runway(wind_direction, runways)
    best_runway_name = format_runway(best_runway)
    current_time = get_current_utc_time(timezone)

   #the final output shown
    print(f"\nBest Runway Heading: {best_runway}°")
    print(f"Recommended Runway(s): {best_runway_name}")
    print(f"\n{airport_name} ({airport_code} / {icao_code})")
    print(f"UTC Time: {current_time}")
    print(f"🌤 {wind_direction}° | {temperature}°C | {weather_condition}")


if __name__ == "__main__":
    main()

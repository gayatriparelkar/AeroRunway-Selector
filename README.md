# AeroRunway Selector

#### Video Demo:  <https://youtu.be/PIBYzaWxVYc?si=8dYOi6PPXgxVMGeY>
#### Description:
### **AI-Assisted Runway Selector for Pilots**

The **AeroRunway Selector** is a Python-based tool designed to help pilots select the safest and most suitable runway for takeoff and landing by analyzing real-time weather data. The project integrates the **OpenWeather API** to fetch live weather conditions, including **wind direction, temperature, and overall weather status**. Additionally, it uses datasets containing airport and runway information to determine available runways at a given airport.

The system works by taking an **IATA airport code** as input, fetching corresponding airport details, and retrieving the latest weather conditions for that location. It then compares the **wind direction** with the available **runway headings** and selects the runway that provides the best alignment, minimizing crosswind effects. If no optimal runway is found, the tool suggests the closest available option.

This project enhances **flight safety and decision-making** by automating the runway selection process using **real-time data and logical calculations**. The output includes **recommended runway(s), best heading, weather conditions, and UTC time**, providing pilots with critical information before takeoff. Future improvements may include integrating additional aviation data sources, GUI enhancements, and support for more weather factors such as visibility and precipitation.

## 🛠 Features
- Fetches real-time wind data using OpenWeather API.
- Reads airport runways from a CSV dataset.
- Determines the best runway aligned with wind direction.

## 🚀How to Run
1. Clone the repository or download the files.
2. Install dependencies: `pip install -r requirements.txt`
3. Set your **OpenWeather API Key** in environment variables:


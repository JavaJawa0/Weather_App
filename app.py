import streamlit as st
import requests
from streamlit_js_eval import get_geolocation


class WeatherAPI:
    def __init__(self, api_key, units="metric"):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.units = units

    def fetch_by_city(self, city):
        params = {"q": city, "appid": self.api_key, "units": self.units}
        return self._get_response(params)

    def fetch_by_coords(self, lat, lon):
        params = {"lat": lat, "lon": lon, "appid": self.api_key, "units": self.units}
        return self._get_response(params)

    def _get_response(self, params):
        try:
            response = requests.get(self.base_url, params=params)
            if response.status_code == 404:
                st.error("City not found. Try again!")
                return None
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Connection error: {e}")
            return None


class WeatherUI:
    def __init__(self):
        st.set_page_config(page_title="SkyCast Pro", page_icon="🌤️")
        st.title("🌤️ SkyCast Pro")

    def render_controls(self):
        # Create two columns: one for typing, one for the GPS button
        col1, col2 = st.columns([3, 1])

        with col1:
            city_input = st.text_input("Enter city name:", placeholder="e.g. New York")

        with col2:
            st.write("##")  # Add spacing to align with textbox
            gps_button = st.button("📍 Use GPS")

        return city_input, gps_button

    def display_weather(self, data):
        if not data: return

        # UI cards and layout
        with st.container(border=True):
            name = data.get('name')
            temp = data['main']['temp']
            desc = data['weather'][0]['description'].capitalize()
            icon = data['weather'][0]['icon']
            humidity = data['main']['humidity']

            st.header(f"Weather in {name}")
            c1, c2, c3 = st.columns(3)
            c1.metric("Temp", f"{temp}°")
            c2.write(f"**Condition** \n{desc}")
            c2.image(f"http://openweathermap.org/img/wn/{icon}@2x.png")
            c3.metric("Humidity", f"{humidity}%")


def main():
    ui = WeatherUI()

    # Check for secrets
    if "OPENWEATHER_API_KEY" not in st.secrets:
        st.error("Missing API Key in Secrets!")
        return

    api = WeatherAPI(st.secrets["OPENWEATHER_API_KEY"])
    city_name, use_gps = ui.render_controls()

    weather_data = None

    # Logic Priority:
    # 1. If user clicks GPS button
    if use_gps:
        with st.spinner("Acquiring GPS..."):
            loc = get_geolocation()
            if loc:
                lat = loc['coords']['latitude']
                lon = loc['coords']['longitude']
                weather_data = api.fetch_by_coords(lat, lon)
            else:
                st.warning("Please allow location access in your browser.")

    # 2. If user typed a city
    elif city_name:
        weather_data = api.fetch_by_city(city_name)

    # 3. Show the results
    if weather_data:
        ui.display_weather(weather_data)


if __name__ == "__main__":
    main()
import streamlit as st
import requests
from streamlit_js_eval import get_geolocation


class WeatherAPI:
    """Handles communication with the OpenWeatherMap API."""

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
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error: {e}")
            return None


class WeatherUI:
    """Handles the Streamlit interface."""

    def __init__(self):
        st.set_page_config(page_title="SkyCast Secure", page_icon="🌤️")
        st.title("🌤️ SkyCast Weather")

    def render_sidebar(self):
        st.sidebar.header("Search")
        city = st.sidebar.text_input("Enter city:")
        unit_label = st.sidebar.selectbox("Units", ["Metric (°C)", "Imperial (°F)"])
        unit_type = "metric" if "Metric" in unit_label else "imperial"
        return city, unit_type

    def display_weather(self, data):
        if not data: return

        name = data.get('name')
        temp = data['main']['temp']
        desc = data['weather'][0]['description'].capitalize()
        icon = data['weather'][0]['icon']

        st.subheader(f"Weather in {name}")
        col1, col2 = st.columns(2)
        col1.metric("Temperature", f"{temp}°")
        col1.write(f"**Conditions:** {desc}")
        col2.image(f"http://openweathermap.org/img/wn/{icon}@2x.png")


def main():
    ui = WeatherUI()
    search_city, units = ui.render_sidebar()

    # SECURE KEY ACCESS
    # This looks for 'OPENWEATHER_API_KEY' in your secrets
    try:
        api_key = st.secrets["OPENWEATHER_API_KEY"]
        weather_service = WeatherAPI(api_key, units)
    except KeyError:
        st.error("Please configure the API Key in secrets!")
        return

    if search_city:
        data = weather_service.fetch_by_city(search_city)
    else:
        st.info("No city entered. Checking GPS...")
        loc = get_geolocation()
        if loc:
            lat = loc['coords']['latitude']
            lon = loc['coords']['longitude']
            data = weather_service.fetch_by_coords(lat, lon)
        else:
            data = None

    if data:
        ui.display_weather(data)


if __name__ == "__main__":
    main()
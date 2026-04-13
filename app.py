import streamlit as st
import requests
from streamlit_js_eval import get_geolocation


class WeatherAPI:
    # ... (Keep your existing WeatherAPI class code here) ...
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
        except:
            return None


class WeatherUI:
    def __init__(self):
        st.set_page_config(page_title="SkyCast Reactive", page_icon="🌤️")

    def set_bg(self, condition):
        """Injects custom CSS to change the background based on weather."""
        # Map conditions to CSS gradients
        bg_styles = {
            "Clear": "linear-gradient(to right, #4facfe 0%, #00f2fe 100%)",  # Bright Blue
            "Clouds": "linear-gradient(to right, #bdc3c7 0%, #2c3e50 100%)",  # Grey/Cloudy
            "Rain": "linear-gradient(to right, #4b6cb7 0%, #182848 100%)",  # Dark Blue/Rain
            "Snow": "linear-gradient(to right, #e6e9f0 0%, #eef1f5 100%)",  # White/Ice
            "Thunderstorm": "linear-gradient(to right, #0f0c29, #302b63, #24243e)",  # Dark Purple
            "Drizzle": "linear-gradient(to right, #89f7fe 0%, #66a6ff 100%)",  # Light Teal
        }

        # Default to a neutral color if condition is unknown
        selected_bg = bg_styles.get(condition, "linear-gradient(#ffffff, #ffffff)")

        # Inject CSS into Streamlit
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: {selected_bg};
                transition: background 0.5s ease;
            }}
            /* Make text readable on dark backgrounds */
            h1, h2, h3, p, span {{
                color: white !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    def render_controls(self):
        st.title("🌤️ SkyCast Reactive")
        col1, col2 = st.columns([3, 1])
        with col1:
            city_input = st.text_input("Enter city name:", key="city_search")
        with col2:
            st.write("##")
            gps_button = st.button("📍 Use GPS")
        return city_input, gps_button

    def display_weather(self, data):
        if not data: return

        condition = data['weather'][0]['main']  # This will be "Clear", "Clouds", etc.
        self.set_bg(condition)  # Call the background changer!

        with st.container(border=True):
            name = data.get('name')
            temp = data['main']['temp']
            desc = data['weather'][0]['description'].capitalize()
            icon = data['weather'][0]['icon']

            st.header(f"Weather in {name}")
            c1, c2 = st.columns(2)
            c1.metric("Temperature", f"{temp}°")
            c1.write(f"**Condition:** {desc}")
            c2.image(f"http://openweathermap.org/img/wn/{icon}@4x.png")


# --- Main Flow ---
def main():
    ui = WeatherUI()

    if "OPENWEATHER_API_KEY" not in st.secrets:
        st.error("Check Secrets!")
        return

    api = WeatherAPI(st.secrets["OPENWEATHER_API_KEY"])
    city_input, gps_clicked = ui.render_controls()
    location = get_geolocation()
    weather_data = None

    if gps_clicked and location:
        weather_data = api.fetch_by_coords(location['coords']['latitude'], location['coords']['longitude'])
    elif city_input:
        weather_data = api.fetch_by_city(city_input)

    if weather_data:
        ui.display_weather(weather_data)


if __name__ == "__main__":
    main()
# SkyCast Pro: Reactive Weather Dashboard

A professional, object-oriented weather application built with Python and Streamlit. This app features real-time weather data fetching, browser-based geolocation, and a reactive UI that changes its theme based on current weather conditions.

---

## Project Architecture

```text
weather-app/
│
├── .streamlit/
│   └── secrets.toml      # Local API keys (Hidden)
├── app.py                # Main Application (OOP Logic)
├── requirements.txt      # List of dependencies
├── .gitignore            # Prevents secrets from being pushed
└── README.md             # Project documentation
```

---

## Prerequisites

Before running this project, ensure you have the following installed on your system:
* **Python 3.8+** - Required to run the Streamlit application.
* **OpenWeatherMap Account** - Required to obtain a free API key for weather data.

---

## Local Installation and Execution

### Step 1: Clone and Install Dependencies
1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   ```
2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Step 2: Configure Secrets
1. Create a `.streamlit` folder in the project root:
   ```bash
   mkdir .streamlit
   ```
2. Inside the `.streamlit` folder, create a `secrets.toml` file and add your API key:
   ```toml
   OPENWEATHER_API_KEY = "your_actual_api_key_here"
   ```
   *Note: This file is ignored by Git to keep your credentials secure.*

### Step 3: Run the Application
1. Launch the Streamlit application:
   ```bash
   streamlit run app.py
   ```
2. Open the local URL provided in your terminal (typically `http://localhost:8501`) to view the dashboard.

---

## Deployment on Streamlit Community Cloud

To deploy this application publicly using Streamlit Community Cloud:

1. Push your repository to **GitHub**, ensuring that `app.py` and `requirements.txt` are included (do not push your `.streamlit/secrets.toml` file).
2. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
3. Click **Create app** and configure the settings:
   * **Repository:** Select your repository.
   * **Branch:** `main`
   * **Main file path:** `app.py`
4. Go to **Settings > Secrets** in your Streamlit dashboard and add your API key:
   ```toml
   OPENWEATHER_API_KEY = "your_actual_api_key_here"
   ```
5. Click **Deploy**.

import streamlit as st
import pymysql
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASS", ""),
    "database": os.getenv("DB_NAME", "hotel")
}

def calculate_price(base_price, weather_main):
    weather_main = weather_main.lower()
    if weather_main in ["rain", "thunderstorm"]:
        return base_price * 1.2  
    elif weather_main in ["clouds", "mist"]:
        return base_price * 1.1  
    else:
        return base_price     

@st.cache_data
def load_data():
    conn = pymysql.connect(**DB_CONFIG)
    query = """
        SELECT datetime, temp, temp_min, temp_max, humidity, 
               weather_main, weather_description, weather_icon
        FROM weather_forecast
        ORDER BY datetime ASC
    """
    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        return df

    df["datetime"] = pd.to_datetime(df["datetime"])
    df["date"] = df["datetime"].dt.date
    return df

st.set_page_config(page_title="Nairobi Weather Dashboard", layout="wide")
st.title("🌤️ Nairobi Weather & Dynamic Hotel Pricing Dashboard")

df = load_data()

if df.empty:
    st.warning("⚠️ No forecast data found in the database. Please run your fetch script first.")
else:
    daily = (
        df.groupby("date")
        .agg({
            "temp_min": "min",
            "temp_max": "max",
            "humidity": "mean",
            "weather_main": "first",
            "weather_description": "first",
            "weather_icon": "first"
        })
        .reset_index()
    )

    base_price = 1000  
    daily["price"] = daily["weather_main"].apply(lambda w: calculate_price(base_price, w))
    today_price = daily.loc[daily["date"] == daily["date"].min(), "price"].iloc[0]
    st.markdown(
        f"""
        <div style="background-color:#f0f8ff;padding:15px;border-radius:10px;
                    text-align:center;font-size:20px;font-weight:bold;
                    border:2px solid #1e90ff;">
            🏨 Today's Booking Price: 💲 {today_price:.2f}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("🌍 Daily Weather & 🏨 Hotel Pricing")
    cols = st.columns(4) 
    for i, row in daily.iterrows():
        with cols[i % 4]:
            st.markdown(f"**{row['date']}**")
            icon_url = f"http://openweathermap.org/img/wn/{row['weather_icon']}@2x.png"
            st.image(icon_url, width=80)
            st.caption(f"{row['weather_description'].capitalize()}")
            st.write(f"🌡️ {row['temp_min']}°C - {row['temp_max']}°C")
            st.write(f"💧 {round(row['humidity'],1)}% humidity")
            st.success(f"💲 Price: {row['price']:.2f}")
    st.subheader("📊 Daily Temperature Forecast")
    st.bar_chart(
        daily.set_index("date")[["temp_min", "temp_max"]]
    )

    st.subheader("💧 Daily Humidity Forecast")
    st.line_chart(
        daily.set_index("date")[["humidity"]]
    )
    st.subheader("🔎 Raw Forecast Data")
    st.dataframe(df)

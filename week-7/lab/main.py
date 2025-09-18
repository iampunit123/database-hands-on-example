import requests
import os
import pymysql
from dotenv import load_dotenv 

load_dotenv()

API_KEY = os.getenv("API_KEY")
CITY = "Nairobi"
BASE_URL = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASS", ""),
    "database": os.getenv("DB_NAME", "weatherDB"),
    "cursorclass": pymysql.cursors.DictCursor
}

def create_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_forecast (
            id INT AUTO_INCREMENT PRIMARY KEY,
            city_id INT,
            city_name VARCHAR(100),
            country VARCHAR(10),
            datetime DATETIME,
            temp FLOAT,
            temp_min FLOAT,
            temp_max FLOAT,
            feels_like FLOAT,
            pressure INT,
            humidity INT,
            weather_main VARCHAR(50),
            weather_description VARCHAR(100),
            weather_icon VARCHAR(10),
            clouds INT,
            rain FLOAT,
            UNIQUE KEY uniq_forecast (city_id, datetime)
        )
    """)

def weather_data():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        data = response.json()
        forecasts = []
        for entry in data.get("list", []):
            forecasts.append({
                "city_id": data["city"]["id"],
                "city_name": data["city"]["name"],
                "country": data["city"]["country"],
                "datetime": entry["dt_txt"],
                "temp": entry["main"]["temp"],
                "temp_min": entry["main"]["temp_min"],
                "temp_max": entry["main"]["temp_max"],
                "feels_like": entry["main"]["feels_like"],
                "pressure": entry["main"]["pressure"],
                "humidity": entry["main"]["humidity"],
                "weather_main": entry["weather"][0]["main"],
                "weather_description": entry["weather"][0]["description"],
                "weather_icon": entry["weather"][0]["icon"],
                "clouds": entry["clouds"]["all"],
                "rain": entry.get("rain", {}).get("3h", 0)
            })
        return forecasts
    else:
        print("Error fetching data:", response.status_code)
        return []

def save_to_mysql(forecasts):
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    create_table(cursor)

    sql = """
        INSERT INTO weather_forecast (
            city_id, city_name, country, datetime, temp, temp_min, temp_max,
            feels_like, pressure, humidity, weather_main, weather_description,
            weather_icon, clouds, rain
        ) VALUES (
            %(city_id)s, %(city_name)s, %(country)s, %(datetime)s, %(temp)s, %(temp_min)s, %(temp_max)s,
            %(feels_like)s, %(pressure)s, %(humidity)s, %(weather_main)s, %(weather_description)s,
            %(weather_icon)s, %(clouds)s, %(rain)s
        )
        ON DUPLICATE KEY UPDATE
            temp=VALUES(temp),
            temp_min=VALUES(temp_min),
            temp_max=VALUES(temp_max),
            feels_like=VALUES(feels_like),
            pressure=VALUES(pressure),
            humidity=VALUES(humidity),
            weather_main=VALUES(weather_main),
            weather_description=VALUES(weather_description),
            weather_icon=VALUES(weather_icon),
            clouds=VALUES(clouds),
            rain=VALUES(rain)
    """

    cursor.executemany(sql, forecasts)
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Inserted {len(forecasts)} records into weather_forecast table.")

if __name__ == "__main__":
    forecasts = weather_data()
    if forecasts:
        save_to_mysql(forecasts)

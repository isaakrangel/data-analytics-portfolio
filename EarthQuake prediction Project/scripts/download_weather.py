from pathlib import Path
import requests
import pandas as pd
import time

from config.config import START_DATE, END_DATE

# =========================================
# LOAD EARTHQUAKE DATA
# =========================================

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw"

INPUT_FILE = RAW_PATH / "earthquakes_2025.csv"
OUTPUT_FILE = RAW_PATH / "weather_2025.csv"

df = pd.read_csv(INPUT_FILE)

# =========================================
# OPTIONAL: FULL DATASET (18K ROWS)
# =========================================

# No head() -> full run
df = df.head(200)

# =========================================
# WEATHER COLLECTION
# =========================================

results = []

print(f"Starting weather extraction for {len(df)} records...")

for i, row in df.iterrows():

    lat = row["latitude"]
    lon = row["longitude"]
    date = pd.to_datetime(row["time"]).strftime("%Y-%m-%d")

    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={lat}"
        f"&longitude={lon}"
        f"&start_date={date}"
        f"&end_date={date}"
        f"&hourly=temperature_2m"
    )

    temperature = None

    # Retry logic (important for stability)
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            if "hourly" in data and "temperature_2m" in data["hourly"]:
                temps = data["hourly"]["temperature_2m"]
                if len(temps) > 0:
                    temperature = temps[0]

            break  # success → exit retry loop

        except Exception as e:
            print(f"Retry {attempt+1}/3 failed at index {i}: {e}")
            time.sleep(1)

    results.append({
        "time": row["time"],
        "latitude": lat,
        "longitude": lon,
        "temperature": temperature
    })

    # Progress log
    if i % 100 == 0:
        print(f"Processed {i}/{len(df)}")

    # Prevent API overload
    time.sleep(0.2)

# =========================================
# SAVE OUTPUT
# =========================================

weather_df = pd.DataFrame(results)
weather_df.to_csv(OUTPUT_FILE, index=False)

print("Weather extraction completed!")
print(f"Saved at: {OUTPUT_FILE}")
print(weather_df.head())
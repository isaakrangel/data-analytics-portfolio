from pathlib import Path
import requests
import pandas as pd

# Import project configuration
from config.config import START_DATE, END_DATE, MIN_MAGNITUDE

# =========================================
# PROJECT PATHS
# =========================================

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw"
RAW_PATH.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = RAW_PATH / "earthquakes_2025.csv"

# =========================================
# USGS API REQUEST
# =========================================

url = (
    "https://earthquake.usgs.gov/fdsnws/event/1/query"
    f"?format=geojson"
    f"&starttime={START_DATE}"
    f"&endtime={END_DATE}"
    f"&minmagnitude={MIN_MAGNITUDE}"
    f"&limit=20000"
)

print("Downloading earthquake data...")

response = requests.get(url, timeout=30)
response.raise_for_status()

data = response.json()

print(f"Total earthquakes retrieved: {len(data['features'])}")

# =========================================
# PARSE JSON INTO DATAFRAME
# =========================================

records = []

for event in data["features"]:
    properties = event["properties"]
    geometry = event["geometry"]["coordinates"]

    records.append({
        "time": properties["time"],
        "place": properties["place"],
        "magnitude": properties["mag"],
        "depth_km": geometry[2],
        "longitude": geometry[0],
        "latitude": geometry[1],
        "tsunami": properties["tsunami"],
        "significance": properties["sig"]
    })

df = pd.DataFrame(records)

# Convert timestamp to datetime
df["time"] = pd.to_datetime(df["time"], unit="ms")

# =========================================
# SAVE DATA TO CSV
# =========================================

df.to_csv(OUTPUT_FILE, index=False)

print("Download completed successfully!")
print(f"File saved at: {OUTPUT_FILE}")
print(df.head())
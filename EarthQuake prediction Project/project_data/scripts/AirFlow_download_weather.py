from pathlib import Path
import requests
import pandas as pd
import time



# =========================================
# PATHS
# =========================================

ROOT = Path(__file__).resolve().parents[1]

PROCESSED_PATH = (
    ROOT /
    "data" /
    "processed"
)

PROCESSED_PATH.mkdir(
    parents=True,
    exist_ok=True
)



# =========================================
# WEATHER VARIABLES
# =========================================

WEATHER_VARIABLES = (
    "temperature_2m,"
    "surface_pressure,"
    "precipitation,"
    "soil_temperature_0_to_7cm,"
    "soil_temperature_100_to_255cm,"
    "soil_moisture_0_to_7cm,"
    "soil_moisture_100_to_255cm"
)



# =========================================
# DOWNLOAD FUNCTION
# =========================================

def download_weather(
    input_file,
    save_interval=100
):

    start_time = time.time()

    input_file = Path(input_file)

    start_date = (
        input_file
        .stem
        .replace(
            "weather_requests_",
            ""
        )
    )

    output_file = (
        PROCESSED_PATH /
        f"weather_{start_date}.csv"
    )

    print(
        "\n========== WEATHER DOWNLOAD ==========",
        flush=True
    )

    print(
        f"Input file: {input_file}",
        flush=True
    )

    requests_df = pd.read_csv(input_file)

    print(
        f"Total weather requests: {len(requests_df)}",
        flush=True
    )



    # =========================================
    # CHECK PREVIOUS RESULTS
    # =========================================

    results = []

    if output_file.exists():

        existing = pd.read_csv(output_file)

        results = existing.to_dict("records")

        processed_keys = set(
            zip(
                existing["date"],
                existing["latitude"],
                existing["longitude"]
            )
        )

        print(
            f"Existing records: {len(existing)}",
            flush=True
        )

    else:

        processed_keys = set()

        print(
            "No previous output found.",
            flush=True
        )



    print(
        f"Remaining requests: {len(requests_df)-len(processed_keys)}",
        flush=True
    )



    # =========================================
    # DOWNLOAD LOOP
    # =========================================

    downloaded = 0

    for index, row in requests_df.iterrows():

        if index % 10 == 0:

            print(
                f"Checking request {index+1}/{len(requests_df)}",
                flush=True
            )

        key = (
            str(row["date"]),
            row["latitude"],
            row["longitude"]
        )

        if key in processed_keys:
            continue

        date = row["date"]
        lat = row["latitude"]
        lon = row["longitude"]

        url = (
            "https://archive-api.open-meteo.com/v1/archive"
            f"?latitude={lat}"
            f"&longitude={lon}"
            f"&start_date={date}"
            f"&end_date={date}"
            f"&hourly={WEATHER_VARIABLES}"
        )

        try:

            response = requests.get(
                url,
                timeout=30
            )

            response.raise_for_status()

            hourly = response.json().get(
                "hourly",
                {}
            )

            record = {

                "date": date,
                "latitude": lat,
                "longitude": lon,

                "temperature_2m":
                    hourly.get("temperature_2m",[None])[0],

                "surface_pressure":
                    hourly.get("surface_pressure",[None])[0],

                "precipitation":
                    hourly.get("precipitation",[None])[0],

                "soil_temperature_0_7cm":
                    hourly.get("soil_temperature_0_to_7cm",[None])[0],

                "soil_temperature_100_255cm":
                    hourly.get("soil_temperature_100_to_255cm",[None])[0],

                "soil_moisture_0_7cm":
                    hourly.get("soil_moisture_0_to_7cm",[None])[0],

                "soil_moisture_100_255cm":
                    hourly.get("soil_moisture_100_to_255cm",[None])[0]

            }

            results.append(record)
            processed_keys.add(key)

            downloaded += 1

        except Exception as e:

            print(
                f"ERROR -> {date} ({lat},{lon}) : {e}",
                flush=True
            )



        if downloaded > 0 and downloaded % 10 == 0:

            print(
                f"Downloaded {downloaded} new weather records.",
                flush=True
            )



        if downloaded > 0 and downloaded % save_interval == 0:

            pd.DataFrame(results).to_csv(
                output_file,
                index=False
            )

            print(
                f"Checkpoint saved ({len(results)} total records).",
                flush=True
            )

        time.sleep(0.2)



    # =========================================
    # FINAL SAVE
    # =========================================

    weather_df = pd.DataFrame(results)

    weather_df.drop_duplicates(
        subset=[
            "date",
            "latitude",
            "longitude"
        ],
        inplace=True
    )

    weather_df.to_csv(
        output_file,
        index=False
    )

    elapsed = time.time() - start_time

    print(
        "\n========== COMPLETED ==========",
        flush=True
    )

    print(
        f"Final dataset: {weather_df.shape}",
        flush=True
    )

    print(
        f"Saved to: {output_file}",
        flush=True
    )

    print(
        f"Execution time: {elapsed/60:.2f} minutes",
        flush=True
    )

    return output_file



if __name__ == "__main__":

    latest_file = max(
        PROCESSED_PATH.glob("weather_requests_*.csv"),
        key=lambda f: f.stat().st_mtime
    )

    download_weather(latest_file)
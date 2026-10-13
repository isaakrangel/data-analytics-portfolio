from pathlib import Path
import pandas as pd
import argparse


# =========================================
# PROJECT PATHS
# =========================================

ROOT = Path(__file__).resolve().parents[1]


RAW_PATH = ROOT / "data" / "raw"
PROCESSED_PATH = ROOT / "data" / "processed"

PROCESSED_PATH.mkdir(
    parents=True,
    exist_ok=True
)



# =========================================
# MERGE FUNCTION
# =========================================

def merge_earthquake_weather(
        earthquake_file,
        weather_file
):


    earthquake_path = RAW_PATH / earthquake_file
    weather_path = PROCESSED_PATH / weather_file


    output_file = (
        PROCESSED_PATH /
        "earthquakes_weather_merged.csv"
    )


    # =====================================
    # LOAD DATA
    # =====================================

    print("Loading earthquake data...")


    earthquakes = pd.read_csv(
        earthquake_path
    )


    print(
        f"Earthquake dataset: {earthquakes.shape}"
    )



    print("Loading weather data...")


    weather = pd.read_csv(
        weather_path
    )


    print(
        f"Weather dataset: {weather.shape}"
    )



    # =====================================
    # PREPARE EARTHQUAKE DATA
    # =====================================


    earthquakes["time"] = pd.to_datetime(
        earthquakes["time"],
        format="ISO8601",
        utc=True
    )


    earthquakes["date"] = (
        earthquakes["time"]
        .dt.date
        .astype(str)
    )


    # IMPORTANT:
    # Weather requests were generated using
    # coordinates rounded to 2 decimals.
    # Apply the same transformation here.

    earthquakes["latitude"] = (
        earthquakes["latitude"]
        .round(2)
    )


    earthquakes["longitude"] = (
        earthquakes["longitude"]
        .round(2)
    )



    # =====================================
    # PREPARE WEATHER DATA
    # =====================================


    weather["date"] = (
        weather["date"]
        .astype(str)
    )


    weather["latitude"] = (
        weather["latitude"]
        .round(2)
    )


    weather["longitude"] = (
        weather["longitude"]
        .round(2)
    )



    # =====================================
    # MERGE
    # =====================================


    print("Merging datasets...")


    merged = earthquakes.merge(

        weather,

        how="left",

        on=[
            "date",
            "latitude",
            "longitude"
        ]

    )



    print(
        f"Merged dataset: {merged.shape}"
    )



    # =====================================
    # CHECK MISSING WEATHER DATA
    # =====================================


    weather_columns = [
        col for col in weather.columns
        if col not in [
            "date",
            "latitude",
            "longitude"
        ]
    ]


    missing_weather = (
        merged[weather_columns]
        .isna()
        .all(axis=1)
        .sum()
    )


    print(
        f"Records without weather data: {missing_weather}"
    )



    # =====================================
    # REMOVE DUPLICATES
    # =====================================


    before = len(merged)


    merged.drop_duplicates(
        inplace=True
    )


    print(
        f"Duplicates removed: {before - len(merged)}"
    )



    # =====================================
    # SAVE
    # =====================================


    merged.to_csv(
        output_file,
        index=False
    )


    print(
        f"Saved at: {output_file}"
    )


    return output_file




# =========================================
# AIRFLOW ENTRY POINT
# =========================================

if __name__ == "__main__":


    parser = argparse.ArgumentParser(
        description="Merge earthquake and weather datasets"
    )


    parser.add_argument(
        "--earthquake_file",
        required=True,
        help="Earthquake CSV filename"
    )


    parser.add_argument(
        "--weather_file",
        required=True,
        help="Weather CSV filename"
    )


    args = parser.parse_args()



    merge_earthquake_weather(

        args.earthquake_file,

        args.weather_file

    )
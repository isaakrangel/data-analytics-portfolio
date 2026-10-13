from pathlib import Path
import pandas as pd


# =========================================
# PROJECT PATHS
# =========================================

ROOT = Path(__file__).resolve().parents[1]

PROCESSED_PATH = ROOT / "data" / "processed"

PROCESSED_PATH.mkdir(
    parents=True,
    exist_ok=True
)



# =========================================
# CREATE WEATHER REQUEST FUNCTION
# =========================================

def create_weather_requests(input_file):


    input_file = Path(input_file)


    print("Loading earthquake dataset...")
    print(f"Input file: {input_file}")


    df = pd.read_csv(input_file)


    print(
        f"Original dataset: {df.shape}"
    )


    # =========================================
    # PREPARE DATE
    # =========================================


    df["time"] = pd.to_datetime(
        df["time"],
        format="ISO8601",
        utc=True
    )


    df["date"] = df["time"].dt.date



    # =========================================
    # CREATE WEATHER REQUESTS
    # =========================================


    weather_requests = df[
        [
            "date",
            "latitude",
            "longitude"
        ]
    ].copy()



    # Reduce repeated API requests
    weather_requests["latitude"] = (
        weather_requests["latitude"]
        .round(2)
    )


    weather_requests["longitude"] = (
        weather_requests["longitude"]
        .round(2)
    )



    before = len(weather_requests)



    weather_requests.drop_duplicates(
        subset=[
            "date",
            "latitude",
            "longitude"
        ],
        inplace=True
    )


    removed = before - len(weather_requests)


    print(
        f"Duplicate requests removed: {removed}"
    )



    weather_requests.sort_values(
        by=[
            "date",
            "latitude",
            "longitude"
        ],
        inplace=True
    )


    weather_requests.reset_index(
        drop=True,
        inplace=True
    )


    print(
        f"Unique weather requests: {weather_requests.shape}"
    )



    # =========================================
    # SAVE FILE
    # =========================================


    start_date = weather_requests["date"].min()
    end_date = weather_requests["date"].max()


    output_file = (
        PROCESSED_PATH /
        f"weather_requests_{start_date}_{end_date}.csv"
    )



    weather_requests.to_csv(
        output_file,
        index=False
    )



    print(
        f"Saved file: {output_file}"
    )


    return output_file

if __name__ == "__main__":

    RAW_PATH = ROOT / "data" / "raw"

    earthquake_files = list(
        RAW_PATH.glob("earthquakes_*.csv")
    )

    if not earthquake_files:
        raise FileNotFoundError(
            "No earthquake CSV files found"
        )

    latest_file = max(
        earthquake_files,
        key=lambda x: x.stat().st_mtime
    )

    print(
        f"Using earthquake file: {latest_file}"
    )

    create_weather_requests(latest_file)






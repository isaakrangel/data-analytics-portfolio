from pathlib import Path
from io import StringIO
import requests
import pandas as pd
import argparse


ROOT = Path(__file__).resolve().parents[1]

RAW_PATH = ROOT / "data" / "raw"
RAW_PATH.mkdir(parents=True, exist_ok=True)



def download_earthquakes(
    start_date,
    end_date,
    min_magnitude=2.5
):

    output_file = (
        RAW_PATH /
        f"earthquakes_{start_date}_{end_date}.csv"
    )


    url = (
        "https://earthquake.usgs.gov/fdsnws/event/1/query"
        "?format=csv"
        f"&starttime={start_date}"
        f"&endtime={end_date}"
        f"&minmagnitude={min_magnitude}"
    )


    print("Downloading earthquake data...")
    print(url)


    response = requests.get(
        url,
        timeout=60
    )

    response.raise_for_status()


    df = pd.read_csv(
        StringIO(response.text)
    )


    if df.empty:
        print("No earthquakes found")
        return None


    print(
        f"Total earthquakes retrieved: {len(df)}"
    )


    df.to_csv(
        output_file,
        index=False
    )


    print(
        f"File saved at: {output_file}"
    )


    return output_file



if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Download USGS earthquake data"
    )


    parser.add_argument(
        "--start_date",
        required=True
    )


    parser.add_argument(
        "--end_date",
        required=True
    )


    args = parser.parse_args()


    download_earthquakes(
        args.start_date,
        args.end_date
    )
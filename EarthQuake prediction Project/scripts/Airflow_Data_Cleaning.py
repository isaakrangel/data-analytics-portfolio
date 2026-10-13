from pathlib import Path
import pandas as pd
from sklearn.impute import SimpleImputer


# =========================================
# PROJECT PATHS
# =========================================

ROOT = Path(__file__).resolve().parents[1]

PROCESSED_PATH = ROOT / "data" / "processed"
CLEANED_PATH = ROOT / "data" / "cleaned"

CLEANED_PATH.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================
# DATA CLEANING FUNCTION
# =========================================

def clean_dataset(input_file):

    input_file = PROCESSED_PATH / input_file

    output_file = (
        CLEANED_PATH /
        f"{input_file.stem}_cleaned.csv"
    )

    print("Loading merged dataset...")

    df = pd.read_csv(input_file)

    print(f"Original dataset: {df.shape}")

    # =====================================
    # KEEP ONLY EARTHQUAKES
    # =====================================

    before = len(df)

    df = df[df["type"] == "earthquake"].copy()

    removed = before - len(df)

    print(f"Removed non-earthquake events: {removed}")

    # =====================================
    # IMPUTE MISSING VALUES
    # =====================================

    columns = [
        "nst",
        "rms",
        "gap",
        "dmin",
        "horizontalError",
        "depthError",
        "magError",
        "magNst"
    ]

    existing_columns = [
        col for col in columns
        if col in df.columns
    ]

    imputer = SimpleImputer(
        strategy="median"
    )

    df[existing_columns] = imputer.fit_transform(
        df[existing_columns]
    )

    # =====================================
    # SAVE
    # =====================================

    df.to_csv(
        output_file,
        index=False
    )

    print(f"Clean dataset shape: {df.shape}")
    print(f"Saved at: {output_file}")

    return output_file


# =========================================
# AIRFLOW ENTRY POINT
# =========================================

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input_file",
        required=True
    )

    args = parser.parse_args()

    clean_dataset(
        args.input_file
    )
from pathlib import Path
import pandas as pd

# =========================================
# PATHS
# =========================================

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw"
CLEAN_PATH = ROOT / "data" / "cleaned"
CLEAN_PATH.mkdir(parents=True, exist_ok=True)

EQ_FILE = RAW_PATH / "earthquakes_2025.csv"
WX_FILE = RAW_PATH / "weather_2025.csv"

OUTPUT_FILE = CLEAN_PATH / "merged_dataset.csv"

# =========================================
# LOAD DATA
# =========================================

eq = pd.read_csv(EQ_FILE)
wx = pd.read_csv(WX_FILE)

print("Earthquakes shape:", eq.shape)
print("Weather shape:", wx.shape)

# =========================================
# ALIGN DATASETS (TEST VERSION)
# =========================================

# Ensure same length (safety check)
min_len = min(len(eq), len(wx))

eq = eq.iloc[:min_len].reset_index(drop=True)
wx = wx.iloc[:min_len].reset_index(drop=True)

# =========================================
# MERGE DATA
# =========================================

merged = pd.DataFrame({
    "time": eq["time"],
    "latitude": eq["latitude"],
    "longitude": eq["longitude"],
    "magnitude": eq["magnitude"],
    "depth_km": eq["depth_km"],
    "temperature": wx["temperature"]
})

# =========================================
# SAVE OUTPUT
# =========================================

merged.to_csv(OUTPUT_FILE, index=False)

print("Merge completed successfully!")
print(f"Saved at: {OUTPUT_FILE}")
print(merged.head())
print("Final shape:", merged.shape)
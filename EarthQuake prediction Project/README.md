# Earthquake Analytics Project

## Overview
This project analyzes global earthquake events and combines them with weather data (temperature) using public APIs. The goal is to build an end-to-end data pipeline including data collection, cleaning, integration, exploratory data analysis, and machine learning.

---

## Data Sources

### Earthquakes
- Source: USGS Earthquake API
- Format: GeoJSON
- Data: magnitude, location, depth, time, tsunami indicators

### Weather
- Source: Open-Meteo API
- Data: hourly temperature based on earthquake coordinates and time


## Pipeline Steps

1. Download earthquake data from USGS API
2. Extract relevant features (location, magnitude, time)
3. Download weather data using Open-Meteo API
4. Merge both datasets
5. Clean and preprocess data
6. Perform exploratory data analysis (EDA)
7. Train predictive models


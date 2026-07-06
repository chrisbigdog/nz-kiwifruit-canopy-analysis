# Version 5 Plan: Regional Weather Context for Kiwifruit

## Goal

Add historical weather context to the dashboard so users can explore climate conditions across selected New Zealand kiwifruit-growing reference locations.

## Scope

This version will add weather context only. It will not claim that weather caused changes in national kiwifruit canopy area or individual orchard performance.

## Reference Locations

- Te Puke, Bay of Plenty
- Katikati, Bay of Plenty
- Opotiki, Bay of Plenty
- Kerikeri, Northland

## Planned Weather Measures

- Annual average temperature
- Annual rainfall
- Frost-day count
- Hot-day count

## Data Source

Open-Meteo Historical Weather API using reanalysis weather data.

## Planned Features

- Region selector in the Streamlit sidebar
- Weather year-range filter
- Weather summary metrics
- Annual rainfall chart
- Annual temperature chart
- Frost and hot-day trend chart
- Downloadable regional weather dataset
- Clear methodology and limitation notes

## Files to Add

- data/kiwifruit_weather_context.csv
- scripts/download_weather_data.py

## Files to Update

- streamlit_app.py
- README.md
- DATA_SOURCE.md
- requirements.txt, only if genuinely needed

## Target Release

v5.0.0 - Regional Weather Context
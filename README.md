# API Data Analysis Using Python Structures

## Project overview

This project retrieves a customer directory from the JSONPlaceholder API and explores where the records are located. JSONPlaceholder provides sample data, so these results do not describe real Pesa Pulse customers.

## What I did

- Retrieved customer records with `requests`.
- Explored nested dictionaries and extracted customer attributes.
- Used a set to find distinct cities and Python dictionaries to count cities and email endings.
- Converted the flattened records into a pandas DataFrame and compared its city counts with the Python counts.
- Saved the data and counts as CSV files and created a chart of email endings.

## Findings

- The API returned 10 sample customer records.
- The records have 10 unique cities, with one customer in each city. This sample shows no concentration in a particular city.
- The `info` email ending appears 3 times; `biz` and `net` appear 2 times each. The chart shows these differences, so it is more informative than the city chart, where every city has a count of one.

## How to run

Requires Python 3.9 or newer.

From the project folder, run these commands in PowerShell:

```terminal
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python analysis.py
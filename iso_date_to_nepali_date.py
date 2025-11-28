# pip install nepali-date_converter

from nepali_date_converter import english_to_nepali_converter
from datetime import datetime

# Your ISO date string
iso_date_string = "2023-07-03T10:30:00Z"

# Parse the ISO date string into a datetime object
# We only need the date components for the Nepali date conversion
dt_object = datetime.fromisoformat(iso_date_string.replace('Z', '+00:00')) 

# Extract year, month, and day
year = dt_object.year
month = dt_object.month
day = dt_object.day

# Convert to Nepali date
nepali_date = english_to_nepali_converter(year, month, day)

print(f"ISO Date: {iso_date_string}")
print(f"Nepali Date: {nepali_date}")

# Get the current date object
from datetime import date
iso_current_date = date.today()
print(f"Current ISO Date: {iso_current_date}")

# Extract year, month, and day
current_year = iso_current_date.year

current_month = iso_current_date.month
current_day = iso_current_date.day
#print(f"Current Nepali Date: {current_day}")

# Convert to Nepali date
current_nepali_date = english_to_nepali_converter(current_year, current_month, current_day)

print(f"Current Nepali Date: {current_nepali_date}")
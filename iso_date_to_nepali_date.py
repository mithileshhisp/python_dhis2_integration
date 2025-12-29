# pip install nepali-date_converter
# pip install npdatetime
# pip install datetime
#pip install bsdatetime
from nepali_date_converter import english_to_nepali_converter
from datetime import datetime, date ,timedelta
#from datetime import datetime, timedelta

import nepali_datetime

#from bsdatetime import bsdate
import calendar

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


# Get the current Nepali date and time
current_nepali_datetime = nepali_datetime.datetime.now()

# Extract the month number
nepali_current_month_number = current_nepali_datetime.month

# Extract the Nepali Year
nepali_current_year = current_nepali_datetime.year

# Get the month name (optional, if you need the name instead of the number)
nepali_current_month_name = current_nepali_datetime.strftime("%B")

print(f"Current Nepali Year: {nepali_current_year}")
print(f"Current Nepali month number: {nepali_current_month_number}")
print(f"Current Nepali month name: {nepali_current_month_name}")


##### Find Start & End Date of Any Nepali Month

#from nepali_datetime import NepaliDate
from nepali_datetime import date as NepaliDate

def get_bs_month_start_end(bs_year, bs_month):
    # Start date: always BS year + month + day 1
    start_date = NepaliDate(bs_year, bs_month, 1)

    # End date: start of next month minus 1 day
    if bs_month == 12:
        next_month_start = NepaliDate(bs_year + 1, 1, 1)
    else:
        next_month_start = NepaliDate(bs_year, bs_month + 1, 1)

    end_date = next_month_start - timedelta(days=1)

    return start_date, end_date

# Example: Get Baisakh 2081 Start & End
from datetime import timedelta

start, end = get_bs_month_start_end(2082, 8)

print("Nepali Start:", start)
print("Nepali End:", end)


## from nepali date to iso date
# Instantiate the converter
from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter
from nepali_calendar_utils.data.custom_calendar import SimpleDate

converter = NepaliDateConverter()

# Example Nepali date (Year, Month, Day)
nepali_year = 2082
nepali_month = 7
nepali_day = 1

# Convert the Nepali date to an English date object
#converted_english_date = converter.convert_nepali_to_english(nepali_year, nepali_month, nepali_day)


converted_english_date = converter.convert_nepali_to_english(nepali_current_year, nepali_current_month_number, 1)

# The result is a custom object, so extract the year, month, and day
ad_year = converted_english_date.year
ad_month = converted_english_date.month
ad_day = converted_english_date.day_of_month

print(f"Current ISO Year: {ad_year}")
print(f"Current ISO month number: {ad_month}")
print(f"Current ISO date: {ad_day}")


# Create a standard Python date object and use its isoformat() method
#ad_date = datetime.date(ad_year, ad_month, ad_day)
#ad_date = datetime.date(year, month, day)
#iso_date_string = ad_date.isoformat()

print(f"Nepali Date (BS): {nepali_year}-{nepali_month}-{nepali_day}")
print(f"ISO Date (AD): {iso_date_string}")



#### Correct & Tested Working Code
import nepali_datetime
from datetime import timedelta

def get_bs_month_start_end(bs_year, bs_month):
    # Start of Nepali month
    start_date = nepali_datetime.date(bs_year, bs_month, 1)

    # Start of next month
    if bs_month == 12:
        next_month = nepali_datetime.date(bs_year + 1, 1, 1)
    else:
        next_month = nepali_datetime.date(bs_year, bs_month + 1, 1)

    # End of month
    end_date = next_month - timedelta(days=1)

    return start_date, end_date


# Example: Baisakh 2081
start, end = get_bs_month_start_end(nepali_current_year, nepali_current_month_number)
#start, end = get_bs_month_start_end(2081, 1)


#start, end = get_bs_month_start_end(2082, 10) ## magh
#start, end = get_bs_month_start_end(2082, 11) ## fagun
#start, end = get_bs_month_start_end(2082, 12) ## chaitra
#start, end = get_bs_month_start_end(2083, 1) ## Baisakh

print("Start BS:", start)
print("End BS:", end)
print("Start AD:", start.to_datetime_date())
print("End AD:", end.to_datetime_date())

# get all dates between startdate,enddate


from datetime import datetime, timedelta

def get_between_dates(start_date, end_date):
    """
    start_date, end_date format: YYYY-MM-DD
    returns list of dates in YYYYMMDD format
    """

    # Convert date objects to string
    if isinstance(start_date, date):
        start_date = start_date.strftime("%Y-%m-%d")
    if isinstance(end_date, date):
        end_date = end_date.strftime("%Y-%m-%d")

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    arr = []
    current = start

    while current <= end:
        arr.append(current.strftime("%Y%m%d"))
        current += timedelta(days=1)

    return arr


#dates = get_between_dates("2023-01-28", "2023-02-03")
dates = get_between_dates(start.to_datetime_date(), end.to_datetime_date())
print("dates:" ,dates)
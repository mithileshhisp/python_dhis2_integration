#https://pypi.org/project/nepali-calendar-utils/
#pip install nepali-calendar-utils
#pip install nepali
#pip install nepali-datetime
import nepali
#from datetime import datetime
### current nepali date
from datetime import datetime

from nepali.datetime import nepalidate, parser

# Get the current local datetime object
iso_current_datetime = datetime.now()

# Example usage:
# Parse a Nepali date string
temp_nepali_datetime = parser.parse('2079-02-15')

print(f"Nepali nepali_datetime: {temp_nepali_datetime}")

#print(temp_nepali_datetime)

# Convert a Python datetime.date object to a nepalidate object
import datetime
date = datetime.date(2017, 3, 15)
nepali_date = nepalidate.from_date(date)

#print(nepali_date)
print(f"Nepali nepali_date: {nepali_date}")

# Nepali date string
nepali_date_str = "2079-02-15"  # Example: Jestha 15, 2079 BS

# Parse the Nepali date string
nepali_dt = nepali.datetime.parser.parse(nepali_date_str)

# Convert to standard datetime object
standard_dt = nepali_dt.to_datetime()

# Convert to ISO 8601 string
iso_date_str = standard_dt.isoformat()

print(f"Nepali Date: {nepali_date_str}")
print(f"ISO Date: {iso_date_str}")

### current nepali date
import nepali_datetime
# Get today's Nepali date
today_nepali_date = nepali_datetime.date.today()

# Print the Nepali date
print(f"Current Nepali Date: {today_nepali_date}")

### current nepali date
##from datetime import datetime

from datetime import date

# Get the current date object
iso_current_date = date.today()

# Convert the date object to an ISO 8601 formatted string
iso_format_date = iso_current_date.isoformat()

print(f"iso_format_date ISO Date: {iso_format_date}")
#rint(iso_format_date)

# Convert the datetime object to an ISO 8601 formatted string
iso_format_string = iso_current_datetime.isoformat()


print(f"Current ISO Date: {iso_current_date}")
print(f"Current ISO Date: {iso_format_string}")



#######################################

from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter
from nepali_calendar_utils.data.custom_calendar import SimpleDate
import datetime

# Instantiate the converter
converter = NepaliDateConverter()

# Example Nepali date (Year, Month, Day)
nepali_year = 2082
nepali_month = 7
nepali_day = 1

# Convert the Nepali date to an English date object
converted_english_date = converter.convert_nepali_to_english(nepali_year, nepali_month, nepali_day)

# The result is a custom object, so extract the year, month, and day
ad_year = converted_english_date.year
ad_month = converted_english_date.month
ad_day = converted_english_date.day_of_month

# Create a standard Python date object and use its isoformat() method
ad_date = datetime.date(ad_year, ad_month, ad_day)
iso_date_string = ad_date.isoformat()

print(f"Nepali Date (BS): {nepali_year}-{nepali_month}-{nepali_day}")
print(f"ISO Date (AD): {iso_date_string}")



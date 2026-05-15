import requests
import pandas as pd

#https://links.hispindia.org/amr_ghana/api/29/analytics/events/query/WhYipXYg2Nh.json?dimension=pe:LAST_12_MONTHS&dimension=ou:b3aCK1PTn5S&dimension=LjiZPsbh1oy.GqP6sLQ1Wt3&dimension=oLBln17zzdJ&dimension=LjiZPsbh1oy.rZa1towh7JE&dimension=uo3FuH69WXH&stage=LjiZPsbh1oy&displayProperty=NAME&totalPages=false&outputType=EVENT&desc=eventdate&pageSize=100&page=1
#https://links.hispindia.org/ippf_uin/api/organisationUnits.json?fields=id,name,code&paging=false
## https://development-finance-codelists.oecd.org/CodesList.aspx
url = "https://api.worldbank.org/v2/country?format=json&per_page=1000"
response = requests.get(url)
data = response.json()

# Extract parts
metadata = data[0]
countries = data[1]

print( f"length of metadata. { len(metadata) }" )

print( f"length of countries. { len(countries) }" )
# Flatten JSON into rows
rows = []

'''
for c in countries:
    rows.append({
        "id": c.get("id"),
        "name": c.get("name"),
        "iso2Code": c.get("iso2Code"),
        "region_id": c.get("region", {}).get("id"),
        "region_iso2code": c.get("region", {}).get("iso2code"),
        "region": c.get("region", {}).get("value"),
        "incomeLevel": c.get("incomeLevel", {}).get("id"),
        "lendingType_id": c.get("lendingType", {}).get("iso2code"),
        "lendingType_iso2code": c.get("lendingType", {}).get("value"),
        "lendingType": c.get("lendingType", {}).get("value"),
        "capitalCity": c.get("capitalCity"),
        "latitude": c.get("latitude"),
        "longitude": c.get("longitude")
    })
'''

rows = []

for c in countries:
    rows.append({
        "id": c.get("id"),
        "name": c.get("name"),
        "iso2Code": c.get("iso2Code"),

        "region_id": c.get("region", {}).get("id"),
        "region_iso2code": c.get("region", {}).get("iso2code"),
        "region": c.get("region", {}).get("value"),

        "incomeLevel_id": c.get("incomeLevel", {}).get("id"),
        "incomeLevel_iso2code": c.get("incomeLevel", {}).get("iso2code"),
        "incomeLevel": c.get("incomeLevel", {}).get("value"),

        "lendingType_id": c.get("lendingType", {}).get("id"),
        "lendingType_iso2code": c.get("lendingType", {}).get("iso2code"),
        "lendingType": c.get("lendingType", {}).get("value"),

        "capitalCity": c.get("capitalCity"),
        "latitude": c.get("latitude"),
        "longitude": c.get("longitude")
    })

print("Total rows:", len(rows))

#print(data)



# Create DataFrame
df = pd.DataFrame(rows)
print(len(df))

print(df.head()) ### only 5 rows default print

df.to_excel("word_bank_countries.xlsx", index=False)

#print(df) ### for all rows Show all rows (not recommended for large data)

#print(df.head(20)) ### Show first 20 rows

#print (df.tail(10)) ### Show last rows
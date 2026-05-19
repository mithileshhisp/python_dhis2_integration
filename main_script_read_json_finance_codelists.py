## https://development-finance-codelists.oecd.org/CodesList.aspx

import json

# Read JSON file
with open("DevFi_Classification - 2026-05-18T115729.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Access top-level keys
#print(data.keys())

print("data.keys():", data.keys())

print("date-last-modified:", data["codelists"]["date-last-modified"])

# Get codelist array
codelists = data["codelists"]["codelist"]

# Loop through codelists
for codelist in codelists:
    print("Codelist Name:", codelist["name"])

    # Get items
    items = codelist["codelist-items"]["codelist-item"]

    # Loop through items
    for item in items:
        code = item.get("code")
        status = item.get("status")
        country_type = item.get("type")
        iso_alpha_3_code = item.get("iso-alpha-3-code")
        iso_alpha_2_code = item.get("iso-alpha-2-code")
        dotstat_code = item.get("dotstatcode")

        # English name
        narrative = item["name"]["narrative"]

        if isinstance(narrative, list):
            english_name = narrative[0]
        else:
            english_name = narrative

        print({
            "code": code,
            "name": english_name,
            "status": status,
            "type": country_type,
            "iso_alpha_3_code" : iso_alpha_3_code,
            "iso_alpha_2_code" : iso_alpha_2_code
            #"dotstat_code" : dotstat_code
        })
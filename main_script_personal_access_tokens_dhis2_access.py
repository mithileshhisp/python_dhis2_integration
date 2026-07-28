import requests

#BASE_URL = "https://links.hispindia.org/ippf_uin/api/41"
BASE_URL = "https://uin.ippf.org/api/41"
## https://links.hispindia.org/ippf_uin/api/41/sqlViews/GUWnhJ6CDGI/data?paging=false&var=uincode:IPPF-AFG-004
## https://links.hispindia.org/ippf_uin/api/41/sqlViews/cTw6vXE1491/data?paging=false&var=uincode:IPPF-AFG-005

kofax_A_sql_view = "cTw6vXE1491"
kofax_B_sql_view = "GUWnhJ6CDGI"

uin_code = 'IPPF-AFG-005'

## ************ ## end user token -- as on 30/06/2026 pro
## ************ ## admin token

get_url = f"{BASE_URL}/sqlViews/{kofax_B_sql_view}/data?paging=false&var=uincode:{uin_code}"
print("get_url:", get_url)

headers = {
    "Authorization": "ApiToken ***********"
}

response = requests.get(get_url, headers=headers)

print("Status:", response.status_code)
#print(response.json())

try:
    #print(response.json())

    response = response.json()

    headers = [h["name"] for h in response["listGrid"]["headers"]]

    rows = response["listGrid"]["rows"]

    formatted_data = []

    for row in rows:
        row_data = dict(zip(headers, row))
        formatted_data.append(row_data)

    for item in formatted_data:
        print(item)

    for item in formatted_data:
        #print(item["org_name"])
        print(item["uin_code"])
        #print(item["senior_management_email"])        

except Exception:
    print(response.text)


### xlsx print 
import pandas as pd

headers = [h["name"] for h in response["listGrid"]["headers"]]
rows = response["listGrid"]["rows"]

df = pd.DataFrame(rows, columns=headers)

df.to_excel("sql_view_response.xlsx", index=False)

#print(df)    
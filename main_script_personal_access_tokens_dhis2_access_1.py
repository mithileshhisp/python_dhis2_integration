import requests

## ******** ## end user token -- as on 30/06/2026 pro
## ******** ## admin token

## presonal access token for PMNP-IS production

# kcis_integration *********** ## 17/07/2026  



#BASE_URL = "https://links.hispindia.org/ippf_uin/api/41"
BASE_URL = "https://uin.ippf.org/api/41"

kofax_A_sql_view = "cTw6vXE1491"
kofax_B_sql_view = "GUWnhJ6CDGI"

uin_code = 'IPPF-AFG-005'

get_url = f"{BASE_URL}/sqlViews/{kofax_B_sql_view}/data?paging=false&var=uincode:{uin_code}"

print("get_url:", get_url)

headers = {
    "Authorization": "ApiToken ***********"
}

response = requests.get(get_url, headers=headers)

#print("Status:", response.status_code)
#print(response.json())

try:
    #response = response.json()
    
    print("Status:", response.status_code)
    print(response.json())

except Exception:
    print(response.text)
 
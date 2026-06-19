import requests

BASE_URL = "https://links.hispindia.org/ippf_uin/api/41"


kofax_A_sql_view = "cTw6vXE1491"
kofax_B_sql_view = "GUWnhJ6CDGI"

uin_code = 'IPPF-AFG-005'

get_url = f"{BASE_URL}/sqlViews/{kofax_B_sql_view}/data?paging=false&var=uincode:{uin_code}"

headers = {
    "Authorization": "ApiToken *********"
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
 
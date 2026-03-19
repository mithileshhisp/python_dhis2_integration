import requests

url = "https://your-sms-gateway-url"

params = {
    "token": "YOUR_TOKEN",
    "from": "SENDER_ID",
    "to": "919876543210",
    "text": "Hello from Python SMS"
}

response = requests.get(url, params=params)

# Check response
try:
    response.raise_for_status()
    print("SMS sent successfully:", response.text)
except requests.exceptions.HTTPError as e:
    print("Error sending SMS:", e)



#1. Extract headers + rows    

data = response.json()

list_grid = data.get("listGrid", {})

headers = [h["name"] for h in list_grid.get("headers", [])]
rows = list_grid.get("rows", [])

#🔹 2. Convert each row into dictionary (VERY IMPORTANT)

for row in rows:
    row_dict = dict(zip(headers, row))
    
    print(row_dict)

#👉 Output will be like:    
{
 'org_name': 'BARDIYA HOSPITAL',
 'due_date': '2026-03-18',
 'tei_uid': 'pD8gtdJY3q1',
 'sms_consent': 'true',
 'mobile_number': '9869189488'
}

#✅ 3. Access specific fields (for SMS use case)
for row in rows:
    row_dict = dict(zip(headers, row))

    if row_dict.get("sms_consent") == "true" and row_dict.get("mobile_number"):
        mobile = row_dict["mobile_number"]
        tei = row_dict["tei_uid"]
        due_date = row_dict["due_date"]

        print(mobile, tei, due_date)

#✅ 4. Example: Send SMS only valid numbers
for row in rows:
    row_dict = dict(zip(headers, row))

    mobile = row_dict.get("mobile_number")

    if row_dict.get("sms_consent") == "true" and mobile:
        message = f"Reminder: Your due date is {row_dict['due_date']}"

        print(f"Sending SMS to {mobile}: {message}")    


data_rows = [dict(zip(headers, row)) for row in rows]

for r in data_rows:
    print(r["mobile_number"])     




import requests

# ================= CONFIG =================
DHIS2_URL = "YOUR_DHIS2_API_URL"
DHIS2_USERNAME = "YOUR_USERNAME"
DHIS2_PASSWORD = "YOUR_PASSWORD"

SMS_API_URL = "YOUR_SMS_API_URL"

TOKEN = "your_token"
SENDER = "your_sender_id"

# =========================================

def get_dhis2_data():
    response = requests.get(
        DHIS2_URL,
        auth=(DHIS2_USERNAME, DHIS2_PASSWORD)
    )
    
    response.raise_for_status()
    return response.json()


def send_sms(mobile, message):
    params = {
        "token": TOKEN,
        "from": SENDER,
        "to": mobile,
        "text": message,
        "encoding": "unicode"   # ✅ IMPORTANT
    }

    response = requests.get(SMS_API_URL, params=params)

    try:
        response.raise_for_status()
        print(f"✅ SMS sent to {mobile}")
    except Exception as e:
        print(f"❌ Failed for {mobile}: {e}")


def process_and_send(data):
    list_grid = data.get("listGrid", {})
    
    headers = [h["name"] for h in list_grid.get("headers", [])]
    rows = list_grid.get("rows", [])

     # ✅ ADD HERE (outside loop)
    sent_numbers = set()

    for row in rows:
        row_dict = dict(zip(headers, row))

        sms_consent = row_dict.get("sms_consent")
        mobile = row_dict.get("mobile_number")
        due_date = row_dict.get("due_date")
        org_name = row_dict.get("org_name")

        # ✅ Validation
        if sms_consent != "true":
            continue
        
        if not mobile or len(mobile) < 10:
            continue

        #🔴 3. Avoid sending duplicates (optional but recommended)    
        # ✅ CHECK DUPLICATE (inside loop)
        if mobile in sent_numbers:
            continue

        # ✅ ADD TO SET
        sent_numbers.add(mobile)

        # ✅ Message
        message = f"Reminder: Visit {org_name} on {due_date} for pill pickup."
        customMessagePillPick = f"तपाइको औषधि लिने बेला भयो, तपाई मिति {due_date} गते {org_name} को केन्द्रमा आउनुहोला |"
        #customMessagePillPick = f"तपाइको औषधि लिने बेला भयो, तपाई  मिति  {due_date} गते  {org_name} को केन्द्रमा आउनुहोला  |"
        # ✅ Send SMS
        send_sms(mobile, message)


# ================= RUN =================
if __name__ == "__main__":
    data = get_dhis2_data()
    process_and_send(data)     




   
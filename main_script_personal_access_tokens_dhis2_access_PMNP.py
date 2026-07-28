import requests

## 1) Call the Organisation Unit API using the org unit code.
## 2) Read the JSON response.
## 3) If an organisation unit is found, extract its id.
## 4) Use that id in the Analytics API (filter=ou:<orgUnitId>).
## presonal access token for PMNP-IS production

# kcis_integration ********* ## 17/07/2026  

BASE_URL = "https://pmnpis.org.ph/app/api"

yearly_period = 2025
org_unit_uid = 'DcGhhRsspFX'
org_unit_code = '0304906000'
#https://pmnpis.org.ph/app/api/organisationUnits.json?fields=id,name,code&filter=code:eq:0304906000&paging=false
#https://pmnpis.org.ph/app/api/analytics.json?dimension=pe:2025&dimension=dx:tbH90pxjEsN;ZfmDHEb9uQe;dAqJKQ4OZJE;WIwOPHkXrib;qaHtUpS9kUs;ohWphabXLPr;nW4xAUAiNtP;Wnpbp6DpzE2;Tpq4v4qroKY;i8lBqJk4cA1;HUSDXNHQmWZ;oVVvN7h8Zki;gw3cgbs2B2c;BC8ZOPIZaqV;oui7wEa1HIP;RGmeOlU71Pu;kXxL7ARMbBk;nkHVSQNwWIF;IvLXsQrfAO9;skz1XUlSgWk;MEcIqV9DvI4;RLP708qxvL0;LuPM6N9Ecyq;yWQwNXYc36f;w3GaHmfdvYJ;RanmiYVBHos;jovTdeirrQ4;Gqiy05nFdz6;HfsMIIu0cSY;asWDgkKlG2r;jnEqLOWSf81;oLTrwJEDOtt;VrCKYKoPK7H;fRnxHUjFVr0;ok8a4Keduff;BKorBU0vUbs;FUNpIngBpNa;ssBTgsfHVUE;e54uVFVAnOV;lemgvBog5dW;STuVG1XHGmm;JjLKhWZdBOO;rk4jfp6tTmv;QPwt60voMCL;H50RcQ6yMLl;tMnec4aBAxA;dcvPuoevjBy;zFuq4Sev0bU;k2dO6h2JG3W;IuSSX9mh0aq;GtbvGQhu5vJ;WuxI941cBtx;Uo0cNGu7vGe;uxvcyuIZ4Eh;NYq6ZaKFteu;oTiXzLzaS4z;MaASM7AxfBI;DlDgg64JyYk;zf4ADyiUS6B;FUDCZ3U4LKm;SWUTyQIG7p4;aIdk9BwVRsw;siiaQMrMlDA;CzSAtWT2o1u;gfKpnM232B2;nIQuIXXCK0i;jIn9G9WPC3l;DZl1yGtHDnl;jggZlcZhx4L;UN1kylBm76p;KrYLnwlmznJ;LabBoNwNvL1;XNvIu1JKLvs;kMAHWHTzUJx;hKsm6EdKGU6&showHierarchy=false&hierarchyMeta=false&includeMetadataDetails=true&includeNumDen=true&skipRounding=false&completedOnly=false&outputIdScheme=CODE&filter=ou:DcGhhRsspFX

#get_org_unit_url = f"{BASE_URL}/organisationUnits.json?fields=id,name,code&filter=code:eq:{org_unit_code}&paging=false"

#get_url = f"{BASE_URL}/analytics.json?dimension=pe:{yearly_period}&dimension=dx:tbH90pxjEsN;ZfmDHEb9uQe;dAqJKQ4OZJE;WIwOPHkXrib;qaHtUpS9kUs;ohWphabXLPr;nW4xAUAiNtP;Wnpbp6DpzE2;Tpq4v4qroKY;i8lBqJk4cA1;HUSDXNHQmWZ;oVVvN7h8Zki;gw3cgbs2B2c;BC8ZOPIZaqV;oui7wEa1HIP;RGmeOlU71Pu;kXxL7ARMbBk;nkHVSQNwWIF;IvLXsQrfAO9;skz1XUlSgWk;MEcIqV9DvI4;RLP708qxvL0;LuPM6N9Ecyq;yWQwNXYc36f;w3GaHmfdvYJ;RanmiYVBHos;jovTdeirrQ4;Gqiy05nFdz6;HfsMIIu0cSY;asWDgkKlG2r;jnEqLOWSf81;oLTrwJEDOtt;VrCKYKoPK7H;fRnxHUjFVr0;ok8a4Keduff;BKorBU0vUbs;FUNpIngBpNa;ssBTgsfHVUE;e54uVFVAnOV;lemgvBog5dW;STuVG1XHGmm;JjLKhWZdBOO;rk4jfp6tTmv;QPwt60voMCL;H50RcQ6yMLl;tMnec4aBAxA;dcvPuoevjBy;zFuq4Sev0bU;k2dO6h2JG3W;IuSSX9mh0aq;GtbvGQhu5vJ;WuxI941cBtx;Uo0cNGu7vGe;uxvcyuIZ4Eh;NYq6ZaKFteu;oTiXzLzaS4z;MaASM7AxfBI;DlDgg64JyYk;zf4ADyiUS6B;FUDCZ3U4LKm;SWUTyQIG7p4;aIdk9BwVRsw;siiaQMrMlDA;CzSAtWT2o1u;gfKpnM232B2;nIQuIXXCK0i;jIn9G9WPC3l;DZl1yGtHDnl;jggZlcZhx4L;UN1kylBm76p;KrYLnwlmznJ;LabBoNwNvL1;XNvIu1JKLvs;kMAHWHTzUJx;hKsm6EdKGU6&showHierarchy=false&hierarchyMeta=false&includeMetadataDetails=true&includeNumDen=true&skipRounding=false&completedOnly=false&outputIdScheme=CODE&filter=ou:{org_unit_uid}"

#print("get_url:", get_org_unit_url)

headers = {
    "Authorization": "ApiToken *************"
}

#*********
#*********
# Step 1: Get Organisation Unit ID
org_unit_url = (
    f"{BASE_URL}/organisationUnits.json"
    f"?fields=id,name,code"
    f"&filter=code:eq:{org_unit_code}"
    f"&paging=false"
)

response = requests.get(org_unit_url, headers=headers)

response.raise_for_status()

data = response.json()

print(f"Org_response_data   : {data}")

org_units = data.get("organisationUnits", [])

if not org_units:
    print("Organisation Unit not found")
else:
    org_id = org_units[0]["id"]
    org_name = org_units[0]["name"]

    print(f"Org ID   : {org_id}")
    print(f"Org Name : {org_name}")

    analytics_url = (
        f"{BASE_URL}/analytics.json"
        f"?dimension=pe:{yearly_period}"
        f"&dimension=dx:tbH90pxjEsN;ZfmDHEb9uQe;dAqJKQ4OZJE;WIwOPHkXrib;qaHtUpS9kUs;ohWphabXLPr;nW4xAUAiNtP;Wnpbp6DpzE2;Tpq4v4qroKY;i8lBqJk4cA1;HUSDXNHQmWZ;oVVvN7h8Zki;gw3cgbs2B2c;BC8ZOPIZaqV;oui7wEa1HIP;RGmeOlU71Pu;kXxL7ARMbBk;nkHVSQNwWIF;IvLXsQrfAO9;skz1XUlSgWk;MEcIqV9DvI4;RLP708qxvL0;LuPM6N9Ecyq;yWQwNXYc36f;w3GaHmfdvYJ;RanmiYVBHos;jovTdeirrQ4;Gqiy05nFdz6;HfsMIIu0cSY;asWDgkKlG2r;jnEqLOWSf81;oLTrwJEDOtt;VrCKYKoPK7H;fRnxHUjFVr0;ok8a4Keduff;BKorBU0vUbs;FUNpIngBpNa;ssBTgsfHVUE;e54uVFVAnOV;lemgvBog5dW;STuVG1XHGmm;JjLKhWZdBOO;rk4jfp6tTmv;QPwt60voMCL;H50RcQ6yMLl;tMnec4aBAxA;dcvPuoevjBy;zFuq4Sev0bU;k2dO6h2JG3W;IuSSX9mh0aq;GtbvGQhu5vJ;WuxI941cBtx;Uo0cNGu7vGe;uxvcyuIZ4Eh;NYq6ZaKFteu;oTiXzLzaS4z;MaASM7AxfBI;DlDgg64JyYk;zf4ADyiUS6B;FUDCZ3U4LKm;SWUTyQIG7p4;aIdk9BwVRsw;siiaQMrMlDA;CzSAtWT2o1u;gfKpnM232B2;nIQuIXXCK0i;jIn9G9WPC3l;DZl1yGtHDnl;jggZlcZhx4L;UN1kylBm76p;KrYLnwlmznJ;LabBoNwNvL1;XNvIu1JKLvs;kMAHWHTzUJx;hKsm6EdKGU6&showHierarchy=false&hierarchyMeta=false&includeMetadataDetails=true&includeNumDen=true&skipRounding=false&completedOnly=false&outputIdScheme=UID"
        f"&filter=ou:{org_id}"
    )

    #print(analytics_url)
    analytics_response = requests.get(
        analytics_url,
        headers=headers
    )

    analytics_response.raise_for_status()

    analytics_data = analytics_response.json()

    #print(f"analytics_data   : {analytics_data}")

    # UID -> metadata
    items = analytics_data["metaData"]["items"]

    for row in analytics_data["rows"]:
        dx = row[0]
        period = row[1]
        value = row[2]

        indicator_name = items[dx]["name"]

        print(f"{indicator_name} ({dx})")
        print(f"Period : {period}")
        print(f"Value  : {value}")
        print("-" * 50)

 
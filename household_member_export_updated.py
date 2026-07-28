'''
python household_member_export.py \
    --url https://dhis2.server.org \
    --username admin \
    --password district \
    --orgunit DiszpKrYNg8

python household_member_export.py \
    --url https://dhis2.server.org \
    --username admin \
    --password district \
    --orgunit 0304906001 \
    --orgunit-type CODE

'''

# python -m pip install tqdm
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
=========================================================================
DHIS2 Household & Household Member Export
Version : 2.0
Target  : DHIS2 2.40
Output  : CSV

Author  : ChatGPT
=========================================================================

Workflow

1. Download Households
2. Build Household Dictionary
3. Download Household Members
4. Match using Family Information attribute
5. Export CSV

=========================================================================
"""

import csv
import argparse
import logging, datetime
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
#from tqdm import tqdm

import re


##############################################################################
# CONFIGURATION
##############################################################################

PAGE_SIZE = 1000

THREADS = 20

TIMEOUT = 120

VERIFY_SSL = True

OUTPUT_FILE = "Household_Member_Export.csv"

##############################################################################
# PROGRAM UID
##############################################################################

HOUSEHOLD_PROGRAM = "oSNoNtcmLXL"

HOUSEHOLD_MEMBER_PROGRAM = "VVLirjoOGbj"

##############################################################################
# HOUSEHOLD ATTRIBUTES
##############################################################################

HH_HEAD = "GXs8SDJL19y"

HH_PUROK = "J2KmQw53CRl"

HH_STREET = "HYNM3CJYLje"

HH_CONTACT = "D9fGfe9AmkZ"

##############################################################################
# MEMBER ATTRIBUTES
##############################################################################

FAMILY_INFORMATION = "gv9xX5w4kKt"

PMNP_ID = "NOKzq4dAKF7"

FIRST_NAME = "PIGLwIaw0wy"

MIDDLE_NAME = "WC0cShCpae8"

LAST_NAME = "IENWcinF8lM"

EXTENSION_NAME = "nyVsU3fTk2b"

RELATIONSHIP = "QAYXozgCOHu"

SEX = "Qt4YSwPxw0X"

DOB = "fJPZFs2yYJQ"

ETHNICITY = "g276qF2fXHi"

PHILSYS_ID = "KFjMj5iiEje"

PHILSYS_MEMBERSHIP = "dDPD11ONpZn"

PHIC_ID = "Yp6gJAdu4yX"

PHIC_MEMBERSHIP = "JjFcU1L7Ll1"

##############################################################################
# LOGGER
##############################################################################

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s %(levelname)s %(message)s"

)

logger = logging.getLogger(__name__)

##############################################################################
# REQUEST SESSION
##############################################################################

def create_session(username, password):

    session = requests.Session()

    retry = Retry(

        total=5,

        connect=5,

        read=5,

        backoff_factor=2,

        status_forcelist=[500,502,503,504],

        allowed_methods=["GET"]

    )

    adapter = HTTPAdapter(max_retries=retry)

    session.mount("http://", adapter)

    session.mount("https://", adapter)

    session.auth = (username, password)

    session.verify = VERIFY_SSL

    session.headers.update({

        "Accept":"application/json"

    })

    return session

##############################################################################
# DHIS2 CLIENT
##############################################################################

class DHIS2Client:

    def __init__(

        self,

        base_url,

        username,

        password

    ):

        self.base_url = base_url.rstrip("/")

        self.session = create_session(

            username,

            password

        )

    ##############################################################

    def get(

        self,

        endpoint,

        params=None

    ):

        url = self.base_url + endpoint

        response = self.session.get(

            url,

            params=params,

            timeout=TIMEOUT

        )

        response.raise_for_status()

        return response.json()

##############################################################################
# ATTRIBUTE HELPER
##############################################################################

def attribute_dict(attributes):

    data = {}

    if attributes is None:

        return data

    for item in attributes:

        data[item["attribute"]] = item.get("value","")

    return data

##############################################################################
# CSV HEADER
##############################################################################

CSV_HEADER = [

"Household OrgUnit UID",

"Household OrgUnit Name",

"Household TEI UID",

"Household Head",

"Purok",

"Street",

"Contact",

"Member TEI UID",

"PMNP ID",

"First Name",

"Middle Name",

"Last Name",

"Extension Name",

"Relationship with household Head",

"Sex",

"DOB",

"Name of IP group (Ethnicity)",

"PhilSys ID",

"PhilSys Membership",

"PHIC ID",

"PHIC Membership"

]


##############################################################################
# HOUSEHOLD DOWNLOAD
##############################################################################

def get_households(client, org_unit_uid, orgUnitName):
    """
    Download all households from Household Program.

    Returns
    -------
    {
        household_uid:{
            household_orgunit_uid,
            household_orgunit_name,
            household_head,
            purok,
            street,
            contact
        }
    }
    """

    logger.info("=" * 70)
    logger.info("Downloading Household TEIs...")
    logger.info("=" * 70)

    households = {}

    page = 1

    while True:

        params = {

            "program": HOUSEHOLD_PROGRAM,

            "ou": org_unit_uid,

            "ouMode": "DESCENDANTS",

            "page": page,

            "pageSize": PAGE_SIZE,

            #"skipPaging": "false",
            "skipPaging": "true",

            #"paging" : "true",

            "fields": "trackedEntityInstance,orgUnit,attributes"

        }

        '''
        # Org Unit UID
        if orgunit_type.upper() == "UID":
            params["ou"] = org_unit
            
            #params["orgUnit"] = org_unit

        # Org Unit CODE
        else:
            params["ou"] = "CODE:" + org_unit
            #params["orgUnit"] = "CODE:" + org_unit
        '''

        data = client.get(

            "/api/trackedEntityInstances",

            params=params

        )
        #print(data.keys())
        #print(data.get("pager"))

        print("PAGE =", page)
        print(params)

        teis = data.get("trackedEntityInstances", [])

        if len(teis) == 0:
            break

        logger.info(
            "Household Page %s : %s records",
            page,
            len(teis)
        )

        for tei in teis:

            attrs = attribute_dict(

                tei.get("attributes", [])

            )

            household_uid = tei["trackedEntityInstance"]

            households[household_uid] = {

                "household_orgunit_uid":

                    tei.get("orgUnit", ""),

                "household_orgunit_name":

                    orgUnitName,

                "household_head":

                    attrs.get(HH_HEAD, ""),

                "purok":

                    attrs.get(HH_PUROK, ""),

                "street":

                    attrs.get(HH_STREET, ""),

                "contact":

                    attrs.get(HH_CONTACT, "")

            }

        pager = data.get("pager", {})

        if page >= pager.get("pageCount", 1):
            break

        page += 1

    logger.info("")
    logger.info("Total Household TEIs : %s", len(households))
    logger.info("")

    return households

##############################################################################
# HOUSEHOLD SUMMARY
##############################################################################

def print_household_summary(households):

    logger.info("=" * 70)

    logger.info("HOUSEHOLD SUMMARY")

    logger.info("=" * 70)

    logger.info("Total Household : %s", len(households))

    logger.info("")

    if households:

        first_key = next(iter(households))

        logger.info("Example Household")

        logger.info(households[first_key])

    logger.info("")

##############################################################################
# HOUSEHOLD MEMBER DOWNLOAD
##############################################################################

def get_household_members(client, org_unit_uid, households, orgUnitName, 
    sex_map, relationship_map,ethnicity_map,philys_membership_map,phic_membership_map):
    """
    Download Household Members and match them with downloaded households.

    Returns
    -------
    list of rows
    """

    logger.info("=" * 70)
    logger.info("Downloading Household Members...")
    logger.info("=" * 70)

    rows = []

    page = 1

    total_members = 0

    matched_members = 0

    while True:

        params = {

            "program": HOUSEHOLD_MEMBER_PROGRAM,

            "ou": org_unit_uid,

            "ouMode": "DESCENDANTS",

            "page": page,

            "pageSize": PAGE_SIZE,

            "skipPaging": "true",
            #"paging": "true",

            "fields": "trackedEntityInstance,orgUnit,orgUnitName,attributes"

        }

        '''
        if orgunit_type.upper() == "UID":
            params["ou"] = org_unit
            # params["orgUnit"] = org_unit

        else:
            params["ou"] = "CODE:" + org_unit
            # params["orgUnit"] = "CODE:" + org_unit
        '''
        data = client.get(

            "/api/trackedEntityInstances",

            params=params

        )

        #print("PAGE =", page)
        #print("params =", params )

        teis = data.get("trackedEntityInstances", [])

        if len(teis) == 0:
            break

        logger.info(
            "Member Page %s : %s records",
            page,
            len(teis)
        )

        for tei in teis:

            total_members += 1

            attrs = attribute_dict(

                tei.get("attributes", [])

            )

            household_uid = attrs.get(FAMILY_INFORMATION, "")

            if household_uid == "":
                continue

            if household_uid not in households:
                continue

            hh = households[household_uid]

            rows.append([

                hh["household_orgunit_uid"],

                hh["household_orgunit_name"],

                household_uid,

                hh["household_head"],

                hh["purok"],

                hh["street"],

                hh["contact"],

                tei.get("trackedEntityInstance", ""),

                attrs.get(PMNP_ID, ""),

                attrs.get(FIRST_NAME, ""),

                attrs.get(MIDDLE_NAME, ""),

                attrs.get(LAST_NAME, ""),

                attrs.get(EXTENSION_NAME, ""),

                #attrs.get(RELATIONSHIP, ""),
                #second argument to .get() is a fallback so that if a code isn't found, the original value is still written.
                relationship_map.get(
                    attrs.get(RELATIONSHIP, ""),
                    attrs.get(RELATIONSHIP, "")
                ),
                #attrs.get(SEX, ""),
                sex_map.get(
                    attrs.get(SEX, ""),
                    attrs.get(SEX, "")
                ),
                attrs.get(DOB, ""),

                ethnicity_map.get(
                    attrs.get(ETHNICITY, ""),
                    attrs.get(ETHNICITY, "")
                ),

                #attrs.get(ETHNICITY, ""),

                attrs.get(PHILSYS_ID, ""),

                #attrs.get(PHILSYS_MEMBERSHIP, ""),

                philys_membership_map.get(
                    attrs.get(PHILSYS_MEMBERSHIP, ""),
                    attrs.get(PHILSYS_MEMBERSHIP, "")
                ),

                attrs.get(PHIC_ID, ""),

                #attrs.get(PHIC_MEMBERSHIP, "")

                phic_membership_map.get(
                    attrs.get(PHIC_MEMBERSHIP, ""),
                    attrs.get(PHIC_MEMBERSHIP, "")
                ),                

            ])

            matched_members += 1

        pager = data.get("pager", {})

        if page >= pager.get("pageCount", 1):
            break

        page += 1

    logger.info("")
    logger.info("Total Members Read     : %s", total_members)
    logger.info("Matched Members        : %s", matched_members)
    logger.info("")

    return rows

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--url",
        required=True,
        help="DHIS2 URL"
    )

    parser.add_argument(
        "--username",
        required=True
    )

    parser.add_argument(
        "--password",
        required=True
    )

    parser.add_argument(
        "--orgunit",
        required=True,
        help="Organisation Unit UID"
    )
    parser.add_argument(
        "--orgunit-type",
        choices=["UID", "CODE"],
        default="UID",
        help="Organisation Unit identifier type (UID or CODE)"
    )

    args = parser.parse_args()

    client = DHIS2Client(
        args.url,
        args.username,
        args.password
    )

    if args.orgunit_type.upper() == "CODE":
        orgUnitUid, orgUnitName = get_orgunit_uid_name(client, args.orgunit)
        args.orgunit = orgUnitUid

    output_file_name = create_output_filename(orgUnitName)

    households = get_households(
        client,
        args.orgunit,orgUnitName
    )

    print_household_summary(households)

    # Part 3
    # download household members

    # Part 4
    # export csv
    sex_map = get_option_map(client, SEX)
    relationship_map = get_option_map(client, RELATIONSHIP)
    ethnicity_map = get_option_map(client, ETHNICITY)
    philys_membership_map = get_option_map(client, PHILSYS_MEMBERSHIP)
    phic_membership_map = get_option_map(client, PHIC_MEMBERSHIP)

    rows = get_household_members(

        client,

        args.orgunit,

        households, orgUnitName, sex_map, relationship_map,
        ethnicity_map,philys_membership_map,phic_membership_map

    )

    logger.info("Rows Ready For Export : %s", len(rows))

    export_csv(rows,output_file_name)


##############################################################################
# Create CSV File name
##############################################################################

def create_output_filename(orgunit_name):
    """
    Create a safe CSV filename from the Org Unit name.
    """

    # Replace invalid filename characters
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', orgunit_name)

    # Replace spaces with underscores
    safe_name = safe_name.replace(" ", "_")

    return f"Household_Member_Export_{safe_name}.csv"

##############################################################################
# CSV EXPORT
##############################################################################

def export_csv(rows, output_file=OUTPUT_FILE):
    """
    Export Household + Household Members to CSV.
    """

    logger.info("=" * 70)
    logger.info("Exporting CSV...")
    logger.info("=" * 70)

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as csvfile:

        writer = csv.writer(csvfile)

        # Header
        writer.writerow(CSV_HEADER)

        # Data
        writer.writerows(rows)

    logger.info("")
    logger.info("CSV Successfully Created")
    logger.info("Rows Exported : %s", len(rows))
    logger.info("Output File   : %s", output_file)
    logger.info("")

##############################################################################
# GET OrgUnit Uid, Name
##############################################################################
def get_orgunit_uid_name(client, orgunit_code):

    data = client.get(
        "/api/organisationUnits",
        params={
            "filter": f"code:eq:{orgunit_code}",
            "fields": "id,name,code"
        }
    )

    ous = data.get("organisationUnits", [])

    if not ous:
        raise Exception(f"Organisation Unit code not found: {orgunit_code}")

    return ous[0]["id"], ous[0]["name"]


##############################################################################
# OPTION SET with TEI attribute
##############################################################################

def get_option_map(client, attribute_uid):
    """
    Returns a dictionary:
    {
        "1": "Male",
        "2": "Female"
    }
    """

    data = client.get(
        f"/api/trackedEntityAttributes/{attribute_uid}",
        params={
            "fields": "optionSet[options[code,name]]"
        }
    )

    option_map = {}

    option_set = data.get("optionSet")

    if option_set:

        for option in option_set.get("options", []):

            option_map[option["code"]] = option["name"]

    return option_map



if __name__ == "__main__":
    current_time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print( f"House Hold and Members Data Export Start Time . { current_time_start }" )
    logger.info(f"House Hold and Members Data Export Start Time  . { current_time_start }")
    
    main()

    current_time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print( f"House Hold and Members Data Export End Time . { current_time_end }" )
    logger.info(f"House Hold and Members Data Export End Time  . { current_time_end }")

#python household_member_export_updated.py --url https://pmnpis.org.ph/app --username ******* --password ******* --orgunit mkvLp2ySTPb  --orgunit-type CODE

#python household_member_export_updated.py --url https://pmnpis.org.ph/app --username ******* --password ******* --orgunit 0304906001  --orgunit-type CODE
#python household_member_export_updated.py --url https://pmnpis.org.ph/app --username ******* --password ******* --orgunit 0405602001  --orgunit-type CODE

'''
Step 1: Add a function to load option sets
##############################################################################
# OPTION SET
##############################################################################

def get_option_map(client, attribute_uid):
    """
    Returns a dictionary:
    {
        "1": "Male",
        "2": "Female"
    }
    """

    data = client.get(
        f"/api/trackedEntityAttributes/{attribute_uid}",
        params={
            "fields": "optionSet[options[code,name]]"
        }
    )

    option_map = {}

    option_set = data.get("optionSet")

    if option_set:

        for option in option_set.get("options", []):

            option_map[option["code"]] = option["name"]

    return option_map
Step 2: Load the maps in main()

After creating the client:

sex_map = get_option_map(client, SEX)

relationship_map = get_option_map(client, RELATIONSHIP)
Step 3: Pass them to get_household_members()

Change:

rows = get_household_members(
    client,
    args.orgunit,
    households
)

to:

rows = get_household_members(
    client,
    args.orgunit,
    households,
    sex_map,
    relationship_map
)
Step 4: Convert the codes

Where you currently create the CSV row:

attrs.get(RELATIONSHIP, ""),
attrs.get(SEX, ""),

replace with:

relationship_map.get(
    attrs.get(RELATIONSHIP, ""),
    attrs.get(RELATIONSHIP, "")
),

sex_map.get(
    attrs.get(SEX, ""),
    attrs.get(SEX, "")
),

The second argument to .get() is a fallback so that if a code isn't found, the original value is still written.

Yes. If your DHIS2 server supports Personal Access Tokens (PAT) (DHIS2 2.36+), you can completely remove the username/password authentication and use a bearer token.

Option 1 (Recommended): Bearer Token

Replace your create_session() function with:

##############################################################################
# REQUEST SESSION
##############################################################################

def create_session(token):

    session = requests.Session()

    retry = Retry(
        total=5,
        connect=5,
        read=5,
        backoff_factor=2,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"]
    )

    adapter = HTTPAdapter(max_retries=retry)

    session.mount("http://", adapter)
    session.mount("https://", adapter)

    session.verify = VERIFY_SSL

    session.headers.update({
        "Accept": "application/json",
        "Authorization": f"ApiToken {token}"
    })

    return session
Update DHIS2Client

Replace:

class DHIS2Client:

    def __init__(
        self,
        base_url,
        username,
        password
    ):

        self.base_url = base_url.rstrip("/")

        self.session = create_session(
            username,
            password
        )

with:

class DHIS2Client:

    def __init__(
        self,
        base_url,
        token
    ):

        self.base_url = base_url.rstrip("/")

        self.session = create_session(token)
Update argparse

Remove:

parser.add_argument("--username", required=True)

parser.add_argument("--password", required=True)

Replace with:

parser.add_argument(
    "--token",
    required=True,
    help="DHIS2 Personal Access Token"
)
Update main()

Replace:

client = DHIS2Client(
    args.url,
    args.username,
    args.password
)

with:

client = DHIS2Client(
    args.url,
    args.token
)
Run
python household_member_export.py \
    --url https://pmnpis.org.ph/app \
    --token YOUR_PERSONAL_ACCESS_TOKEN \
    --orgunit-type CODE \
    --orgunit 0304906001








'''
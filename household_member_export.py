#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
==========================================================
DHIS2 Household & Household Member Export
Version : 1.0
Author  : ChatGPT
Target  : DHIS2 2.40+
Output  : CSV
==========================================================
"""

import os
import csv
import time
import json
import argparse
import logging
from typing import Dict, List

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from tqdm import tqdm


###############################################################################
# CONFIGURATION
###############################################################################

# --------------------------------------------------------------------------
# CHANGE THESE VALUES
# --------------------------------------------------------------------------

DHIS2_URL = "https://your-dhis2-server.org"

USERNAME = "admin"

PASSWORD = "district"

VERIFY_SSL = True

PAGE_SIZE = 1000

TIMEOUT = 120

OUTPUT_FILE = "Household_Member_Export.csv"

###############################################################################
# PROGRAM UID
###############################################################################

HOUSEHOLD_PROGRAM = "oSNoNtcmLXL"

HOUSEHOLD_MEMBER_PROGRAM = "VVLirjoOGbj"

###############################################################################
# HOUSEHOLD ATTRIBUTES
###############################################################################

HH_HEAD = "GXs8SDJL19y"

HH_PUROK = "J2KmQw53CRl"

HH_STREET = "HYNM3CJYLje"

HH_CONTACT = "D9fGfe9AmkZ"

###############################################################################
# MEMBER ATTRIBUTES
###############################################################################

FAMILY_INFORMATION = "gv9xX5w4kKt"

PMNP_ID = "NOKzq4dAKF7"

FIRST_NAME = "PIGLwIaw0wy"

MIDDLE_NAME = "WC0cShCpae8"

LAST_NAME = "IENWcinF8lM"

EXTENSION = "nyVsU3fTk2b"

RELATIONSHIP = "QAYXozgCOHu"

SEX = "Qt4YSwPxw0X"

DOB = "fJPZFs2yYJQ"

ETHNICITY = "g276qF2fXHi"

PHILSYS_ID = "KFjMj5iiEje"

PHILSYS_MEMBERSHIP = "dDPD11ONpZn"

PHIC_ID = "Yp6gJAdu4yX"

PHIC_MEMBERSHIP = "JjFcU1L7Ll1"


###############################################################################
# LOGGER
###############################################################################

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)


###############################################################################
# REQUEST SESSION
###############################################################################

def create_session():

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

    session.mount("http://",adapter)

    session.mount("https://",adapter)

    session.auth=(USERNAME,PASSWORD)

    session.verify=VERIFY_SSL

    session.headers.update({

        "Accept":"application/json"

    })

    return session


###############################################################################
# DHIS2 CLIENT
###############################################################################

class DHIS2Client:

    def __init__(self):

        self.session=create_session()

    ###########################################################################

    def get(self,endpoint,params=None):

        url=f"{DHIS2_URL.rstrip('/')}/{endpoint.lstrip('/')}"

        r=self.session.get(

            url,

            params=params,

            timeout=TIMEOUT

        )

        r.raise_for_status()

        return r.json()

    ###########################################################################

    def get_total_pages(

            self,

            program,

            orgunit

    ):

        params={

            "program":program,

            "orgUnit":orgunit,

            "ouMode":"DESCENDANTS",

            "page":1,

            "pageSize":1

        }

        data=self.get(

            "/api/trackedEntityInstances",

            params=params

        )

        pager=data.get("pager",{})

        return pager.get("pageCount",1)

    ###########################################################################

    def get_page(

            self,

            program,

            orgunit,

            page

    ):

        params={

            "program":program,

            "orgUnit":orgunit,

            "ouMode":"DESCENDANTS",

            "page":page,

            "pageSize":PAGE_SIZE,

            "fields":"*"

        }

        return self.get(

            "/api/trackedEntityInstances",
            "/api/tracker/trackedEntities",

            params=params

        )


###############################################################################
# ATTRIBUTE HELPERS
###############################################################################

def attributes_to_dict(attributes):

    result={}

    if attributes is None:

        return result

    for a in attributes:

        result[a["attribute"]]=a.get("value","")

    return result


###############################################################################
# CSV HEADER
###############################################################################

CSV_HEADER=[

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

"Extension",

"Relationship",

"Sex",

"DOB",

"Ethnicity",

"PhilSys ID",

"PhilSys Membership",

"PHIC ID",

"PHIC Membership"

]

###############################################################################
# END OF PART 1
###############################################################################

###############################################################################
# DOWNLOAD HOUSEHOLDS
###############################################################################

def get_households(client, org_unit):
    """
    Download all households for the selected Org Unit.

    Returns
    -------
    dict

    {
        household_tei_uid:{
            household_orgunit_uid,
            household_orgunit_name,
            household_head,
            purok,
            street,
            contact
        }
    }
    """

    logger.info("Downloading Households...")

    households = {}

    page = 1

    while True:

        params = {

            "program": HOUSEHOLD_PROGRAM,

            "orgUnit": org_unit,

            "ouMode": "DESCENDANTS",

            "page": page,

            "pageSize": PAGE_SIZE,

            "skipPaging": "false",

            "fields":
                "trackedEntity,"
                "orgUnit,"
                "attributes"

        }

        data = client.get(
            "/api/tracker/trackedEntities",
            params
        )

        teis = data.get("instances", [])

        if len(teis) == 0:
            break

        logger.info(
            f"Household Page {page} : {len(teis)} records"
        )

        for tei in teis:

            attr = attributes_to_dict(
                tei.get("attributes", [])
            )

            households[
                tei["trackedEntity"]
                #tei["trackedEntityInstance"]

            ] = {

                "household_orgunit_uid":
                    tei.get("orgUnit", ""),

                "household_orgunit_name":
                    "",

                "household_head":
                    attr.get(HH_HEAD, ""),

                "purok":
                    attr.get(HH_PUROK, ""),

                "street":
                    attr.get(HH_STREET, ""),

                "contact":
                    attr.get(HH_CONTACT, "")

            }

        page += 1

    logger.info(
        f"Total Households : {len(households)}"
    )

    return households


###############################################################################
# GET ORG UNIT NAMES
###############################################################################

def populate_orgunit_names(client, households):
    """
    Converts OrgUnit UID into OrgUnit Name
    """

    logger.info("Downloading Organisation Units...")

    cache = {}

    for hh in tqdm(households.values()):

        uid = hh["household_orgunit_uid"]

        if uid in cache:

            hh["household_orgunit_name"] = cache[uid]

            continue

        data = client.get(
            f"/api/organisationUnits/{uid}",
            {
                "fields": "id,name"
            }
        )

        name = data.get("name", "")

        cache[uid] = name

        hh["household_orgunit_name"] = name

    logger.info(
        f"Organisation Units : {len(cache)}"
    )


###############################################################################
# HOUSEHOLD SUMMARY
###############################################################################

def print_household_summary(households):

    print()

    print("=" * 60)

    print("HOUSEHOLD SUMMARY")

    print("=" * 60)

    print()

    print(
        "Total Households :",
        len(households)
    )

    print()

    if len(households):

        sample = next(iter(households.values()))

        print("Example Household")

        print(json.dumps(
            sample,
            indent=4
        ))

        print()

###############################################################################
# END OF PART 2
###############################################################################

###############################################################################
# DOWNLOAD HOUSEHOLD MEMBERS
###############################################################################

def get_household_members(client, org_unit, households, csv_writer):
    """
    Download Household Members, merge with Household information,
    and write matching rows directly to the CSV.

    Parameters
    ----------
    client : DHIS2Client

    org_unit : str

    households : dict

    csv_writer : csv.writer
    """

    logger.info("Downloading Household Members...")

    page = 1

    total_members = 0

    exported = 0

    while True:

        params = {

            "program": HOUSEHOLD_MEMBER_PROGRAM,

            "orgUnit": org_unit,

            "ouMode": "DESCENDANTS",

            "page": page,

            "pageSize": PAGE_SIZE,

            "fields": "*"

        }

        data = client.get(

            "/api/trackedEntityInstances",

            params=params

        )

        teis = data.get("trackedEntityInstances", [])

        if not teis:

            break

        logger.info(
            f"Member Page {page} : {len(teis)} records"
        )

        for tei in teis:

            total_members += 1

            attrs = attributes_to_dict(

                tei.get("attributes", [])

            )

            household_uid = attrs.get(
                FAMILY_INFORMATION,
                ""
            )

            # Skip members whose household is not in our selected OU
            if household_uid not in households:
                continue

            hh = households[household_uid]

            csv_writer.writerow([

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

                attrs.get(EXTENSION, ""),

                attrs.get(RELATIONSHIP, ""),

                attrs.get(SEX, ""),

                attrs.get(DOB, ""),

                attrs.get(ETHNICITY, ""),

                attrs.get(PHILSYS_ID, ""),

                attrs.get(PHILSYS_MEMBERSHIP, ""),

                attrs.get(PHIC_ID, ""),

                attrs.get(PHIC_MEMBERSHIP, "")

            ])

            exported += 1

        page += 1

    logger.info("====================================")
    logger.info(f"Members Read     : {total_members}")
    logger.info(f"Members Exported : {exported}")
    logger.info("====================================")

## python household_member_export.py --orgunit=DiszpKrYNg8

#pip install requests tqdm
#python household_member_export.py --orgunit=<ORG_UNIT_UID>
#Household_Member_Export.csv
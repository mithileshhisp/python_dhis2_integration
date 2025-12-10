import requests
import json

# ============================================================
# DHIS2 SERVER CONFIGURATION
# ============================================================

DHIS2_URL = "https://stage.hispindia.org/pmnpis_dev"   # <-- change this
USERNAME = "***"
PASSWORD = "****"

ENDPOINT = "/api/analyticsTableHooks"   # correct for DHIS2 2.40
#https://stage.hispindia.org/pmnpis_dev/api/analyticsTableHooks?paging=false
# select * from tablehook;
# ============================================================
# HOOK DEFINITION
# ============================================================

eventHookPayload = {
    "name": "_analytics_linelist",
    "phase": "ANALYTICS_TABLE_POPULATED",
    "analyticsTableType": "EVENT",
    "sql": "DROP TABLE IF EXISTS _pmnp_linelist; CREATE TABLE _pmnp_linelist AS SELECT (SELECT name FROM organisationunit WHERE uid = uidlevel2) AS region, ounamehierarchy, ouname, DATE(executiondate) AS visitdate, \"RDQQ3t9oXw5\" AS \"Household_UID\", \"NOKzq4dAKF7\" AS \"PMNP_ID\", \"PIGLwIaw0wy\" AS \"First_name\", \"WC0cShCpae8\" AS \"Middle_name\", \"IENWcinF8lM\" AS \"Last_name\", \"nyVsU3fTk2b\" AS \"Extension_name\", \"fJPZFs2yYJQ\" AS \"Date_of_Birth\", \"H42aYY9JMIR\" AS \"Age_in_years\", \"X2Oln1OyP5o\" AS \"Age_in_months\", \"xDSSvssuNFs\" AS \"Age_in_weeks\", \"d2n5w4zpxuo\" AS \"Age_in_days\", \"VQ9dyZbj843\" AS \"TTD1_vaccine_date\", \"sBzNt7bbggE\" AS \"TTD2_vaccine_date\", \"EeL84itsEVm\" AS \"TTD3_vaccine_date\", \"dxM5jWLEKXq\" AS \"TTD4_vaccine_date\", \"lRI8oJTn3jL\" AS \"TTD5_vaccine_date\", \"ycBIHr9bYyw\" AS \"HHM_Pregnancy_status\", \"wqR0L5WGV6S\" AS \"PW_HF_visit_for_prenatal_checkup\", \"M5nofSFKw1e\" AS \"PW_1st_HF_visit_for_prenatal_checkup\", \"AZXJKuGOM6n\" AS \"PW_2nd_HF_visit_for_prenatal_checkup\", \"MR4IiYlxfsx\" AS \"PW_3rd_HF_visit_for_prenatal_checkup\", \"ZMjGmieu8Iz\" AS \"PW_4th_HF_visit_for_prenatal_checkup\", \"Bdd2wmXbizw\" AS \"PW_5th_HF_visit_for_prenatal_checkup\", \"Plkdcpkb04F\" AS \"PW_6th_HF_visit_for_prenatal_checkup\", \"AG21Y0hmrAu\" AS \"PW_7th_HF_visit_for_prenatal_checkup\", \"RAWt5NBWtvB\" AS \"PW_8th_HF_visit_for_prenatal_checkup\", \"AO4P3pcKqek\" AS \"PW_Iron_folic_acid_or_multiple_micronutrient\", \"ZkoIX2TigZA\" AS \"PW_Medicine_taken_for_intestinal_worms\", \"cMg8stHS4aH\" AS \"PW_Injection_for_tetanus_given\", \"se8TXlLUzh8\" AS \"HHM_Postpartum\", \"rvv5Hfyczyh\" AS \"HHM_Date_of_Delivery_(Postpartum)\", \"mT44qeiiVpv\" AS \"MC_HF_visit_for_prenatal_checkup\", \"l23OPIamSVU\" AS \"PPW_1st_HF_visit_for_prenatal_checkup\", \"WdfB53AeOSD\" AS \"PPW_2nd_HF_visit_for_prenatal_checkup\", \"vPHSleGlsCM\" AS \"PPW_3rd_HF_visit_for_prenatal_checkup\", \"ciExesjoFlQ\" AS \"PPW_4th_HF_visit_for_prenatal_checkup\", \"LrSJ5Je5N9B\" AS \"PPW_5th_HF_visit_for_prenatal_checkup\", \"tTOMrF0wYr3\" AS \"PPW_6th_HF_visit_for_prenatal_checkup\", \"Y2F9wTOlNMM\" AS \"PPW_7th_HF_visit_for_prenatal_checkup\", \"Y3mZGw9YGqr\" AS \"PPW_8th_HF_visit_for_prenatal_checkup\", \"zbbkBO029vE\" AS \"MC_180_allocated_supplements_finished\", \"HK1uGfoC77d\" AS \"MC_Medicine_for_intestinal_worms_taken\", \"tQ9bxb0faAR\" AS \"MC_Tetanus_injection_given\", \"L6IwuUPsbOT\" AS \"PP_Birth_in_HF\", \"jIAwnqn8GTU\" AS \"PP_Consultation_within_24_hours_of_delivery\", \"AhH8CegcpvQ\" AS \"PP_Consultation_within_3_days_of_delivery\", \"sOsvy89ROmD\" AS \"PP_Consultation_within_7-14_days_of_delivery\", \"EadgXIE9RbC\" AS \"PP_Consultation_within_6_weeks_of_delivery\", \"SMfz85dxBrG\" AS \"CN_Child_exclusively_breastfed_in_24_hours\", \"RLms3EMK6Lx\" AS \"Adequate_Diet_Diversity\", \"YJEM6K4r8B6\" AS \"CN_Child_consumed_breastmilk_yesterday\", \"aIMeDdwzVQQ\" AS \"CN_Child_consumed_grains_yesterday\", \"nVFnpIJFBtP\" AS \"CN_Child_consumed_legumes_yesterday\", \"iiAjifuwYOE\" AS \"CN_Child_consumed_dairy_yesterday\", \"hQgU2xbT2CL\" AS \"CN_Child_consumed_flesh_foods_yesterday\", \"xbPC3AWgDrB\" AS \"CN_Child_consumed_eggs_yesterday\", \"qfYU7s0EylE\" AS \"CN_Consumed_Vitamin_A_rich_fruits_and_vegetables\", \"ZxGgsjfOje1\" AS \"CN_Consumed_other_fruits_and_vegetables\", \"saTG1WrWtEW\" AS \"CN_Child_given_micronutrient_powder\", \"JoD2AagclsB\" AS \"CN_Child_given_Vitamin_A\", \"YgK3LWUrA6f\" AS \"CN_Weight_and_height_monitored\", \"uYWxyRYP7GN\" AS \"CN_Follow_up_monitoring_date\", \"EMHed4Yi7L6\" AS \"CH_Age_appropriate_vaccine_given\", \"Wj1Re9XKW5P\" AS \"CN_Weight_for_age\", \"TON0hSWcaw7\" AS \"CN_Length_or_Height_for_age\", \"RXWSlNxAwq1\" AS \"CN_Weight_for_height_status\", \"s3q2EVu3qe0\" AS \"CN_MUAC_findings\" FROM analytics_event_temp_vvlirjoogbj WHERE uidlevel2 NOT IN ('zqTkGmyJZeh');"
}

eventHookPayload_hh_member = {
    "name": "_analytics_linelist_hh_member",
    "phase": "ANALYTICS_TABLE_POPULATED",
    "analyticsTableType": "EVENT",
    "sql": "drop table if exists _pmnp_linelist_hh_member; create table _pmnp_linelist_hh_member as select (select name from organisationunit where uid=uidlevel2) as region,(select name from organisationunit where uid=uidlevel3) as province,(select name from organisationunit where uid=uidlevel4) as municipality,(select name from organisationunit where uid=uidlevel5) as barangay, ou as orguid, ounamehierarchy, ouname, date(executiondate) as visitdate, \"RDQQ3t9oXw5\" as \"Household_UID\", \"NOKzq4dAKF7\" as \"PMNP_ID\", \"PIGLwIaw0wy\" as \"First_name\", \"WC0cShCpae8\" as \"Middle_name\", \"IENWcinF8lM\" as \"Last_name\", \"nyVsU3fTk2b\" as \"Extension_name\", \"fJPZFs2yYJQ\" as \"Date_of_Birth\", \"H42aYY9JMIR\" as \"Age_in_years\", \"X2Oln1OyP5o\" as \"Age_in_months\", \"xDSSvssuNFs\" as \"Age_in_weeks\", \"d2n5w4zpxuo\" as \"Age_in_days\", \"VQ9dyZbj843\" as \"TTD1_vaccine_date\", \"sBzNt7bbggE\" as \"TTD2_vaccine_date\", \"EeL84itsEVm\" as \"TTD3_vaccine_date\", \"dxM5jWLEKXq\" as \"TTD4_vaccine_date\", \"lRI8oJTn3jL\" as \"TTD5_vaccine_date\", \"ycBIHr9bYyw\" as \"HHM_Pregnancy_status\", \"wqR0L5WGV6S\" as \"PW_HF_visit_for_prenatal_checkup\", \"M5nofSFKw1e\" as \"PW_1st_HF_visit_for_prenatal_checkup\", \"AZXJKuGOM6n\" as \"PW_2nd_HF_visit_for_prenatal_checkup\", \"MR4IiYlxfsx\" as \"PW_3rd_HF_visit_for_prenatal_checkup\", \"ZMjGmieu8Iz\" as \"PW_4th_HF_visit_for_prenatal_checkup\", \"Bdd2wmXbizw\" as \"PW_5th_HF_visit_for_prenatal_checkup\", \"Plkdcpkb04F\" as \"PW_6th_HF_visit_for_prenatal_checkup\", \"AG21Y0hmrAu\" as \"PW_7th_HF_visit_for_prenatal_checkup\", \"RAWt5NBWtvB\" as \"PW_8th_HF_visit_for_prenatal_checkup\", \"AO4P3pcKqek\" as \"PW_Iron_folic_acid_or_multiple_micronutrient\", \"ZkoIX2TigZA\" as \"PW_Medicine_taken_for_intestinal_worms\", \"cMg8stHS4aH\" as \"PW_Injection_for_tetanus_given\", \"se8TXlLUzh8\" as \"HHM_Postpartum\", \"rvv5Hfyczyh\" as \"HHM_Date_of_Delivery_(Postpartum)\", \"mT44qeiiVpv\" as \"MC_HF_visit_for_prenatal_checkup\", \"l23OPIamSVU\" as \"PPW_1st_HF_visit_for_prenatal_checkup\", \"WdfB53AeOSD\" as \"PPW_2nd_HF_visit_for_prenatal_checkup\", \"vPHSleGlsCM\" as \"PPW_3rd_HF_visit_for_prenatal_checkup\", \"ciExesjoFlQ\" as \"PPW_4th_HF_visit_for_prenatal_checkup\", \"LrSJ5Je5N9B\" as \"PPW_5th_HF_visit_for_prenatal_checkup\", \"tTOMrF0wYr3\" as \"PPW_6th_HF_visit_for_prenatal_checkup\", \"Y2F9wTOlNMM\" as \"PPW_7th_HF_visit_for_prenatal_checkup\", \"Y3mZGw9YGqr\" as \"PPW_8th_HF_visit_for_prenatal_checkup\", \"zbbkBO029vE\" as \"MC_180_allocated_supplements_finished\", \"HK1uGfoC77d\" as \"MC_Medicine_for_intestinal_worms_taken\", \"tQ9bxb0faAR\" as \"MC_Tetanus_injection_given\", \"L6IwuUPsbOT\" as \"PP_Birth_in_HF\", \"jIAwnqn8GTU\" as \"PP_Consultation_within_24_hours_of_delivery\", \"AhH8CegcpvQ\" as \"PP_Consultation_within_3_days_of_delivery\", \"sOsvy89ROmD\" as \"PP_Consultation_within_7-14_days_of_delivery\", \"EadgXIE9RbC\" as \"PP_Consultation_within_6_weeks_of_delivery\", \"SMfz85dxBrG\" as \"CN_Child_exclusively_breastfed_in_24_hours\", \"RLms3EMK6Lx\" as \"Adequate_Diet_Diversity\", \"YJEM6K4r8B6\" as \"CN_Child_consumed_breastmilk_yesterday\", \"aIMeDdwzVQQ\" as \"CN_Child_consumed_grains_yesterday\", \"nVFnpIJFBtP\" as \"CN_Child_consumed_legumes_yesterday\", \"iiAjifuwYOE\" as \"CN_Child_consumed_dairy_yesterday\", \"hQgU2xbT2CL\" as \"CN_Child_consumed_flesh_foods_yesterday\", \"xbPC3AWgDrB\" as \"CN_Child_consumed_eggs_yesterday\", \"qfYU7s0EylE\" as \"CN_Consumed_Vitamin_A_rich_fruits_and_vegetables\", \"ZxGgsjfOje1\" as \"CN_Consumed_other_fruits_and_vegetables\", \"saTG1WrWtEW\" as \"CN_Child_given_micronutrient_powder\", \"JoD2AagclsB\" as \"CN_Child_given_Vitamin_A\", \"YgK3LWUrA6f\" as \"CN_Weight_and_height_monitored\", \"uYWxyRYP7GN\" as \"CN_Follow_up_monitoring_date\", \"EMHed4Yi7L6\" as \"CH_Age_appropriate_vaccine_given\", \"Wj1Re9XKW5P\" as \"CN_Weight_for_age\", \"TON0hSWcaw7\" as \"CN_Length_or_Height_for_age\", \"RXWSlNxAwq1\" as \"CN_Weight_for_height_status\", \"s3q2EVu3qe0\" as \"CN_MUAC_findings\" from analytics_event_temp_vvlirjoogbj where uidlevel2 not in ('zqTkGmyJZeh')"

}

# ============================================================
# SEND REQUEST
# ============================================================

response = requests.post(
    DHIS2_URL + ENDPOINT,
    auth=(USERNAME, PASSWORD),
    headers={"Content-Type": "application/json"},
    data=json.dumps(eventHookPayload_hh_member)
)


# ============================================================
# RESULT
# ============================================================

print("Status Code:", response.status_code)
try:
    print(response.json())
except:
    print(response.text)

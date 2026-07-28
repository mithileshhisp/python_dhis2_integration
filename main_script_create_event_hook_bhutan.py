import requests
import json

# ============================================================
# DHIS2 SERVER CONFIGURATION
# ============================================================
# select * from tablehook;
#DHIS2_URL = "https://stage.hispindia.org/pmnpis_dev"   # <-- change this
DHIS2_URL = "https://hhs.drukhmis.gov.bt/bhutan_hhs"   # <-- change this production
USERNAME = "*****"
PASSWORD = "******"

ENDPOINT = "/api/analyticsTableHooks"   # correct for DHIS2 2.40
#https://hhs.drukhmis.gov.bt/bhutan_hhs/api/analyticsTableHooks?paging=false&fields=*
#https://hhs.drukhmis.gov.bt/bhutan_hhs/api/analyticsTableHooks?paging=false&fields=*
#https://hhs.drukhmis.gov.bt/bhutan_hhs/api/analyticsTableHooks?paging=false&fields=*

# select * from tablehook;
# ============================================================
# HOOK DEFINITION
# ============================================================

print("Event Hook Creation Start")

eventHookPayload = {
    "name": "_analytics_linelist",
    "phase": "ANALYTICS_TABLE_POPULATED",
    "analyticsTableType": "EVENT",
    "sql": "DROP TABLE IF EXISTS _pmnp_linelist; CREATE TABLE _pmnp_linelist AS SELECT (SELECT name FROM organisationunit WHERE uid = uidlevel2) AS region, ounamehierarchy, ouname, DATE(executiondate) AS visitdate, \"RDQQ3t9oXw5\" AS \"Household_UID\", \"NOKzq4dAKF7\" AS \"PMNP_ID\", \"PIGLwIaw0wy\" AS \"First_name\", \"WC0cShCpae8\" AS \"Middle_name\", \"IENWcinF8lM\" AS \"Last_name\", \"nyVsU3fTk2b\" AS \"Extension_name\", \"fJPZFs2yYJQ\" AS \"Date_of_Birth\", \"H42aYY9JMIR\" AS \"Age_in_years\", \"X2Oln1OyP5o\" AS \"Age_in_months\", \"xDSSvssuNFs\" AS \"Age_in_weeks\", \"d2n5w4zpxuo\" AS \"Age_in_days\", \"VQ9dyZbj843\" AS \"TTD1_vaccine_date\", \"sBzNt7bbggE\" AS \"TTD2_vaccine_date\", \"EeL84itsEVm\" AS \"TTD3_vaccine_date\", \"dxM5jWLEKXq\" AS \"TTD4_vaccine_date\", \"lRI8oJTn3jL\" AS \"TTD5_vaccine_date\", \"ycBIHr9bYyw\" AS \"HHM_Pregnancy_status\", \"wqR0L5WGV6S\" AS \"PW_HF_visit_for_prenatal_checkup\", \"M5nofSFKw1e\" AS \"PW_1st_HF_visit_for_prenatal_checkup\", \"AZXJKuGOM6n\" AS \"PW_2nd_HF_visit_for_prenatal_checkup\", \"MR4IiYlxfsx\" AS \"PW_3rd_HF_visit_for_prenatal_checkup\", \"ZMjGmieu8Iz\" AS \"PW_4th_HF_visit_for_prenatal_checkup\", \"Bdd2wmXbizw\" AS \"PW_5th_HF_visit_for_prenatal_checkup\", \"Plkdcpkb04F\" AS \"PW_6th_HF_visit_for_prenatal_checkup\", \"AG21Y0hmrAu\" AS \"PW_7th_HF_visit_for_prenatal_checkup\", \"RAWt5NBWtvB\" AS \"PW_8th_HF_visit_for_prenatal_checkup\", \"AO4P3pcKqek\" AS \"PW_Iron_folic_acid_or_multiple_micronutrient\", \"ZkoIX2TigZA\" AS \"PW_Medicine_taken_for_intestinal_worms\", \"cMg8stHS4aH\" AS \"PW_Injection_for_tetanus_given\", \"se8TXlLUzh8\" AS \"HHM_Postpartum\", \"rvv5Hfyczyh\" AS \"HHM_Date_of_Delivery_(Postpartum)\", \"mT44qeiiVpv\" AS \"MC_HF_visit_for_prenatal_checkup\", \"l23OPIamSVU\" AS \"PPW_1st_HF_visit_for_prenatal_checkup\", \"WdfB53AeOSD\" AS \"PPW_2nd_HF_visit_for_prenatal_checkup\", \"vPHSleGlsCM\" AS \"PPW_3rd_HF_visit_for_prenatal_checkup\", \"ciExesjoFlQ\" AS \"PPW_4th_HF_visit_for_prenatal_checkup\", \"LrSJ5Je5N9B\" AS \"PPW_5th_HF_visit_for_prenatal_checkup\", \"tTOMrF0wYr3\" AS \"PPW_6th_HF_visit_for_prenatal_checkup\", \"Y2F9wTOlNMM\" AS \"PPW_7th_HF_visit_for_prenatal_checkup\", \"Y3mZGw9YGqr\" AS \"PPW_8th_HF_visit_for_prenatal_checkup\", \"zbbkBO029vE\" AS \"MC_180_allocated_supplements_finished\", \"HK1uGfoC77d\" AS \"MC_Medicine_for_intestinal_worms_taken\", \"tQ9bxb0faAR\" AS \"MC_Tetanus_injection_given\", \"L6IwuUPsbOT\" AS \"PP_Birth_in_HF\", \"jIAwnqn8GTU\" AS \"PP_Consultation_within_24_hours_of_delivery\", \"AhH8CegcpvQ\" AS \"PP_Consultation_within_3_days_of_delivery\", \"sOsvy89ROmD\" AS \"PP_Consultation_within_7-14_days_of_delivery\", \"EadgXIE9RbC\" AS \"PP_Consultation_within_6_weeks_of_delivery\", \"SMfz85dxBrG\" AS \"CN_Child_exclusively_breastfed_in_24_hours\", \"RLms3EMK6Lx\" AS \"Adequate_Diet_Diversity\", \"YJEM6K4r8B6\" AS \"CN_Child_consumed_breastmilk_yesterday\", \"aIMeDdwzVQQ\" AS \"CN_Child_consumed_grains_yesterday\", \"nVFnpIJFBtP\" AS \"CN_Child_consumed_legumes_yesterday\", \"iiAjifuwYOE\" AS \"CN_Child_consumed_dairy_yesterday\", \"hQgU2xbT2CL\" AS \"CN_Child_consumed_flesh_foods_yesterday\", \"xbPC3AWgDrB\" AS \"CN_Child_consumed_eggs_yesterday\", \"qfYU7s0EylE\" AS \"CN_Consumed_Vitamin_A_rich_fruits_and_vegetables\", \"ZxGgsjfOje1\" AS \"CN_Consumed_other_fruits_and_vegetables\", \"saTG1WrWtEW\" AS \"CN_Child_given_micronutrient_powder\", \"JoD2AagclsB\" AS \"CN_Child_given_Vitamin_A\", \"YgK3LWUrA6f\" AS \"CN_Weight_and_height_monitored\", \"uYWxyRYP7GN\" AS \"CN_Follow_up_monitoring_date\", \"EMHed4Yi7L6\" AS \"CH_Age_appropriate_vaccine_given\", \"Wj1Re9XKW5P\" AS \"CN_Weight_for_age\", \"TON0hSWcaw7\" AS \"CN_Length_or_Height_for_age\", \"RXWSlNxAwq1\" AS \"CN_Weight_for_height_status\", \"s3q2EVu3qe0\" AS \"CN_MUAC_findings\" FROM analytics_event_temp_vvlirjoogbj WHERE uidlevel2 NOT IN ('zqTkGmyJZeh') AND ps = 'QfXSvc9HtKN';"
}

eventHookPayload_hh_member = {
    "name": "_analytics_linelist_hh_member",
    "phase": "ANALYTICS_TABLE_POPULATED",
    "analyticsTableType": "EVENT",
    "sql": "drop table if exists _pmnp_linelist_hh_member; create table _pmnp_linelist_hh_member as select (select name from organisationunit where uid=uidlevel2) as region,(select name from organisationunit where uid=uidlevel3) as province,(select name from organisationunit where uid=uidlevel4) as municipality,(select name from organisationunit where uid=uidlevel5) as barangay, ou as orguid, ounamehierarchy, ouname, date(executiondate) as visitdate, \"RDQQ3t9oXw5\" as \"Household_UID\", \"NOKzq4dAKF7\" as \"PMNP_ID\", \"PIGLwIaw0wy\" as \"First_name\", \"WC0cShCpae8\" as \"Middle_name\", \"IENWcinF8lM\" as \"Last_name\", \"nyVsU3fTk2b\" as \"Extension_name\", \"fJPZFs2yYJQ\" as \"Date_of_Birth\", \"H42aYY9JMIR\" as \"Age_in_years\", \"X2Oln1OyP5o\" as \"Age_in_months\", \"xDSSvssuNFs\" as \"Age_in_weeks\", \"d2n5w4zpxuo\" as \"Age_in_days\", \"VQ9dyZbj843\" as \"TTD1_vaccine_date\", \"sBzNt7bbggE\" as \"TTD2_vaccine_date\", \"EeL84itsEVm\" as \"TTD3_vaccine_date\", \"dxM5jWLEKXq\" as \"TTD4_vaccine_date\", \"lRI8oJTn3jL\" as \"TTD5_vaccine_date\", \"ycBIHr9bYyw\" as \"HHM_Pregnancy_status\", \"wqR0L5WGV6S\" as \"PW_HF_visit_for_prenatal_checkup\", \"M5nofSFKw1e\" as \"PW_1st_HF_visit_for_prenatal_checkup\", \"AZXJKuGOM6n\" as \"PW_2nd_HF_visit_for_prenatal_checkup\", \"MR4IiYlxfsx\" as \"PW_3rd_HF_visit_for_prenatal_checkup\", \"ZMjGmieu8Iz\" as \"PW_4th_HF_visit_for_prenatal_checkup\", \"Bdd2wmXbizw\" as \"PW_5th_HF_visit_for_prenatal_checkup\", \"Plkdcpkb04F\" as \"PW_6th_HF_visit_for_prenatal_checkup\", \"AG21Y0hmrAu\" as \"PW_7th_HF_visit_for_prenatal_checkup\", \"RAWt5NBWtvB\" as \"PW_8th_HF_visit_for_prenatal_checkup\", \"AO4P3pcKqek\" as \"PW_Iron_folic_acid_or_multiple_micronutrient\", \"ZkoIX2TigZA\" as \"PW_Medicine_taken_for_intestinal_worms\", \"cMg8stHS4aH\" as \"PW_Injection_for_tetanus_given\", \"se8TXlLUzh8\" as \"HHM_Postpartum\", \"rvv5Hfyczyh\" as \"HHM_Date_of_Delivery_(Postpartum)\", \"mT44qeiiVpv\" as \"MC_HF_visit_for_prenatal_checkup\", \"l23OPIamSVU\" as \"PPW_1st_HF_visit_for_prenatal_checkup\", \"WdfB53AeOSD\" as \"PPW_2nd_HF_visit_for_prenatal_checkup\", \"vPHSleGlsCM\" as \"PPW_3rd_HF_visit_for_prenatal_checkup\", \"ciExesjoFlQ\" as \"PPW_4th_HF_visit_for_prenatal_checkup\", \"LrSJ5Je5N9B\" as \"PPW_5th_HF_visit_for_prenatal_checkup\", \"tTOMrF0wYr3\" as \"PPW_6th_HF_visit_for_prenatal_checkup\", \"Y2F9wTOlNMM\" as \"PPW_7th_HF_visit_for_prenatal_checkup\", \"Y3mZGw9YGqr\" as \"PPW_8th_HF_visit_for_prenatal_checkup\", \"zbbkBO029vE\" as \"MC_180_allocated_supplements_finished\", \"HK1uGfoC77d\" as \"MC_Medicine_for_intestinal_worms_taken\", \"tQ9bxb0faAR\" as \"MC_Tetanus_injection_given\", \"L6IwuUPsbOT\" as \"PP_Birth_in_HF\", \"jIAwnqn8GTU\" as \"PP_Consultation_within_24_hours_of_delivery\", \"AhH8CegcpvQ\" as \"PP_Consultation_within_3_days_of_delivery\", \"sOsvy89ROmD\" as \"PP_Consultation_within_7-14_days_of_delivery\", \"EadgXIE9RbC\" as \"PP_Consultation_within_6_weeks_of_delivery\", \"SMfz85dxBrG\" as \"CN_Child_exclusively_breastfed_in_24_hours\", \"RLms3EMK6Lx\" as \"Adequate_Diet_Diversity\", \"YJEM6K4r8B6\" as \"CN_Child_consumed_breastmilk_yesterday\", \"aIMeDdwzVQQ\" as \"CN_Child_consumed_grains_yesterday\", \"nVFnpIJFBtP\" as \"CN_Child_consumed_legumes_yesterday\", \"iiAjifuwYOE\" as \"CN_Child_consumed_dairy_yesterday\", \"hQgU2xbT2CL\" as \"CN_Child_consumed_flesh_foods_yesterday\", \"xbPC3AWgDrB\" as \"CN_Child_consumed_eggs_yesterday\", \"qfYU7s0EylE\" as \"CN_Consumed_Vitamin_A_rich_fruits_and_vegetables\", \"ZxGgsjfOje1\" as \"CN_Consumed_other_fruits_and_vegetables\", \"saTG1WrWtEW\" as \"CN_Child_given_micronutrient_powder\", \"JoD2AagclsB\" as \"CN_Child_given_Vitamin_A\", \"YgK3LWUrA6f\" as \"CN_Weight_and_height_monitored\", \"uYWxyRYP7GN\" as \"CN_Follow_up_monitoring_date\", \"EMHed4Yi7L6\" as \"CH_Age_appropriate_vaccine_given\", \"Wj1Re9XKW5P\" as \"CN_Weight_for_age\", \"TON0hSWcaw7\" as \"CN_Length_or_Height_for_age\", \"RXWSlNxAwq1\" as \"CN_Weight_for_height_status\", \"s3q2EVu3qe0\" as \"CN_MUAC_findings\" from analytics_event_temp_vvlirjoogbj where uidlevel2 not in ('zqTkGmyJZeh') AND ps = 'QfXSvc9HtKN'; "

}

'''
eventHookPayload_hh_member_updated = {
    "id": "ROr6zdm4HQb",
    "name": "_analytics_linelist_hh_member",
    "phase": "ANALYTICS_TABLE_POPULATED",
    "analyticsTableType": "EVENT",
    "sql": "drop table if exists _pmnp_linelist_hh_member; create table _pmnp_linelist_hh_member as select (select name from organisationunit where uid=uidlevel2) as region,(select name from organisationunit where uid=uidlevel3) as province,(select name from organisationunit where uid=uidlevel4) as municipality, (select name from organisationunit where uid=uidlevel5) as barangay, ou as orguid, ounamehierarchy,ouname,date(executiondate) as visitdate,  \"RDQQ3t9oXw5\" as \"Household_UID\",\"NOKzq4dAKF7\" as \"PMNP_ID\",\"PIGLwIaw0wy\" as \"First_name\",\"WC0cShCpae8\" as \"Middle_name\",\"IENWcinF8lM\" as \"Last_name\",\"nyVsU3fTk2b\" as \"Extension_name\",\"fJPZFs2yYJQ\" as \"Date_of_Birth\",\"H42aYY9JMIR\" as \"Age_in_years\",\"X2Oln1OyP5o\" as \"Age_in_months\",\"xDSSvssuNFs\" as \"Age_in_weeks\",\"d2n5w4zpxuo\" as \"Age_in_days\",\"VQ9dyZbj843\" as \"TTD1_vaccine_date\",\"sBzNt7bbggE\" as \"TTD2_vaccine_date\",\"EeL84itsEVm\" as \"TTD3_vaccine_date\",\"dxM5jWLEKXq\" as \"TTD4_vaccine_date\",\"lRI8oJTn3jL\" as \"TTD5_vaccine_date\", (select \"ycBIHr9bYyw\" from analytics_event_temp_vvlirjoogbj  where ps='LRJrFeDNEdT' and tei=dd.tei and executiondate=dd.executiondate order by created desc limit 1) as \"HHM_Pregnancy_status\",\"wqR0L5WGV6S\" as \"PW_HF_visit_for_prenatal_checkup\",\"M5nofSFKw1e\" as \"PW_1st_HF_visit_for_prenatal_checkup\",\"AZXJKuGOM6n\" as \"PW_2nd_HF_visit_for_prenatal_checkup\",\"MR4IiYlxfsx\" as \"PW_3rd_HF_visit_for_prenatal_checkup\",\"ZMjGmieu8Iz\" as \"PW_4th_HF_visit_for_prenatal_checkup\",\"Bdd2wmXbizw\" as \"PW_5th_HF_visit_for_prenatal_checkup\",\"Plkdcpkb04F\" as \"PW_6th_HF_visit_for_prenatal_checkup\",\"AG21Y0hmrAu\" as \"PW_7th_HF_visit_for_prenatal_checkup\",\"RAWt5NBWtvB\" as \"PW_8th_HF_visit_for_prenatal_checkup\",\"AO4P3pcKqek\" as \"PW_Iron_folic_acid_or_multiple_micronutrient\",\"ZkoIX2TigZA\" as \"PW_Medicine_taken_for_intestinal_worms\",\"cMg8stHS4aH\" as \"PW_Injection_for_tetanus_given\",(select \"se8TXlLUzh8\" from analytics_event_temp_vvlirjoogbj  where ps='LRJrFeDNEdT' and tei=dd.tei and executiondate=dd.executiondate order by created desc limit 1) as \"HHM_Postpartum\",(select \"rvv5Hfyczyh\" from analytics_event_temp_vvlirjoogbj  where ps='LRJrFeDNEdT' and tei=dd.tei and executiondate=dd.executiondate order by created desc limit 1) as \"HHM_Date_of_Delivery_(Postpartum)\",\"mT44qeiiVpv\" as \"MC_HF_visit_for_prenatal_checkup\",\"l23OPIamSVU\" as \"PPW_1st_HF_visit_for_prenatal_checkup\",\"WdfB53AeOSD\" as \"PPW_2nd_HF_visit_for_prenatal_checkup\",\"vPHSleGlsCM\" as \"PPW_3rd_HF_visit_for_prenatal_checkup\",\"ciExesjoFlQ\" as \"PPW_4th_HF_visit_for_prenatal_checkup\",\"LrSJ5Je5N9B\" as \"PPW_5th_HF_visit_for_prenatal_checkup\",\"tTOMrF0wYr3\" as \"PPW_6th_HF_visit_for_prenatal_checkup\",\"Y2F9wTOlNMM\" as \"PPW_7th_HF_visit_for_prenatal_checkup\",\"Y3mZGw9YGqr\" as \"PPW_8th_HF_visit_for_prenatal_checkup\",\"zbbkBO029vE\" as \"MC_180_allocated_supplements_finished\",\"HK1uGfoC77d\" as \"MC_Medicine_for_intestinal_worms_taken\",\"tQ9bxb0faAR\" as \"MC_Tetanus_injection_given\",\"L6IwuUPsbOT\" as \"PP_Birth_in_HF\",\"jIAwnqn8GTU\" as \"PP_Consultation_within_24_hours_of_delivery\",\"AhH8CegcpvQ\" as \"PP_Consultation_within_3_days_of_delivery\",\"sOsvy89ROmD\" as \"PP_Consultation_within_7-14_days_of_delivery\",\"EadgXIE9RbC\" as \"PP_Consultation_within_6_weeks_of_delivery\",\"SMfz85dxBrG\" as \"CN_Child_exclusively_breastfed_in_24_hours\",\"RLms3EMK6Lx\" as \"Adequate_Diet_Diversity\",\"YJEM6K4r8B6\" as \"CN_Child_consumed_breastmilk_yesterday\",\"aIMeDdwzVQQ\" as \"CN_Child_consumed_grains_yesterday\",\"nVFnpIJFBtP\" as \"CN_Child_consumed_legumes_yesterday\",\"iiAjifuwYOE\" as \"CN_Child_consumed_dairy_yesterday\",\"hQgU2xbT2CL\" as \"CN_Child_consumed_flesh_foods_yesterday\",\"xbPC3AWgDrB\" as \"CN_Child_consumed_eggs_yesterday\",\"qfYU7s0EylE\" as \"CN_Consumed_Vitamin_A_rich_fruits_and_vegetables\",\"ZxGgsjfOje1\" as \"CN_Consumed_other_fruits_and_vegetables\",\"saTG1WrWtEW\" as \"CN_Child_given_micronutrient_powder\",\"JoD2AagclsB\" as \"CN_Child_given_Vitamin_A\",\"YgK3LWUrA6f\" as \"CN_Weight_and_height_monitored\",\"uYWxyRYP7GN\" as \"CN_Follow_up_monitoring_date\",\"EMHed4Yi7L6\" as \"CH_Age_appropriate_vaccine_given\",\"Wj1Re9XKW5P\" as \"CN_Weight_for_age\",\"TON0hSWcaw7\" as \"CN_Length_or_Height_for_age\",\"RXWSlNxAwq1\" as \"CN_Weight_for_height_status\",\"s3q2EVu3qe0\" as \"CN_MUAC_findings\" from analytics_event_temp_vvlirjoogbj dd where uidlevel2 not in ('zqTkGmyJZeh') and ps='QfXSvc9HtKN'"
}


eventHookPayload_hh_member_updated = {
    "id": "ROr6zdm4HQb",
    "name": "_analytics_linelist_hh_member",
    "phase": "ANALYTICS_TABLE_POPULATED",
    "analyticsTableType": "EVENT",
    
    "sql": """
        drop table if exists _pmnp_linelist_hh_member; create table _pmnp_linelist_hh_member
        WITH latest_hhm AS (
    SELECT DISTINCT ON (tei, executiondate)
           tei,
           executiondate,
           "ycBIHr9bYyw" AS pregnancy_status,
           "se8TXlLUzh8" AS postpartum,
           "rvv5Hfyczyh" AS delivery_date
    FROM analytics_event_temp_vvlirjoogbj
    WHERE ps = 'LRJrFeDNEdT'
    ORDER BY tei, executiondate, created DESC
)
SELECT
    ou.name AS region,
    dd.ounamehierarchy,
    dd.ouname,
    DATE(dd.executiondate) AS visitdate,

    dd."RDQQ3t9oXw5" AS household_uid,
    dd."NOKzq4dAKF7" AS pmnp_id,
    dd."PIGLwIaw0wy" AS first_name,
    dd."WC0cShCpae8" AS middle_name,
    dd."IENWcinF8lM" AS last_name,
    dd."nyVsU3fTk2b" AS extension_name,

    dd."fJPZFs2yYJQ" AS date_of_birth,
    dd."H42aYY9JMIR" AS age_in_years,
    dd."X2Oln1OyP5o" AS age_in_months,
    dd."xDSSvssuNFs" AS age_in_weeks,
    dd."d2n5w4zpxuo" AS age_in_days,

    dd."VQ9dyZbj843" AS ttd1_vaccine_date,
    dd."sBzNt7bbggE" AS ttd2_vaccine_date,
    dd."EeL84itsEVm" AS ttd3_vaccine_date,
    dd."dxM5jWLEKXq" AS ttd4_vaccine_date,
    dd."lRI8oJTn3jL" AS ttd5_vaccine_date,

    hhm.pregnancy_status AS hhm_pregnancy_status,
    dd."wqR0L5WGV6S" AS pw_hf_visit_prenatal,
    dd."M5nofSFKw1e" AS pw_1st_hf_visit,
    dd."AZXJKuGOM6n" AS pw_2nd_hf_visit,
    dd."MR4IiYlxfsx" AS pw_3rd_hf_visit,
    dd."ZMjGmieu8Iz" AS pw_4th_hf_visit,

    hhm.postpartum AS hhm_postpartum,
    hhm.delivery_date AS hhm_delivery_date_postpartum,

    dd."mT44qeiiVpv" AS mc_hf_visit_prenatal,
    dd."l23OPIamSVU" AS ppw_1st_hf_visit,
    dd."WdfB53AeOSD" AS ppw_2nd_hf_visit,
    dd."vPHSleGlsCM" AS ppw_3rd_hf_visit,
    dd."ciExesjoFlQ" AS ppw_4th_hf_visit,

    dd."s3q2EVu3qe0" AS cn_muac_findings

    FROM analytics_event_temp_vvlirjoogbj dd

    LEFT JOIN latest_hhm hhm
       ON hhm.tei = dd.tei
       AND hhm.executiondate = dd.executiondate

    LEFT JOIN organisationunit ou
       ON ou.uid = dd.uidlevel2
    WHERE dd.ps = 'QfXSvc9HtKN'
        AND dd.uidlevel2 <> 'zqTkGmyJZeh';
    """
}
'''

eventHookPayload_house_hold_updated_with_users = {
    #"id": "ROr6zdm4HQb",
    "name": "_analytics_linelist_hh_with_users",
    "phase": "ANALYTICS_TABLE_POPULATED",
    "analyticsTableType": "EVENT",
    
    "sql": """
        drop table if exists _bhutan_linelist_hh CASCADE;
        CREATE TABLE _bhutan_linelist_hh AS
        WITH latest_events AS (
            SELECT
                dd.*,
                ROW_NUMBER() OVER (
                    PARTITION BY dd.tei
                    ORDER BY dd.executiondate DESC
                ) AS rn
            FROM analytics_event_l0egy4eomhv dd
            WHERE dd.ps = 'vY4mlqYfJEH'
        )
        SELECT
        ou2.name as level2,
        ou3.name as level3,
        ou4.name as level4,
        ou5.name as level5,

        dd.ou as orguid,
        dd.ounamehierarchy,
        dd.ouname,
        dd.tei as tei_uid,
        date(dd.executiondate) as visitdate,

        dd."b4UUhQPwlRH" as Unique_Dwelling_No,
        dd."eMYBznRdn0t" as Zhichar_Building_ID,
        dd."kvCvhyGBLIi" as Zhichar_Unit_ID,
        dd."alEL4UIuRee" as BPC_Code,
        dd."WcKI8B0MYaB" as House_Number,
        dd."lOMK3xUwRc7" as Village,
        dd."SHPW4d00NnM" as Dwelling_GPS_Location,	
        dd."HP5XaFj6iZ7" as Dwelling_Altitude_m,	
        dd."dDJdN7rtIoA" as Remarks_attribute,
        dd."BUEzQEErqa7" as Registered_Year,

        dd."F0DV8pEPF98" as HH___Animal_feeds,

        dd."lSzJofGb7fU" as HH___Burial,
        dd."Og4wEm4Z7OV" as HH___Burning,
        dd."uMRfJEDErNx" as HH___IRS_Sprayed,
        dd."a0t6coJR4bG" as HH___Drinking_water_main_source,
        dd."NPb0hOBn6g9" as HH___Household_status,
        dd."lRVDgo5HwYe" as HH___Water_collection_location,
        dd."ADGaCK23IbP" as HH___Time_to_get_water,
        dd."ABBZkh32owZ" as HH___Insufficient_drinking_water,
        dd."JT2QvZDPRAy" as HH___Toilet_facility_used,
        dd."ySLtaPSULVN" as HH___Emptied_pit_latrine_or_septic_tank,
        dd."RIqHmgT1OWu" as HH___Emptied_septic_tank_contents_location,
        dd."R0AYFvHFg6u" as HH___HHM_Hand_wash_location,
        dd."d4DgS6Tv3uG" as HH___Air_pollution_exposure_to_HH_members,
        dd."SgyzeqQpg6V" as HH___Composting,
        dd."vP0NGw6z3Mh" as HH___Open_Pit,
        dd."nz1hyyrSn4k" as HH___Public_garbage_collection,
        dd."Ju3AkdRHT52" as HH___Availability_of_detergent,
        dd."pUnhWS1qOeS" as HH___Brand_of_salt,
        dd."WXDWkfS3GhG" as Remarks,
        dd."rlecl6N9HcX" as HH___Facility_shared_with_non_HH_members,
        dd."WTFyAoDjI4X" as HH___LLINs_currently_in_possession,
        dd."DenbY2uVxeR" as HH___Recyclable_solid_waste_Others,
        dd."ua9PvkeM7iH" as HH___Recycling_or_reusing,
        dd."wbLpz0ADrJv" as HH___Solid_waste_Others,
        dd."vapo8mgKcyM" as HH___Non_bio_degradable_solid_waste_Others,
        dd."Cql7XO3Z5Fe" as HH___Food_to_Feed,
        dd."b60lyh4IRgb" as HH___HHM_slept_under_LLIN,
        dd."Ojvu6krZKBX" as HH___No_of_LLINs_received_since_last_3_years,
        dd."hwCISmocKY6" as HH___Open_Pit_Non_biodegradable,
        dd."CWDcKbFmFty" as HH___Open_Pit_Recyclable,
        dd."haBuqhxXffw" as HH___Public_garbage_collection_Recyclable,
        dd."f28Es6U3KSr" as HH___Burning_Non_biodegradable,
        dd."fkAXYJ8nOll" as HH___Public_garbage_collection_Non_biodegradable,
        dd."d4VMT4orArm" as HH___Availability_of_water,
        dd."ezLCrmL40SD" as HH___Nearest_facility_distance,
        dd."SQmWcDdvnem" as HH___Economic_Status,
        dd."tjXaQPI9OcQ" as HH___Household_Survey_Date,
        dd."YGisOzETviK" as HH___HH_Salt_iodine_content,
        dd."GtSSMCc6nXz" as HH___LLINs_present_in_HH,
        dd."rWCn0WGoAeS" as HH___HHM_slept_under_LLIN_in_last_12_months,

        dd.createdbyusername AS created_by_username,
        dd.createdbyname AS created_by_first_name,
        dd.createdbylastname AS created_by_last_name,
        dd.createdbydisplayname AS created_by_display_name,

        dd.lastupdatedbyusername AS last_updated_by_username,
        dd.lastupdatedbyname AS last_updated_by_first_name,
        dd.lastupdatedbylastname AS last_updated_by_last_name,
        dd.lastupdatedbydisplayname AS last_updated_by_display_name


        FROM latest_events dd

        LEFT JOIN organisationunit ou2 ON ou2.uid = dd.uidlevel2
        LEFT JOIN organisationunit ou3 ON ou3.uid = dd.uidlevel3
        LEFT JOIN organisationunit ou4 ON ou4.uid = dd.uidlevel4
        LEFT JOIN organisationunit ou5 ON ou5.uid = dd.uidlevel5

        WHERE dd.rn = 1;
    """
}

eventHookPayload_house_hold_member_with_users = {
    #"id": "hu2033d7sZw", tubTCfyKArM
    "name": "_analytics_linelist_hh_member_with_users",
    "phase": "ANALYTICS_TABLE_POPULATED",
    "analyticsTableType": "EVENT",
    
    "sql": """
        drop table if exists _bhutan_linelist_hh_member CASCADE; 
        CREATE TABLE _bhutan_linelist_hh_member AS
        WITH latest_events AS (
            SELECT
                dd.*,
                ROW_NUMBER() OVER (
                    PARTITION BY dd.tei
                    ORDER BY dd.executiondate DESC
                ) AS rn
            FROM analytics_event_xvzrp56zkvi dd
        )
        SELECT
        ou2.name as level2,
        ou3.name as level3,
        ou4.name as level4,
        ou5.name as level5,

        dd.ou as orguid,
        dd.ounamehierarchy,
        dd.ouname,
        dd.tei as tei_uid,
        date(dd.executiondate) as visitdate,

        dd."gv9xX5w4kKt" as Family_Information_UID,
        dd."vrM7vt4JZmQ" as UHID,
        dd."rB3psCPmxwE" as Date_of_birth,
        dd."HyGJqEzbxD4" as Contact_Number,
        dd."hDE1WNqTTwF" as Unique_dwelling_ID,
        dd."CADfVSQEVVi" as ID_type,
        dd."rOA2ACbkXug" as ID_number,
        dd."BaiVwt8jVfg" as Age_in_years,
        dd."MYaNKVVYIQT" as Sex,
        dd."s7f3ayF0MEG" as Name,
        dd."ycGbZeG8LeX" as HHM_1___Current_Marital_status,
        dd."zh9y01mPiMD" as HHM_1___Usual_activity_during_the_last_6_months,
        dd."LyBiqvOGFGc" as HHM_1___Age_at_first_marriage_or_first_living_together,
        dd."AMuk90nUTfs" as HHM_2___NCD_module_individual,
        dd."JYX7fyIMwrh" as HHM_2___Smoked_tobacco_products,
        dd."ytkIZFQcene" as HHM_2___Age_when_started_smoking,
        dd."D8IeOPkU4dF" as HHM_1___Tested_for_cervical_cancer,
        dd."jeDxGYlYBPx" as HHM_1___Latest_breast_cancer_test_year,
        dd."toFNuY0zR2a" as HHM_1___H_pylori_screening,
        dd."pyzd5HgSFPb" as HHM_1___Recent_H_pylori_test,
        dd."kcJX2YCBB3v" as HHM_1___Modern_Education,
        dd."DPlIkV0XnI8" as HHM_1___Attending_traditional_learning,
        dd."zxllKSJ52U1" as HHM_1___Stillbirth_last_year,
        dd."UjLxTtDk9qc" as HHM_1___Miscarriage_or_abortion_last_year,
        dd."mt37cOH28F9" as HHM_1___Place_of_delivery,
        dd."uQg4s7Jd8WW" as HHM_1___Place_of_incidence,
        dd."JgHcoI8Vs9v" as HHM_1___ANC_availed_during_recent_pregnancy,
        dd."ZbunNrGNEx7" as HHM_1___Using_hearing_aid,
        dd."jQ83rALANCm" as HHM_1___Difficulty_hearing_with_hearing_aid,
        dd."KrSqdwQgJoe" as HHM_1___Difficulty_walking,
        dd."hf97Ye9CrT4" as HHM_1___Difficulty_with_self_care,
        dd."jrOVR4fNd3H" as HHM_1___Difficulty_hearing,
        dd."NsyZ9HTZMMa" as HHM_1___Difficulty_seeing,
        dd."Z4zfIkKCP7R" as HHM_1___Currently_pregnant,
        dd."VQRxvN71m5l" as HHM_1___Last_year_pregnancy_outcome,
        dd."kzp9TltHi2M" as HHM_1___Beats_per_minute_1,
        dd."dzeTdP1U1b1" as HHM_1___Age_at_death,
        dd."UzYD7jqOBqp" as HHM_2___Problems_due_to_smoking,
        dd."gVbtSt6UaCK" as HHM_2___Concern_about_smoking,
        dd."w4zA0GSrnY2" as HHM_2___Failed_smoking_cut_down,
        dd."pul07TNK7nX" as HHM_2___Tobacco_products,
        dd."DlZeFlKCRGr" as HHM_2___First_started_tobacco_products_age,
        dd."ZTjoxxpLJRt" as HHM_2___Desire_for_tobacco_products,
        dd."McJaMbzcxAS" as HHM_1___Date_of_Death,
        dd."fhcVXetFGxn" as HHM_2___tobacco_products_frequency,
        dd."NJYj8K15jBK" as HHM_2___Desire_to_smoke,
        dd."Tb38VQldkEr" as HHM_2___Areca_nut_consumption,
        dd."dmBGs4QGUbu" as HHM_2___alcohol_consumption,
        dd."WgCarY7Ko0w" as HHM_2___First_started_areca_nut_consumption_age,
        dd."BdVVPG3a82M" as HHM_1___Immunization_received_by_child,
        dd."vQUMCUTDtzn" as HHM_2___Problems_due_to_areca_nut_consumption,
        dd."qaBIOjngXpL" as HHM_2___Smoking_in_closed_areas,
        dd."I064ESZkgag" as HHM_2___areca_nut_consumption___failing_responsibilities,
        dd."x4Vn8TFDtol" as HHM_2___Concern_about_areca_nut_consumption,
        dd."iWaeCiMpBV9" as HHM_2___Pregnant,
        dd."TC0ysGa0ji0" as HHM_2___Failed_areca_nut_consumption_cut_down,
        dd."TT3KCBECRUZ" as HHM_2___Failed_tobacco_products_cut_down,
        dd."nZgJU0CKihb" as HHM_2___Desire_for_areca_nut_consumption,
        dd."Z1AIOXyZEdo" as HHM_2___First_started_alcohol_consumption_age,
        dd."Y68nILE3Hbm" as HHM_2___alcohol_consumption_12_months,
        dd."ZcfMOSb2YAW" as HHM_2___areca_nut_consumption_frequency,
        dd."KfRuikfQldK" as HHM_2___Waist_circumference_cm,
        dd."Y8Y097LoIrP" as HHM_2___alcohol_consumption_frequency,
        dd."RDXCYFo4Uv8" as HHM_1___Diastolic_mmHg_1,
        dd."LRWUTlsJIQP" as HHM_2___Failed_alcohol_consumption_cut_down,
        dd."Di8AmkzbgVG" as HHM_2___Fruit_servings,
        dd."kEL5hSBu6gC" as HHM_2___Work_related_physical_exertion,
        dd."Nt3mxnRg81J" as HHM_2___Vegetable_serving,
        dd."xl2mqLHkDff" as HHM_2___Weekly_vegetable_consumption,
        dd."qys7jQQ8Ecs" as HHM_2___Weekly_fruit_consumption,
        dd."T5ph3cF6LtQ" as HHM_2___Moderate_exertion,
        dd."I09jWdGQDsn" as HHM_2___weekly_physical_exertion_work,
        dd."A4cdhctkNzu" as HHM_2___six_or_more_standard_drinks,
        dd."zbQG9VzXEwQ" as HHM_2___10_mins_cycling,
        dd."RoH08osPgJe" as HHM_2___weekly_exertion,
        dd."v6h7EhZw5Ui" as HHM_2___daily_cycling,
        dd."x4rAVIrHNQW" as HHM_2___weekly_cycling,
        dd."xOAkG4s0XYb" as HHM_2___alcohol_consumption___failing_responsibilities,
        dd."egLB4q5WL2n" as HHM_2___Weekly_sports,
        dd."ckV0yOEytlG" as HHM_2___Weekly___Sports___moderate_intensity,
        dd."k0xgunv5thB" as HHM_2___Hypertention_diagnosis_by_doctor,
        dd."lQZCEKfKrvx" as HHM_2___Local_healer_consulted_for_BP,
        dd."RlTylqBRM17" as HHM_2___Hypertention_diagnosis_by_doctor_last_year,
        dd."t90UIe4vFSX" as HHM_2___Daily___Sports___moderate_intensity,
        dd."ow3jWPZceeS" as HHM_2___Prescribed_medication_for_BP_taken,
        dd."Oi1PtLq78V8" as HHM_2___BP_traditional_remedies,
        dd."cMd8GGJgTLT" as HHM_2___Blood_sugar_measured,
        dd."QY3jBX7waUm" as HHM_2___Diabetes_diagnosed_by_doctor,
        dd."n5n0yLyVwuA" as HHM_2___Eye_check_up_after_diabetes_diagnosis,
        dd."ZLQF5qBLWlQ" as HHM_2___Daily_sports,
        dd."UkChrCwAdnm" as HHM_2___Drugs_prescribed_for_diabetes,
        dd."S185gnI1Jyq" as HHM_2___Prescribed_insulin,
        dd."ywmbicYTIhw" as HHM_2___Local_healer_consulted_for_diabetes,
        dd."hWWA6W6Vvgf" as HHM_2___Blood_pressure_measured_by_doctor,
        dd."N3aQ8FrbXga" as HHM_2___Cholesterol_measured_by_doctor,
        dd."TBo8Lw8Rfis" as HHM_2___Raised_cholesterol_warning,
        dd."OJaXOHWDGwU" as HHM_2___Raised_cholesterol_warning_last_year,
        dd."j8vPhrQ93Ye" as HHM_2___Cholesterol_medication_by_doctor,
        dd."aUFofe87M5z" as HHM_2___Local_healer_consulted_for_cholesterol,
        dd."gKEcTk9bVeg" as HHM_2___Cholesterol_local_treatment,
        dd."PBDkdqR3yWo" as HHM_2___Heart_attack_stroke_chest_pain,
        dd."eWjobHqRmVR" as HHM_2___Asprin_consumption,
        dd."En7TKezqhAz" as HHM_2___Stanins_consumption,
        dd."CszAgcZlA2I" as HHM_2___Weight_in_Kilogram_kg,
        dd."DBKh0M3rsKO" as HHM_2___Hip_circumference_cm,
        dd."pxqEppI9NuY" as HHM_2___Height_in_Centimeters_cm,
        dd."R64k3NNm72d" as HHM_1___Tested_for_breast_cancer,
        dd."nxzNOl3Qjwc" as HHM_1___Latest_cervical_cancer_test_year,
        dd."KLQOqxBSInZ" as HHM_2___Smoking_in_home,
        dd."CMyXmIIL2Pg" as HHM_1___Systolic_mmHg_1,
        dd."cP1EanFicmA" as HHM_1___Membership_Status,
        dd."F6ed0skrJQw" as HHM_1___Transferred_to,
        dd."KJ05f4WOeCO" as HHM_2___Problems_due_to_tobacco_products,
        dd."l9A9zUdal3y" as HHM_2___Smoking___failing_responsibilities,
        dd."EKGSw9xQZSC" as HHM_2___tobacco_products___failing_responsibilities,
        dd."yi3wYvQ9aAt" as HHM_2___Diabetes_diagnosis_in_last_year,
        dd."MY7X9t0l8r3" as HHM_2___Diabetes_traditional_medication,
        dd."PsY5SWSq583" as HHM_2___Smoking_frequency,
        dd."kb8mwrpjGGU" as HHM_2___Desire_for_alcohol_consumption,
        dd."XbokNSO2zVH" as HHM_2___Concern_about_alcohol_consumption,
        dd."vxYznE6Y6NX" as HHM_2___Intense_sports,
        dd."vuQ97rrVTZH" as HHM_2___Sports___moderate_intensity,
        dd."tSkN17334Pz" as HHM_1___Glasses_or_contact_lenses,
        dd."DKT4HMi6oSn" as HHM_1___Difficulty_seeing_with_glasses,
        dd."blkMcSWuz4L" as HHM_1___Difficulty_communicating,
        dd."e0Tg69b3KDD" as HHM_1___Assistance_for_walking_received,
        dd."ejY7zEReQea" as HHM_1___Difficulty_concentrating,
        dd."vWP61ahAkEn" as HHM_1___Treatment_recieved_for_blood_pressure_in_last_2_weeks,
        dd."rhOQjp901FX" as HHM_2___daily_exertion,
        dd."A7UlEPDnV3C" as HHM_1___Accidental_death,
        dd."XpnpuBUtcT2" as HHM_1___Death_alcohol_related,
        dd."KZbBK7iKP3T" as HHM_1___Manner_of_Death,
        dd."Fr5ML76aJNF" as HHM_1___Pregnant_Giving_birth_42_days_of_pregnancy,
        dd."ztinvfhAZnN" as HHM_1___Location_of_death,
        dd."IWmyyzSPchd" as HHM_2___Problems_due_to_alcohol_consumption,
        dd."NAZ7d8bUbjd" as HHM_2___Daily_physical_exertion_work,
        dd."jswy7SbqErA" as HHM_1___Live_births_last_year,

        dd.createdbyusername AS created_by_username,
        dd.createdbyname AS created_by_first_name,
        dd.createdbylastname AS created_by_last_name,
        dd.createdbydisplayname AS created_by_display_name,

        dd.lastupdatedbyusername AS last_updated_by_username,
        dd.lastupdatedbyname AS last_updated_by_first_name,
        dd.lastupdatedbylastname AS last_updated_by_last_name,
        dd.lastupdatedbydisplayname AS last_updated_by_display_name

        FROM latest_events dd

        LEFT JOIN organisationunit ou2 ON ou2.uid = dd.uidlevel2
        LEFT JOIN organisationunit ou3 ON ou3.uid = dd.uidlevel3
        LEFT JOIN organisationunit ou4 ON ou4.uid = dd.uidlevel4
        LEFT JOIN organisationunit ou5 ON ou5.uid = dd.uidlevel5

        WHERE dd.rn = 1;
    """
}



# ============================================================
# SEND REQUEST
# ============================================================


response = requests.post(
    DHIS2_URL + ENDPOINT,
    auth=(USERNAME, PASSWORD),
    headers={"Content-Type": "application/json"},
    data=json.dumps(eventHookPayload_house_hold_updated_with_users)
)


# ============================================================
# SEND REQUEST for DELETE EVENTHOOK
# ============================================================

'''
event_hook_id = "/fvvGDpypuIy"
response = requests.delete(
    DHIS2_URL + ENDPOINT + event_hook_id,
    auth=(USERNAME, PASSWORD),
    headers={"Content-Type": "application/json"}
)
'''

# ============================================================
# RESULT
# ============================================================

print("Status Code:", response.status_code)
try:
    print(response.json())
except:
    print(response.text)

print("Event Hook Creation End")

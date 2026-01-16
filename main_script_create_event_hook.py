import requests
import json

# ============================================================
# DHIS2 SERVER CONFIGURATION
# ============================================================
# select * from tablehook;
#DHIS2_URL = "https://stage.hispindia.org/pmnpis_dev"   # <-- change this
DHIS2_URL = "https://pmnpis.org.ph/app"   # <-- change this production
USERNAME = "*****"
PASSWORD = "*****"

ENDPOINT = "/api/analyticsTableHooks"   # correct for DHIS2 2.40
#https://stage.hispindia.org/pmnpis_dev/api/analyticsTableHooks?paging=false&fields=*
# select * from tablehook;
# ============================================================
# HOOK DEFINITION
# ============================================================

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

eventHookPayload_hh_member_updated = {
    "id": "ROr6zdm4HQb",
    "name": "_analytics_linelist_hh_member",
    "phase": "ANALYTICS_TABLE_POPULATED",
    "analyticsTableType": "EVENT",
    
    "sql": """
        drop table if exists _pmnp_linelist_hh_member; 
        CREATE TABLE _pmnp_linelist_hh_member AS
        SELECT
        ou2.name as region,
        ou3.name as province,
        ou4.name as municipality,
        ou5.name as barangay,

        dd.ou as orguid,
        dd.ounamehierarchy,
        dd.ouname,
        date(dd.executiondate) as visitdate,


        dd."RDQQ3t9oXw5" as household_uid,
        dd."NOKzq4dAKF7" as pmnp_id,


        dd."PIGLwIaw0wy" as first_name,
        dd."WC0cShCpae8" as middle_name,
        dd."IENWcinF8lM" as last_name,
        dd."nyVsU3fTk2b" as extension_name,


        dd."fJPZFs2yYJQ" as date_of_birth,
        dd."H42aYY9JMIR" as age_in_years,
        dd."X2Oln1OyP5o" as age_in_months,
        dd."xDSSvssuNFs" as age_in_weeks,
        dd."d2n5w4zpxuo" as age_in_days,


        dd."VQ9dyZbj843" as ttd1_vaccine_date,
        dd."sBzNt7bbggE" as ttd2_vaccine_date,
        dd."EeL84itsEVm" as ttd3_vaccine_date,
        dd."dxM5jWLEKXq" as ttd4_vaccine_date,
        dd."lRI8oJTn3jL" as ttd5_vaccine_date,


        preg."ycBIHr9bYyw" as hhm_pregnancy_status,
        preg."se8TXlLUzh8" as hhm_postpartum,
        preg."rvv5Hfyczyh" as hhm_date_of_delivery_postpartum,


        dd."wqR0L5WGV6S" as pw_hf_visit_prenatal,
        dd."M5nofSFKw1e" as pw_1st_hf_visit,
        dd."AZXJKuGOM6n" as pw_2nd_hf_visit,
        dd."MR4IiYlxfsx" as pw_3rd_hf_visit,
        dd."ZMjGmieu8Iz" as pw_4th_hf_visit,
        dd."Bdd2wmXbizw" as pw_5th_hf_visit,
        dd."Plkdcpkb04F" as pw_6th_hf_visit,
        dd."AG21Y0hmrAu" as pw_7th_hf_visit,
        dd."RAWt5NBWtvB" as pw_8th_hf_visit,


        dd."AO4P3pcKqek" as pw_iron_folic_acid,
        dd."ZkoIX2TigZA" as pw_deworming,
        dd."cMg8stHS4aH" as pw_tetanus_injection,


        dd."SMfz85dxBrG" as cn_exclusive_breastfeeding_24h,
        dd."RLms3EMK6Lx" as adequate_diet_diversity,
        dd."YJEM6K4r8B6" as cn_breastmilk_yesterday,
        dd."aIMeDdwzVQQ" as cn_grains,
        dd."nVFnpIJFBtP" as cn_legumes,
        dd."iiAjifuwYOE" as cn_dairy,
        dd."hQgU2xbT2CL" as cn_flesh_foods,
        dd."xbPC3AWgDrB" as cn_eggs,
        dd."qfYU7s0EylE" as cn_vitamin_a_foods,
        dd."ZxGgsjfOje1" as cn_other_fruits_veg,

        dd."saTG1WrWtEW" as cn_mnp,
        dd."JoD2AagclsB" as cn_vitamin_a,
        dd."YgK3LWUrA6f" as cn_growth_monitoring,
        dd."uYWxyRYP7GN" as cn_followup_date,

        dd."EMHed4Yi7L6" as ch_age_appropriate_vaccine,
        dd."Wj1Re9XKW5P" as cn_weight_for_age,
        dd."TON0hSWcaw7" as cn_height_for_age,
        dd."RXWSlNxAwq1" as cn_weight_for_height,
        dd."s3q2EVu3qe0" as cn_muac

    from analytics_event_temp_vvlirjoogbj dd

    left join lateral (
        select
            p."ycBIHr9bYyw",
            p."se8TXlLUzh8",
            p."rvv5Hfyczyh"
        from analytics_event_temp_vvlirjoogbj p
        where p.ps = 'LRJrFeDNEdT'
        and p.tei = dd.tei
        and p.executiondate = dd.executiondate
        order by p.created desc
        limit 1
    ) preg on true

    left join organisationunit ou2 on ou2.uid = dd.uidlevel2
    left join organisationunit ou3 on ou3.uid = dd.uidlevel3
    left join organisationunit ou4 on ou4.uid = dd.uidlevel4
    left join organisationunit ou5 on ou5.uid = dd.uidlevel5

    where dd.ps = 'QfXSvc9HtKN'
    and dd.uidlevel2 <> 'zqTkGmyJZeh';

    """
}











# ============================================================
# SEND REQUEST
# ============================================================

response = requests.post(
    DHIS2_URL + ENDPOINT,
    auth=(USERNAME, PASSWORD),
    headers={"Content-Type": "application/json"},
    data=json.dumps(eventHookPayload_hh_member_updated)
)


# ============================================================
# RESULT
# ============================================================

print("Status Code:", response.status_code)
try:
    print(response.json())
except:
    print(response.text)

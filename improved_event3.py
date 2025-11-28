import requests
import pandas as pd
import json
#from zcredentials import un, pw
#from formatting import format_date, handle_nan, float_to_int, int_to_float, to_String, get_float_value
import psutil
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

org_unit_id = 'xkmuovGov2p'
programStageID = "fWx165aDTmA"
programID = 'TCLXsIjo3xu'
searching_Attribute_id = "yS5DA2VY2oc"
url = '*******/api/'
event_push_endpoint = f"{url}events"
DE_url = f'{url}dataElements?paging=False'

def get_ram_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)  # Convert bytes to MB

def fetching_tei_ID(session, url, programID, searching_Attribute_id, benregID):
    tei_url = f"{url}trackedEntityInstances.json?ouMode=ALL&program={programID}&fields=trackedEntityInstance&filter={searching_Attribute_id}:EQ:{benregID}"
    try:
        response = session.get(tei_url)
        response.raise_for_status()
        tei_data = response.json()
        return tei_data['trackedEntityInstances']
    except requests.RequestException as e:
        print(f"Error fetching TEI ID: {e}", flush=True)
        return None

def process_row(session, row, DE_name_id, record_count):
    tei_data = fetching_tei_ID(session, url, programID, searching_Attribute_id, row['BeneficiaryRegID'])
    if not tei_data:
        with open('event_failed_log.txt', 'a') as fail_record:
            fail_record.write(f"\nThis BeneficiaryRegID does not exist: {row['BeneficiaryRegID']}")
        print(f'\nRECORD NO.: {record_count}                   This BeneficiaryRegID does not exist: {row["BeneficiaryRegID"]}', flush=True)
    else:
        event_payload = {
            "program": programID,
            "orgUnit": org_unit_id,
            "eventDate": format_date(row['CreatedDate']),
            "mergeDataValues": True,
            "programStage": programStageID,
            "status": "ACTIVE",
            "trackedEntityInstance": tei_data[0]['trackedEntityInstance'],
            "dataValues": [
                        {"dataElement": DE_name_id['HbA1c'], "value": get_float_value(row['HbA1c'])},          #import this single element later element details: mixed(float, str) ->int
                        {"dataElement": DE_name_id['VisitCode'], "value": int_to_float(row['VisitCode'])},
                        {"dataElement": DE_name_id['BenVisitID'], "value": int_to_float(row['BenVisitID'])},
                        {"dataElement": DE_name_id['BeneficiaryRegID'], "value": handle_nan(row['BeneficiaryRegID'])},
                        {"dataElement": DE_name_id['VisitNo'], "value": handle_nan(row['VisitNo'])},
                        {"dataElement": DE_name_id['VanID'], "value": handle_nan(row['VanID'])},
                        {"dataElement": DE_name_id['AgeOnVisit'], "value": float_to_int(row['AgeOnVisit'])},
                        {"dataElement": DE_name_id['VisitReason'], "value": handle_nan(row['VisitReason'])},
                        {"dataElement": DE_name_id['VisitCategory'], "value": handle_nan(row['VisitCategory'])},
                        {"dataElement": DE_name_id['PregnancyStatus'], "value": handle_nan(row['PregnancyStatus'])},
                        {"dataElement": DE_name_id['Referal_Visitcode'], "value": handle_nan(row['Referal_Visitcode'])},
                        {"dataElement": DE_name_id['referredToInstituteName'], "value": to_String(row['referredToInstituteName'])},
                        {"dataElement": DE_name_id['referralreason'], "value": handle_nan(row['referralreason'])},
                        {"dataElement": DE_name_id['ProvisionalDiagnosis'], "value": handle_nan(row['ProvisionalDiagnosis'])},
                        {"dataElement": DE_name_id['phyanthropometry_bmi'], "value": handle_nan(row['phyanthropometry_bmi'])},
                        {"dataElement": DE_name_id['nurse_rbs'], "value": handle_nan(row['nurse_rbs'])},
                        {"dataElement": DE_name_id['Weight_Kg'], "value": handle_nan(row['Weight_Kg'])},
                        {"dataElement": DE_name_id['Height_Cm'], "value": handle_nan(row['Height_Cm'])},
                        {"dataElement": DE_name_id['WaistCircumference_cm'], "value": handle_nan(row['WaistCircumference_cm'])},
                        {"dataElement": DE_name_id['Temperature'], "value": handle_nan(row['Temperature'])},
                        {"dataElement": DE_name_id['SystolicBP_1stReading'], "value": handle_nan(row['SystolicBP_1stReading'])},
                        {"dataElement": DE_name_id['DiastolicBP_1stReading'], "value": handle_nan(row['DiastolicBP_1stReading'])},
                        {"dataElement": DE_name_id['ComorbidCondition_Fulltext'], "value": to_String(row['ComorbidCondition_Fulltext'])},
                        {"dataElement": DE_name_id['Comorbid_Diabetes'], "value": to_String(row['Comorbid_Diabetes'])},
                        {"dataElement": DE_name_id['Comorbid_Hypertension'], "value": to_String(row['Comorbid_Hypertension'])},
                        {"dataElement": DE_name_id['Comorbid_Asthma'], "value": to_String(row['Comorbid_Asthma'])},
                        {"dataElement": DE_name_id['Comorbid_Epilepsy'], "value": to_String(row['Comorbid_Epilepsy'])},
                        {"dataElement": DE_name_id['Comorbid_Heart_Disease'], "value": to_String(row['Comorbid_Heart_Disease'])},
                        {"dataElement": DE_name_id['Comorbid_Kidney_Disease'], "value": to_String(row['Comorbid_Kidney_Disease'])},
                        {"dataElement": DE_name_id['Comorbid_Sickle_Cell'], "value": to_String(row['Comorbid_Sickle_Cell'])},
                        {"dataElement": DE_name_id['Labtest_Prescribed'], "value": handle_nan(row['Labtest_Prescribed'])},
                        {"dataElement": DE_name_id['Drug_Prescribedcode'], "value": handle_nan(row['Drug_Prescribedcode'])},
                        {"dataElement": DE_name_id['Drug_Dispensecode'], "value": handle_nan(row['Drug_Dispensecode'])},
                        {"dataElement": DE_name_id['diagnosisprovided_full_text'], "value": handle_nan(row['diagnosisprovided_full_text'])},
                        {"dataElement": DE_name_id['DiagnosisProvided1'], "value": handle_nan(row['DiagnosisProvided1'])},
                        {"dataElement": DE_name_id['NCD_Condition'], "value": handle_nan(row['NCD_Condition'])},
                        {"dataElement": DE_name_id['ncd_condition_full_text'], "value": handle_nan(row['ncd_condition_full_text'])},
                        {"dataElement": DE_name_id['PulseRate'], "value": handle_nan(row['PulseRate'])},
                        {"dataElement": DE_name_id['spo2'], "value": handle_nan(row['spo2'])},
                        {"dataElement": DE_name_id['feto_Visitcode'], "value": handle_nan(row['feto_Visitcode'])},
                        {"dataElement": DE_name_id['TestName'], "value": handle_nan(row['TestName'])},
                        {"dataElement": DE_name_id['GenericDrugName'], "value": handle_nan(row['GenericDrugName'])},
                        {"dataElement": DE_name_id['Labtest_Done_Visitcode'], "value": handle_nan(row['Labtest_Done_Visitcode'])},
                        {"dataElement": DE_name_id['Total_lab_test'], "value": handle_nan(row['Total_lab_test'])},
                        {"dataElement": DE_name_id['Random_Blood_Sugar'], "value": get_float_value(row['Random_Blood_Sugar'])},
                        {"dataElement": DE_name_id['Hemoglobin'], "value": handle_nan(row['Hemoglobin'])},
                        {"dataElement": DE_name_id['UrineAlbumin'], "value": handle_nan(row['UrineAlbumin'])},
                        {"dataElement": DE_name_id['UrineSugar'], "value": handle_nan(row['UrineSugar'])},
                        {"dataElement": DE_name_id['Urine_Pregnancy_test'], "value": handle_nan(row['Urine_Pregnancy_test'])},
                        {"dataElement": DE_name_id['Malaria'], "value": handle_nan(row['Malaria'])},
                        {"dataElement": DE_name_id['ECG'], "value": handle_nan(row['ECG'])},
                        {"dataElement": DE_name_id['Liver_Function_Test'], "value": handle_nan(row['Liver_Function_Test'])},
                        {"dataElement": DE_name_id['Liverfunctiontest_Direct_Bilirubin'], "value": handle_nan(row['Liverfunctiontest_Direct_Bilirubin'])},
                        {"dataElement": DE_name_id['Liverfunctiontest_SGPT'], "value": handle_nan(row['Liverfunctiontest_SGPT'])},
                        {"dataElement": DE_name_id['Liverfunctiontest_SGOT'], "value": handle_nan(row['Liverfunctiontest_SGOT'])},
                        {"dataElement": DE_name_id['Liverfunctiontest_Total_Serum_Bilirubin'], "value": handle_nan(row['Liverfunctiontest_Total_Serum_Bilirubin'])},
                        {"dataElement": DE_name_id['Liverfunctiontest_Blood_Urea'], "value": handle_nan(row['Liverfunctiontest_Blood_Urea'])},
                        {"dataElement": DE_name_id['Liverfunctiontest_Serum_Creatinine'], "value": handle_nan(row['Liverfunctiontest_Serum_Creatinine'])},
                        {"dataElement": DE_name_id['Renal_function_test'], "value": handle_nan(row['Renal_function_test'])},
                        {"dataElement": DE_name_id['Renalfunctiontest_Serum_Creatinine'], "value": handle_nan(row['Renalfunctiontest_Serum_Creatinine'])},
                        {"dataElement": DE_name_id['Renalfunctiontest_Blood_Urea'], "value": handle_nan(row['Renalfunctiontest_Blood_Urea'])},
                        {"dataElement": DE_name_id['Lipid_profile'], "value": handle_nan(row['Lipid_profile'])},
                        {"dataElement": DE_name_id['Lipidprofile_Serum_Total_Cholesterol'], "value": handle_nan(row['Lipidprofile_Serum_Total_Cholesterol'])},
                        {"dataElement": DE_name_id['Lipidprofile_Serum_HDL'], "value": handle_nan(row['Lipidprofile_Serum_HDL'])},
                        {"dataElement": DE_name_id['Lipidprofile_LDL'], "value": handle_nan(row['Lipidprofile_LDL'])},
                        {"dataElement": DE_name_id['Lipidprofile_Serum_Triglycerides'], "value": handle_nan(row['Lipidprofile_Serum_Triglycerides'])},
                        {"dataElement": DE_name_id['Post_Lunch_Blood_Sugar'], "value": handle_nan(row['Post_Lunch_Blood_Sugar'])},
                        {"dataElement": DE_name_id['Fasting_Blood_Sugar'], "value": handle_nan(row['Fasting_Blood_Sugar'])},
                        {"dataElement": DE_name_id['Complete_Blood_Picture'], "value": handle_nan(row['Complete_Blood_Picture'])},
                        {"dataElement": DE_name_id['CBP_ESR'], "value": handle_nan(row['CBP_ESR'])},
                        {"dataElement": DE_name_id['CBP_Monocytes'], "value": handle_nan(row['CBP_Monocytes'])},
                        {"dataElement": DE_name_id['CBP_Hemoglobin'], "value": handle_nan(row['CBP_Hemoglobin'])},
                        {"dataElement": DE_name_id['CBP_RBC'], "value": handle_nan(row['CBP_RBC'])},
                        {"dataElement": DE_name_id['CBP_Lymphocytes'], "value": handle_nan(row['CBP_Lymphocytes'])},
                        {"dataElement": DE_name_id['CBP_Neutrophils'], "value": handle_nan(row['CBP_Neutrophils'])},
                        {"dataElement": DE_name_id['CBP_Basophils'], "value": handle_nan(row['CBP_Basophils'])},
                        {"dataElement": DE_name_id['CBP_Eosinophils'], "value": handle_nan(row['CBP_Eosinophils'])},
                        {"dataElement": DE_name_id['CBP_MCV'], "value": handle_nan(row['CBP_MCV'])},
                        {"dataElement": DE_name_id['CBP_MCH'], "value": handle_nan(row['CBP_MCH'])},
                        {"dataElement": DE_name_id['CBP_MCHC'], "value": handle_nan(row['CBP_MCHC'])},
                        {"dataElement": DE_name_id['CBP_Hematocrit'], "value": handle_nan(row['CBP_Hematocrit'])},
                        {"dataElement": DE_name_id['CBP_Platelet_Count'], "value": handle_nan(row['CBP_Platelet_Count'])},
                        {"dataElement": DE_name_id['CBP_Total_Leucocyte_Count'], "value": handle_nan(row['CBP_Total_Leucocyte_Count'])},
                        {"dataElement": DE_name_id['Widal_Test'], "value": handle_nan(row['Widal_Test'])},
                        {"dataElement": DE_name_id['Sputum_AFB_Test'], "value": handle_nan(row['Sputum_AFB_Test'])},
                        {"dataElement": DE_name_id['Sickle_Cell_Disease_Test'], "value": handle_nan(row['Sickle_Cell_Disease_Test'])},
                        {"dataElement": DE_name_id['HBsAg'], "value": handle_nan(row['HBsAg'])},
                        {"dataElement": DE_name_id['Complete_Urine_Examination'], "value": handle_nan(row['Complete_Urine_Examination'])},
                        {"dataElement": DE_name_id['Complete_Urine_Examination_Total_Leucocyte_Count'], "value": handle_nan(row['Complete_Urine_Examination_Total_Leucocyte_Count'])},
                        {"dataElement": DE_name_id['Complete_Urine_Examination_Urine_for_Nitrite'], "value": handle_nan(row['Complete_Urine_Examination_Urine_for_Nitrite'])},
                        {"dataElement": DE_name_id['Chikungunya'], "value": handle_nan(row['Chikungunya'])},
                        {"dataElement": DE_name_id['Hb_Electrophoresis'], "value": handle_nan(row['Hb_Electrophoresis'])},
                        {"dataElement": DE_name_id['Dengue_NS1_Antigen'], "value": handle_nan(row['Dengue_NS1_Antigen'])},
                        {"dataElement": DE_name_id['Dengue_Antibody_Test'], "value": handle_nan(row['Dengue_Antibody_Test'])},
                        {"dataElement": DE_name_id['HIV1_HIV2_RDT'], "value": handle_nan(row['HIV1_HIV2_RDT'])},
                        {"dataElement": DE_name_id['Visual_Acuity_Test'], "value": handle_nan(row['Visual_Acuity_Test'])},
                        {"dataElement": DE_name_id['Blood_Group'], "value": handle_nan(row['Blood_Group'])},
                        {"dataElement": DE_name_id['VDRL_Test'], "value": handle_nan(row['VDRL_Test'])},
                        {"dataElement": DE_name_id['Syphilis'], "value": handle_nan(row['Syphilis'])},
                        {"dataElement": DE_name_id['Serum_Uric_Acid'], "value": handle_nan(row['Serum_Uric_Acid'])},
                        {"dataElement": DE_name_id['Serum_Total_Cholesterol'], "value": handle_nan(row['Serum_Total_Cholesterol'])},
                        {"dataElement": DE_name_id['Hepatitis_B'], "value": handle_nan(row['Hepatitis_B'])},
                        {"dataElement": DE_name_id['Hepatitis_C'], "value": handle_nan(row['Hepatitis_C'])},
                        {"dataElement": DE_name_id['ESR'], "value": handle_nan(row['ESR'])},
                        {"dataElement": DE_name_id['RBS_Status'], "value": handle_nan(row['RBS_Status'])}
                    ]
                }

        try:
            response = session.post(event_push_endpoint, data=json.dumps(event_payload), headers={"Content-Type": "application/json"})
            response.raise_for_status()
            # print('####################################################### SUCCESSFUL ##########################################################', flush=True)
            # print(f'RECORD NO.: {record_count}                    current benID: {row["BeneficiaryRegID"]}', flush=True)
        except requests.RequestException as e:
            resp_msg=response.text
            ind=resp_msg.find('conflict')
            # print(f'####################################################### FAILED #######################################################', flush=True)
            # print(f'RECORD NO.: {record_count}                    current benID: {row["BeneficiaryRegID"]}', flush=True)
            # print(f"Failed to create events. Error: {resp_msg[ind-1:]}", flush=True)
            with open('event_failed_log.txt', 'a') as fail_record:
                fail_record.write(f'\ncurrent benID: {row["BeneficiaryRegID"]}\n Error Message: {resp_msg[ind-1:]}\n')
                fail_record.write("----------------------------------------------------------------------------------------\n")

with requests.Session() as session:
    session.auth = (un, pw)
    DE_resp = session.get(DE_url).json()

DE_list = DE_resp['dataElements']

df = pd.read_csv('filtered_event_data.csv')
df = df[:1000]

required_DE = list(df.columns)
DE_name_id = {i['displayName']: i['id'] for i in DE_list if i['displayName'] in required_DE}
missing = [i for i in required_DE if i not in DE_name_id.keys()]

ram_usages = []
server_ram=[] 
start_time = time.time()
record_count = 0

with open('performance_tracking_event.txt', 'a') as f:
    f.write(f'""""""""""""""""""""""""" STATS """"""""""""""""""""""""""""\nRunning Date and Time: {pd.Timestamp.now()}\n')

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_row, session, row, DE_name_id, record_count + i) for i, (index, row) in enumerate(df.iterrows())]

        for future in as_completed(futures):
            future.result()
            record_count += 1
            ram_usages.append(get_ram_usage())
            memory_info = psutil.virtual_memory()
            ser_ram=f"{memory_info.used / (1024 ** 2):.2f}"
            
            server_ram.append(float(ser_ram))
            print(ser_ram,'mb')

            if time.time() - start_time >= 300:
                f.write(f'total records imported/hour: {record_count}\n')
                start_time = time.time()

    if ram_usages:
        max_ram = max(ram_usages)
        min_ram = min(ram_usages)
        avg_ram = sum(ram_usages) / len(ram_usages)
        max_ser = max(server_ram)
        min_ser = min(server_ram)
        avg_ser = sum(server_ram) / len(server_ram)

        f.write(f'max utilization: {max_ram} \nmin utilization: {min_ram} \naverage utilization: {avg_ram}\n')
        f.write(f'Operation ended at : {pd.Timestamp.now()}\nram usage: {ram_usages}\n')
        
        f.write(f'server max utilization: {max_ser} \nserver min utilization: {min_ser} \nserver average utilization: {avg_ser}\n')
        f.write(f'Server Ram Usage: {server_ram}')

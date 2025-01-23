#!/bin/bash

# Navigate to the directory where main.py is located
cd /home/mithilesh/hiv_event_datavalue_update

# Activate virtual environment if needed (replace 'venv/bin/activate' with your venv path)
# source venv/bin/activate

# Run the main.py script
python3 main_script_eventDataValue_update_age.py
python3 main_script_eventDataValue_update_sex.py
python3 main_script_eventDataValue_update_fSW_type.py
python3 main_script_eventDataValue_update_client_of_fSW_type.py
python3 main_script_eventDataValue_update_risk_group.py
python3 main_script_eventDataValue_update_marital_status.py

# Deactivate virtual environment if activated
# deactivate

# Navigate for saans
##cd /var/odk-dhis2-saans
##python3 main.py

import pandas as pd
import json
import os

import re

# Clean file name for Windows
def clean_filename(name):
    return re.sub(r'[\\/*?:"<>|\n\r]', "_", name).strip()

# Load Excel
df = pd.read_excel("Option_Group_Import_Village.xlsx")

# Output folder
output_dir = "option_sets_json"
os.makedirs(output_dir, exist_ok=True)

# Group by Option Group Name
for group_name, group_df in df.groupby("Option Group Name"):
    
    # Clean name for saving
    safe_group_name = clean_filename(group_name)
    
    # Option Set UID (same for the group)
    option_set_uid = group_df["Option Set UID"].iloc[0]
    option_group_uid = group_df["Option Group UID"].iloc[0]
    print( f"option_group_uid . { option_group_uid }" )

    # Build options list
    options_list = []
    for _, row in group_df.iterrows():
        options_list.append({
            "id": row["option UID"],
            "code": row["Code"],
            "name": row["Shortname"]
        })

    print( f"options_list . { options_list }" )

    # Final JSON structure
    option_set_json = {
        "id": option_set_uid,
        "name": group_name,
        "options": options_list
    }

    # Save JSON
    file_path = os.path.join(output_dir, f"{safe_group_name}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(option_set_json, f, indent=2, ensure_ascii=False)

    print(f"Created: {file_path}")


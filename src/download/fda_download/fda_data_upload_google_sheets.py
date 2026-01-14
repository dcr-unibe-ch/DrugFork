import pandas as pd
import gspread
import re
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials

# === CONFIGURATION ===
SERVICE_ACCOUNT_FILE = "data/FDA/Google_API_key.json"
CSV_FILE = "data/FDA/formatted_output_openFDA.csv"
SPREADSHEET_NAME = "FDA_EMA_Swissmedic_Drug_Approval"
SHEET_NAME = "Sheet1"
START_ROW_TO_CLEAR = 226  # <-- specify from which row everything should be deleted

# === GOOGLE SHEETS CONNECTION ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)
client = gspread.authorize(creds)
sheet = client.open(SPREADSHEET_NAME).worksheet(SHEET_NAME)

# === DELETE ROWS FROM START_ROW_TO_CLEAR ===
total_rows = len(sheet.get_all_values())
if total_rows >= START_ROW_TO_CLEAR:
    sheet.batch_clear([f"A{START_ROW_TO_CLEAR}:AZ{total_rows}"])  # deletes all content from A226 to AZ...

# === LOAD FDA CSV ===
df_raw = pd.read_csv(CSV_FILE)

# === DROP-DOWN MAPPING FUNCTIONS ===
def map_decision(val):
    v = str(val).strip().lower()
    return "approved" if v == "approved" else ""

def map_current_status(val):
    v = str(val).strip().lower()
    if v == "authorised":
        return "authorised"
    elif v == "discontinued":
        return "withdrawn"
    elif v == "withdrawn":
        return "withdrawn"
    else:
        return "NA"

def map_yes_no(val):
    v = str(val).strip().lower()
    return "yes" if v == "yes" else "no"

# === COLUMN DEFINITION ACCORDING TO GOOGLE SHEET STRUCTURE ===
columns_gsheet = [
    'Origin', 'Document Link/ name', 'Marketing_authorisation_number', 'EMA_product_number', 'Drug',
    'Non_proprietary_name', 'marketing_authorisation_holder', 'Drug_class', 'Pharmaceutical_form',
    'Administration_route', 'Decision', 'Current_status', 'Decision_date', 'Orphan_drug_status',
    'Indication_extended', 'Indication_requested', 'Indication_approved', 'Disease_class(es)',
    'Application_date', 'Decisions_number', 'Nonclinical_abridged', 'Referral_body', 'Referral',
    'Nonclinical_pharmacology_invitro', 'Nonclinical_pharmacology_species', 'Nonclinical_pharmacology_strain',
    'Nonclinical_pharmacology_model', 'Nonclinical_pharmacology_sex', 'Nonclinical_pharmacology_outcomes',
    'Nonclinical_pharmacology_adverse_findings', 'Nonclinical_pharmacokinetics_species',
    'Nonclinical_pharmacokinetics_strain', 'Nonclinical_pharmacokinetics_model',
    'Nonclinical_pharmacokinetics_sex', 'Nonclinical_pharmacokinetics_findings',
    'Nonclinical_pharmacokinetics_outcomes', 'Nonclinical_toxicology_species', 'Nonclinical_toxicology_strain',
    'Nonclinical_toxicology_model', 'Nonclinical_toxicology_sex', 'Nonclinical_toxicology_outcomes',
    'Nonclinical_toxicology_outcomes', 'Nonclinical_toxicology_adverse_events',
    'Sex_reported_allgemein', 'Sex', 'Comment'
]

# === PREPARE EMPTY DATAFRAME ===
df_sheet = pd.DataFrame(columns=columns_gsheet)

# === ENTER VALUES FROM FDA DATA ===
df_sheet['Origin'] = df_raw['Origin']
df_sheet['Document Link/ name'] = ""
df_sheet['Marketing_authorisation_number'] = df_raw['Marketing authorisation Number']
df_sheet['EMA_product_number'] = "NA"
df_sheet['Drug'] = df_raw['Drug name']
df_sheet['Non_proprietary_name'] = df_raw['Non proprietary name']
df_sheet['marketing_authorisation_holder'] = df_raw['Marketing authorisation holder/ applicant']
df_sheet['Drug_class'] = ""
df_sheet['Pharmaceutical_form'] = df_raw['Pharmaceutical form']
df_sheet['Administration_route'] = (
    df_raw['Administration route']
    .str.extract(r'(oral|nasal|topical|ophthalmic|transdermal|injection|intravenous)', flags=re.IGNORECASE)[0]
    .str.lower()
)

df_sheet['Decision'] = df_raw['Decision'].apply(map_decision)
df_sheet['Current_status'] = df_raw['Current status'].apply(map_current_status)
df_sheet['Decision_date'] = df_raw['Decision date']
df_sheet['Orphan_drug_status'] = ""
df_sheet['Indication_extended'] = ""
df_sheet['Indication_requested'] = ""
df_sheet['Indication_approved'] = ""
df_sheet['Disease_class(es)'] = ""
df_sheet['Application_date'] = ""
df_sheet['Decisions_number'] = ""
df_sheet['Nonclinical_abridged'] = df_raw['Non-clinical abridge'].apply(map_yes_no)
df_sheet['Referral_body'] = ""  # leave empty
df_sheet['Referral'] = df_raw['Referral'].apply(map_yes_no)

# === LEAVE REMAINING FIELDS EMPTY ===
for col in columns_gsheet:
    if col not in df_sheet.columns:
        df_sheet[col] = ""

# === COLUMNS IN CORRECT ORDER ===
df_sheet = df_sheet[columns_gsheet]

# === INSERT NEW DATA FROM ROW 226 ===
set_with_dataframe(sheet, df_sheet, row=START_ROW_TO_CLEAR, include_column_header=False)

print("FDA data successfully appended to Google Sheet.")
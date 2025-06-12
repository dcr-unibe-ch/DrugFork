import json
import csv
import os
import re
from collections import defaultdict

# Mapping Submission Status
status_dict = {
    "AP": "Approved",
    "TA": "Tentative Approval",
    "SU": "Suspended",
    "WD": "Withdrawn",
    "RA": "Returned Application",
    "CR": "Complete Response",
    "NA": "Not Approved"
}

# Mapping final output fields to source fields
output_field_map = {
    'Origin': lambda entry: 'FDA', # set FDA as default origin
    'Marketing authorisation Number': 'application_number',
    'Drug name': 'brand_name',
    'Non proprietary name': 'generic_name',
    'Marketing authorisation holder/ applicant': 'sponsor_name',
    'Pharmaceutical form': 'dosage_form',
    'Administration route': 'route',
    'Decision': 'submission_status',
    'Decision date': 'submission_status_date',
    'Current status': 'current_status',
    'Non-clinical abridge': 'non_clinical_abridge',
    'Referral': 'reference_drug'
}
formatted_fieldnames = list(output_field_map.keys())

# Date formating function
def format_date(datestr):
    if datestr and len(datestr) == 8 and datestr.isdigit():
        return f"{datestr[6:8]}.{datestr[4:6]}.{datestr[0:4]}"
    return datestr

# Function to standardize application numbers
def canonicalize_applno(applno):
    return re.sub(r'^\D+', '', applno)

# Function to load marketing status lookup from a file
def load_marketing_status_lookup(path):
    status_dict = {}
    with open(path, encoding='utf-8') as f: # load file with UTF-8 encoding
        next(f) # skip header line
        for line in f: # read each line
            parts = line.strip().split('\t')
            if len(parts) >= 2: # ensure there are at least two parts
                status_dict[parts[0]] = parts[1] # map status ID to description
    return status_dict

# Function to load marketing status from a file
def load_marketing_status(path):
    applno_to_status = defaultdict(set)
    with open(path, encoding='utf-8') as f:
        next(f)
        for line in f:
            parts = line.strip().split('\t') # split by tab
            if len(parts) >= 2: 
                applno = canonicalize_applno(parts[1]) # use standardized application number
                applno_to_status[applno].add(parts[0]) # add status ID to the set for this application number
    return applno_to_status

# Function to load more information from Products.txt
def load_products_txt(path):
    applno_to_products = defaultdict(list)
    with open(path, encoding='utf-8') as f:
        next(f)
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 7:
                applno = canonicalize_applno(parts[0])
                product = {
                    'form': parts[2],
                    'reference_drug': 'Yes' if parts[4].strip() == '1' else 'No',
                    'drug_name': parts[5],
                    'active_ingredient': parts[6],
                }
                applno_to_products[applno].append(product)
    return applno_to_products

# Function to extract relevant information from each entry
def extract_info(entry, current_status, products_by_applno):
    applno = entry.get('application_number', '')
    applno_canon = canonicalize_applno(applno) # standardize application number
    non_clinical_abridge = "yes" if applno.startswith('ANDA') else "no" # Non-clinical abridge is "yes" for ANDA applications
    sponsor_name = entry.get('sponsor_name', '')

    brands, generics, forms, routes, ref_drugs = set(), set(), set(), set(), set() # Initialize sets for unique values
    for product in entry.get('products', [{}]): 
        brands.add(product.get('brand_name', '')) 
        generics.add(product.get('generic_name', product.get('active_ingredients', [{}])[0].get('name', '')))
        forms.add(product.get('dosage_form', ''))
        routes.add(product.get('route', ''))
        ref_drugs.add(product.get('reference_drug', ''))

    # load additional product information if available from Products.txt
    if applno_canon in products_by_applno:
        for prod in products_by_applno[applno_canon]:
            if not any(brands): brands.add(prod['drug_name'])
            if not any(generics): generics.add(prod['active_ingredient'])
            if not any(forms): forms.update(prod['form'].split(';'))
            if not any(routes): routes.update(prod['form'].split(';'))
            if not any(ref_drugs): ref_drugs.add(prod['reference_drug'])

    # Determine submission status and date from original submission
    submission_status = ''
    submission_status_date = ''
    submissions = entry.get('submissions', [])
    for sub in submissions:
        if sub.get('submission_type') == 'ORIG' and sub.get('submission_status'):
            raw_status = sub['submission_status']
            submission_status = status_dict.get(raw_status, raw_status)
            submission_status_date = format_date(sub.get('submission_status_date', ''))
            break

    return {
        'application_number': applno,
        'brand_name': "; ".join(sorted(x for x in brands if x)),
        'generic_name': "; ".join(sorted(x for x in generics if x)),
        'sponsor_name': sponsor_name,
        'dosage_form': "; ".join(sorted(x for x in forms if x)),
        'route': "; ".join(sorted(x for x in routes if x)),
        'submission_status': submission_status,
        'submission_status_date': submission_status_date,
        'non_clinical_abridge': non_clinical_abridge,
        'reference_drug': "; ".join(sorted(x for x in ref_drugs if x)),
        'current_status': current_status
    }

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    fda_dir = os.path.join(root_dir, 'data', 'FDA')
    zip_folder = os.path.join(fda_dir, 'FDA_ZIP_folder_drugs@fda')
    file_in = os.path.join(fda_dir, 'drugs@fda_openFDA.json')
    file_out_csv = os.path.join(fda_dir, 'formatted_output_openFDA.csv')
    file_out_json = os.path.join(fda_dir, 'formatted_output_openFDA.json')
    marketingstatus_txt = os.path.join(zip_folder, 'MarketingStatus.txt')
    marketingstatus_lookup = os.path.join(zip_folder, 'MarketingStatus_Lookup.txt')
    products_txt = os.path.join(zip_folder, 'Products.txt')

    msid2desc = load_marketing_status_lookup(marketingstatus_lookup) # dictionary mapping marketing status IDs to their descriptions
    applno2status = load_marketing_status(marketingstatus_txt) # dictionary mapping application numbers to their marketing status IDs
    products_by_applno = load_products_txt(products_txt) # dictionary mapping application numbers to their product information
 
    with open(file_in, encoding='utf-8') as f:
        data = json.load(f)
    results = data.get('results', data)

    # Deduplicate entries based on application number
    deduped = {}
    for entry in results:
        applno = entry.get('application_number', '')
        applno_canon = canonicalize_applno(applno)
        status_ids = applno2status.get(applno_canon, set())
        if "1" in status_ids or "2" in status_ids: # "1" and "2" are IDs for authorised status
            current_status = "authorised"
        elif status_ids: # If there are other status IDs, use the one in the dictionary
            first_other_id = sorted(status_ids)[0]
            current_status = msid2desc.get(first_other_id, "unknown")
        else:
            current_status = ""

        info = extract_info(entry, current_status, products_by_applno)

        if applno not in deduped:
            deduped[applno] = info
        else:
            for key in ['brand_name', 'generic_name', 'dosage_form', 'route', 'reference_drug']:
                vals = set(deduped[applno][key].split("; ")) | set(info[key].split("; "))
                deduped[applno][key] = "; ".join(sorted(x for x in vals if x))
            for key in ['submission_status', 'submission_status_date']:
                if info[key]:
                    deduped[applno][key] = info[key]

    # Format output rows
    rows = []
    for entry in deduped.values():
        row = {}
        for col_name, src in output_field_map.items():
            row[col_name] = src(entry) if callable(src) else entry.get(src, '')
        rows.append(row)

    # save data to CSV and JSON files
    with open(file_out_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=formatted_fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    with open(file_out_json, 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(rows)} Data saved in:\n→ {file_out_csv}\n→ {file_out_json}")

if __name__ == '__main__':
    main()
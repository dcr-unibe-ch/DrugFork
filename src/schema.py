json_schema = {
    "type": "object",
    "properties": {
        "Origin": {"type": "string"},
        "Marketing_authorisation_number": {"type": "string"},
        "Drug": {"type": "string"},
        "Non_proprietary_name": {"type": "string"},
        "Drug_class": {"type": "string"},
        "Pharmaceutical_form": {"type": "string"},
        "Administration_route": {"type": "string"},
        "Decision": {"type": "string"},
        "Current_status": {"type": "string"},
        "Decision_date": {"type": "string", "pattern": r"^\d{2}\.\d{2}\.\d{4}$"},
        "Orphan_drug_status": {"type": "string"},
        "Indication_requested": {"type": "string"},
        "Indication_approved": {"type": "string"},
        "Disease_class(es)": {"type": "string"},
        "Application_date": {"type": "string", "pattern": r"^\d{2}\.\d{2}\.\d{4}$"},
        "Nonclinical_pharmacology_species": {"type": "string"},
        "Nonclinical_pharmacology_strain": {"type": "string"},
        "Nonclinical_pharmacology_model": {"type": "string"},
        "Nonclinical_pharmacokinetics_species": {"type": "string"},
        "Nonclinical_pharmacokinetics_strain": {"type": "string"},
        "Nonclinical_pharmacokinetics_model": {"type": "string"}
    },
    "required": ["Origin", "Marketing_authorisation_number", "Drug", "Non_proprietary_name", "Drug_class", "Pharmaceutical_form", "Administration_route", "Decision", "Current_status", "Decision_date", "Orphan_drug_status", "Indication_requested", "Indication_approved", "Disease_class(es)", "Application_date", "Nonclinical_pharmacology_species", "Nonclinical_pharmacology_strain", "Nonclinical_pharmacology_model", "Nonclinical_pharmacokinetics_species", "Nonclinical_pharmacokinetics_strain", "Nonclinical_pharmacokinetics_model"]
}

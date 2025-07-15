json_schema = {
    "type": "object",
    "properties": {
        "Marketing_authorisation_number": {"type": "string"},
        "Drug_name": {"type": "string"},
        "Non_proprietary_name": {"type": "string"},
        "Marketing_authorisation_holder": {"type": "string"},
        "Drug_class": {"type": "string"},
        "Pharmaceutical_form": {"type": "string"},
        "Administration_route": {"type": "string"},
        "Decision": {"type": "string"},
        "Current_status": {"type": "string"},
        "Decision_date": {"type": "string"},
        "Orphan_drug_status": {"type": "string"},
        "Indication_extended": {"type": "string"},
        "Indication_approved": {"type": "string"},
        "Disease_class(es)": {"type": "string"},
        "Application_date": {"type": "string"},
        "Nonclinical_abridged": {"type": "string"},
        "Referral_body": {"type": "string"}
    },
    "required": ["Marketing_authorisation_number", "Drug_name", "Non_proprietary_name", "Marketing_authorisation_holder", "Drug_class", "Pharmaceutical_form", "Administration_route", "Decision", "Current_status", "Decision_date", "Orphan_drug_status", "Indication_extended", "Indication_approved", "Disease_class(es)", "Application_date", "Nonclinical_abridged", "Referral_body"]
}

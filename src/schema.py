json_schema = {
    "type": "object",
    "properties": {
        "drug_name": {"type": "string"},
        "substance_name": {"type": "string"},
        "year_of_decision": {"type": "integer"}
    },
    "required": ["drug_name", "substance_name", "year_of_decision"]
}

EMA_pairs = {
    "Marketing_authorisation_number": {
        "question": "What is the EMA product number? Product number, usually specified below the date on the first page. It usually has the form of `EMA/{6-digit-number}/{year-of-decision}`",
        "response": "`Marketing_authorisation_number` (string)"
    },
    "Procedure_number": {
        "question": "What is the procedure number? Procedure number, usually stated on the first page. It usually has the form of `EMEA/H/C/{6-digit-number}/0000` or `EMEA/H/C/{6-digit-number}",
        "response": "`Procedure_number` (string)."
    },
    "Drug_name": {
        "question": "What is the market name of the drug? Market name, usually specified on the first page (string)",
        "response": "`Drug_name` (string)."
    },
    "Non_proprietary_name": {
        "question": "What is the non-proprietary name of the drug (name of the substance)? The nonprioprietary name of the drug is usually specified on the first page, following `international non-proprietary name` or similar. Otherwise in the report body",
        "response": "`Non_proprietary_name` (string)."
    },
    "Marketing_authorisation_holder": {
        "question": "Who is the marketing authorisation holder? This is the company that holds the marketing authorisation for the drug or applied for it.",
        "response": "`Marketing_authorisation_holder` (string)"
    },
    "Drug_class": {
        "question": "What is the drug class? Choose only from the following list: `Small molecule`, `Biologics`, `Peptides and proteins`, `Cell and gene therapy`, `Vaccine`, `Other`. Explanation of drug classes: \nSmall Molecules are low molecular weight compounds, typically synthesized chemically. Examples: aspirin, statins, antidepressants.\nBiologics are large, complex molecules derived from living organisms. Examples: monoclonal antibodies.\nPeptides and Proteins are short or long chains of amino acids not classified as full biologics. Examples: insulin, somatostatin.\nCell and Gene Therapies are therapies using modified cells or genes. Examples: CAR-T cell therapies, CRISPR-based gene therapies.\nVaccines are agents stimulating the immune system to prevent or mitigate diseases. Examples: mRNA vaccines, live-attenuated vaccines. \nOther should only be used if you are sure that the drug does not belong to any of the above classes. Try not to use it.",
        "response": "`Drug_class` (string)"
    },
    "Pharmaceutical_form": {
        "question": "What is the pharmaceutical form of the drug (application form)? For example, it could be `solution for injection`, `cream`, `inhalation powder`, `tablet`, etc. It is usually specified in the report section where the drug is described, e.g. `about the product` or similar.",
        "response": "`Pharmaceutical_form` (string)"
    },
    "Administration_route": {
        "question": "How is the drug administered to the patient? It is usually specified in the report section where the drug is described, e.g. `about the product` or similar. Examples: `autologous`, `cutaneous`, `epicutaneous`, `inhalation`, `intramuscular`, `intratumoural`, `intravenous`, `inravitreal`, `nasal`, `ocular`, `oral`, `subcutaneous`, `subretinal`, `intravesical`, `intrathecal`, `vaginal`, etc. Other options are possible. If the administration route is not specified, write `Not reported`.",
        "response": "`Administration_route` (string)"
    },
    "Decision": {
        "question": "What is the decision of the authorisation body? Choose from the following: `approved`, `temporary authorisation`, `withdrawn`, `refused`, `conditional marketing authorisation`. It is usually stated in the section about the steps taken for the assessment of the drug, or else somewhere in the text.",
        "response": "`Decision` (string)"
    },
    "Current_status": {
        "question": "What is the current status of the drug? Choose from the following: `authorised`, `authorised (under additional monitoring)`, `withdrawn`, `NA`, `revoked`. If not explicitely stated, it is likely to be `authorised`, but double-check the report",
        "response": "`Current_status` (string)"
    },
    "Decision_date": {
        "question": "What is the date of the decision? Format: dd.mm.yyyy",
        "response": "`Decision_date` (string)"
    },
    "Decision_year": {
        "question": "What is the year the decision was made? Format: yyyy",
        "response": "`Decision_year` (string)"
    },
    "Orphan_drug_status": {
        "question": "Is the drug designated as an orphan drug? Choose from the following options:  `yes`, `no`.",
        "response": "`Orphan_drug_status` (string)"
    },
    "Indication_extended": {
        "question": "Is the indication extended? Meaning, is it a drug which was previously authorised for a different indication? Choose from the following options:  `yes`, `no`.",
        "response": "`Indication_extended` (string)"
    },
    "Indication_requested": {
        "question": "What is the indication initially requested for approval of the drug?",
        "response": "`Indication_requested` (string)"
    },
    "Indication_approved": {
        "question": "If the drug is approved, what indication is it approved for? Otherwise, state `NA`.",
        "response": "`Indication_approved` (string)"
    },
    "Disease_class(es)": {
        "question": "What is/are the disease class or disease classes of the drug? The classes are usually not explicitely stated in the report, so you have to conclude based on the implicit information. Choose from the following list and select all that are applicable, separating by semicolon: `Infectious and parasitic diseases`, `Neoplasms`, `Diseases of the blood and blood-forming organs`, `Endocrine, nutritional, and metabolic diseases`, `Mental and behavioural disorders`, `Diseases of the nervous system`, `Diseases of the eye and adnexa`, `Diseases of the ear and mastoid process`, `Diseases of the circulatory system`, `Diseases of the respiratory system`, `Diseases of the digestive system`, `Diseases of the skin`, `Diseases of the musculoskeletal system and connective tissue`, `Diseases of the genitourinary system`, `Pregnancy and childbirth`, `Congenital malformations and chromosomal abnormalities`, `Injury, poisoning and certain other consequences of external causes`. If none from the list apply, then and only then write `Other`, avoid it as much as possible. Choose every applicable class.",
        "response": "`Disease_class(es)` (string)"
    },
    "Application_date": {
        "question": "What is the date of the application for drug approval? Format: dd.mm.yyyy",
        "response": "`Application_date` (string)"
    },
    "Application_year": {
        "question": "What is the year of the application for drug approval? Format: yyyy",
        "response": "`Application_year` (string)"
    },
    "Nonclinical_abridged": {
        "question": "Is the nonclinical part of the application abridged? Choose from the following options: `yes`, `no`. If there is no information about nonclinical aspects, then it might be abridged, be attentive. Phrases like `an abridged evaluation`, `nonclinical data not available` or `no nonclinical documentation was submitted` indicate that it is abridged.",
        "response": "`Nonclinical_abridged` (string)"
    },
    "Referral_body": {
        "question": "For nonclinically abridged applications, what is the referral body? Else, write `NA`.",
        "response": "`Referral_body` (string)"
    }
}
SwissMedic_pairs = {
    "Marketing_authorisation_number": {
        "question": "What is the marketing authorisation number? Product number, usually specified on the first page. It is always a 5-digit number",
        "response": "`Marketing_authorisation_number` (string)"
    },
    "Procedure_number": {
        "question": "What is the procedure number? If not specified, write `Not reported`.",
        "response": "`Procedure_number` (string)"
    },
    "Drug_name": {
        "question": "What is the market name of the drug? Market name, usually specified on the first page (string)",
        "response": "`Drug_name` (string)"
    },
    "Non_proprietary_name": {
        "question": "What is the non-proprietary name of the drug (name of the substance)? The nonprioprietary name of the drug is usually specified on the first page, following `international non-proprietary name` or similar. Otherwise in the report body.",
        "response": "`Non_proprietary_name` (string)"
    },
    "Marketing_authorisation_holder": {
        "question": "Who is the marketing authorisation holder? This is the company that holds the marketing authorisation for the drug or applied for it. It is usually specified on the first page, following `Marketing authorisation holder` or similar.",
        "response": "`Marketing_authorisation_holder` (string)"
    },
    "Drug_class": {
        "question": "What is the drug class? Choose only from the following list: `Small molecule`, `Biologics`, `Peptides and proteins`, `Cell and gene therapy`, `Vaccine`, `Other`. Explanation of drug classes: \nSmall Molecules are low molecular weight compounds, typically synthesized chemically. Examples: aspirin, statins, antidepressants.\nBiologics are large, complex molecules derived from living organisms. Examples: monoclonal antibodies.\nPeptides and Proteins are short or long chains of amino acids not classified as full biologics. Examples: insulin, somatostatin.\nCell and Gene Therapies are therapies using modified cells or genes. Examples: CAR-T cell therapies, CRISPR-based gene therapies.\nVaccines are agents stimulating the immune system to prevent or mitigate diseases. Examples: mRNA vaccines, live-attenuated vaccines. \nOther should only be used if you are sure that the drug does not belong to any of the above classes. Try not to use it.",
        "response": "`Drug_class` (string)"
    },
    "Pharmaceutical_form": {
        "question": "What is the pharmaceutical form of the drug (application form)? For example, it could be `solution for injection`, `cream`, `inhalation powder`, `tablet`, etc. It is sometimes specified on the front page under the non-proprietary name.",
        "response": "`Pharmaceutical_form` (string)"
    },
    "Administration_route": {
        "question": "How is the drug administered to the patient? It is usually specified on the first page. Examples: `autologous`, `cutaneous`, `epicutaneous`, `inhalation`, `intramuscular`, `intratumoural`, `intravenous`, `inravitreal`, `nasal`, `ocular`, `oral`, `subcutaneous`, `subretinal`, `intravesical`, `intrathecal`, `vaginal`, etc. Other options are possible. If the administration route is not specified, write `Not reported`.",
        "response": "`Administration_route` (string)"
    },
    "Decision": {
        "question": "What is the decision of the authorisation body? Choose from the following: `approved`, `temporary authorisation`, `withdrawn`, `refused`, `conditional marketing authorisation`. It is usually stated in the section about the steps taken for the assessment of the drug, or else somewhere in the text.",
        "response": "`Decision` (string)"
    },
    "Current_status": {
        "question": "What is the current status of the drug? Choose from the following: `authorised`, `authorised (under additional monitoring)`, `withdrawn`, `NA`, `revoked`. If not explicitely stated, it is likely to be `authorised`, but double-check the report",
        "response": "`Current_status` (string)"
    },
    "Decision_date": {
        "question": "What is the date of the final decision? Format: dd.mm.yyyy",
        "response": "`Decision_date` (string)"
    },
    "Decision_year": {
        "question": "What is the year the final decision was made? Format: yyyy",
        "response": "`Decision_year` (string)"
    },
    "Orphan_drug_status": {
        "question": "Is the drug designated as an orphan drug? Choose from the following options:  `yes`, `no`.",
        "response": "`Orphan_drug_status` (string)"
    },
    "Indication_extended": {
        "question": "Is the indication extended? Meaning, is it a drug which was previously authorised for a different indication? Choose from the following options:  `yes`, `no`.",
        "response": "`Indication_extended` (string)"
    },
    "Indication_requested": {
        "question": "What is the indication initially requested for approval of the drug?",
        "response": "`Indication_requested` (string)"
    },
    "Indication_approved": {
        "question": "If the drug is approved, what indication is it approved for? Otherwise, state `NA`.",
        "response": "`Indication_approved` (string)"
    },
    "Disease_class(es)": {
        "question": "What is the disease class/ disease classes of the drug according to ICD-11? The classes commanly aren't named directly in the report, so you have to conclude based on the implicit information in the report. Choose from the following list and select all that are applicable, separating by semicolon: `Infectious and parasitic diseases`, `Neoplasms`, `Diseases of the blood and blood-forming organs`, `Endocrine, nutritional, and metabolic diseases`, `Mental and behavioural disorders`, `Diseases of the nervous system`, `Diseases of the eye and adnexa`, `Diseases of the ear and mastoid process`, `Diseases of the circulatory system`, `Diseases of the respiratory system`, `Diseases of the digestive system`, `Diseases of the skin`, `Diseases of the musculoskeletal system and connective tissue`, `Diseases of the genitourinary system`, `Pregnancy and childbirth`, `Congenital malformations and chromosomal abnormalities`, `Injury, poisoning and certain other consequences of external causes`. If none from the list apply, then and only then write `Other`, avoid it as much as possible.",
        "response": "`Disease_class(es)` (string)"
    },
    "Application_date": {
        "question": "What is the date of the application for drug approval? Format: dd.mm.yyyy",
        "response": "`Application_date` (string)"
    },
    "Application_year": {
        "question": "What is the year of the application for drug approval? Format: yyyy",
        "response": "`Application_year` (string)"
    },
    "Nonclinical_abridged": {
        "question": "Is the nonclinical part of the application abridged? Choose from the following options: `yes`, `no`. It is usually specified in the section `nonclinical aspects` or similar. If there is no information about nonclinical aspects, then it might be abridged, be attentive. Phrases like `an abridged evaluation`, `nonclinical data not available` or `no nonclinical documentation was submitted` indicate that it is abridged.",
        "response": "`Nonclinical_abridged` (string)"
    },
    "Referral_body": {
        "question": "For nonclinically abridged applications, what is the referral body? Else, write `NA`. It is usually specified in the section `nonclinical aspects`.",
        "response": "`Referral_body` (string)"
    }
}
Japan_pairs = {
    "Marketing_authorisation_number": {
        "question": "What is the marketing authorisation number? If not specified, write `Not reported`.",
        "response": "`Marketing_authorisation_number` (string)"
    },
    "Procedure_number": {
        "question": "What is the procedure number? If not specified, write `Not reported`.",
        "response": "`Procedure_number` (string)."
    },
    "Drug_name": {
        "question": "What is the brand name of the drug? Only keep the drug name, ignore the dosage and administration route or form.",
        "response": "`Drug_name` (string)."
    },
    "Non_proprietary_name": {
        "question": "What is the non-proprietary name of the drug (name of the substance)? Only keep the name, ignore additional information.",
        "response": "`Non_proprietary_name` (string)."
    },
    "Marketing_authorisation_holder": {
        "question": "Who is the marketing authorisation holder (applicant)?",
        "response": "`Marketing_authorisation_holder` (string)"
    },
    "Drug_class": {
        "question": "What is the drug class? Choose only from the following list: `Small molecule`, `Biologics`, `Peptides and proteins`, `Cell and gene therapy`, `Vaccine`, `Other`. Explanation of drug classes: \nSmall Molecules are low molecular weight compounds, typically synthesized chemically. Examples: aspirin, statins, antidepressants.\nBiologics are large, complex molecules derived from living organisms. Examples: monoclonal antibodies.\nPeptides and Proteins are short or long chains of amino acids not classified as full biologics. Examples: insulin, somatostatin.\nCell and Gene Therapies are therapies using modified cells or genes. Examples: CAR-T cell therapies, CRISPR-based gene therapies.\nVaccines are agents stimulating the immune system to prevent or mitigate diseases. Examples: mRNA vaccines, live-attenuated vaccines. \nOther should only be used if you are sure that the drug does not belong to any of the above classes. Try not to use it.",
        "response": "`Drug_class` (string)"
    },
    "Pharmaceutical_form": {
        "question": "What is the pharmaceutical form of the drug (application form)? For example, it could be `solution for injection`, `cream`, `inhalation powder`, `tablet`, etc. It is usually specified following `dosage form/strength` across the document. Keep only the pharmaceutical form.",
        "response": "`Pharmaceutical_form` (string)"
    },
    "Administration_route": {
        "question": "How is the drug administered to the patient? It is specified somewhere in the text. Examples: `autologous`, `cutaneous`, `epicutaneous`, `inhalation`, `intramuscular`, `intratumoural`, `intravenous`, `inravitreal`, `nasal`, `ocular`, `oral`, `subcutaneous`, `subretinal`, `intravesical`, `intrathecal`, `vaginal`, etc. Other options are possible. If the administration route is not specified, write `Not reported`.",
        "response": "`Administration_route` (string)"
    },
    "Decision": {
        "question": "What is the decision of the authorisation body? Choose from the following: `approved`, `temporary authorisation`, `withdrawn`, `refused`, `conditional marketing authorisation`. It is usually stated in the section about the results of deliberation.",
        "response": "`Decision` (string)"
    },
    "Current_status": {
        "question": "What is the current status of the drug? Choose from the following: `authorised`, `authorised (under additional monitoring)`, `withdrawn`, `NA`, `revoked`. If not explicitely stated, it is likely to be `authorised`, but double-check the report",
        "response": "`Current_status` (string)"
    },
    "Decision_date": {
        "question": "What is the date of the decision? Format: `dd.mm.yyyy`. It is usually stated in the section about the results of deliberation.",
        "response": "`Decision_date` (string)"
    },
    "Decision_year": {
        "question": "What is the year the decision was made? Format: `yyyy`. It is usually stated in the section about the results of deliberation.",
        "response": "`Decision_year` (string)"
    },
    "Orphan_drug_status": {
        "question": "Is the drug designated as an orphan drug? Choose from the following options:  `yes`, `no`.",
        "response": "`Orphan_drug_status` (string)"
    },
    "Indication_extended": {
        "question": "Is the indication extended? Meaning, is it a drug which was previously authorised for a different indication? Choose from the following options:  `yes`, `no`.",
        "response": "`Indication_extended` (string)"
    },
    "Indication_requested": {
        "question": "What is the indication initially requested for approval of the drug? If not specified, write `Not reported`.",
        "response": "`Indication_requested` (string)"
    },
    "Indication_approved": {
        "question": "If the drug is approved, what indication is it approved for? Otherwise, state `NA`.",
        "response": "`Indication_approved` (string)"
    },
    "Disease_class(es)": {
        "question": "What is the disease class/ disease classes of the drug according to ICD-11? The classes commanly aren't named directly in the report, so you have to conclude based on the implicit information in the report. Choose from the following list and select all that are applicable, separating by semicolon: `Infectious and parasitic diseases`, `Neoplasms`, `Diseases of the blood and blood-forming organs`, `Endocrine, nutritional, and metabolic diseases`, `Mental and behavioural disorders`, `Diseases of the nervous system`, `Diseases of the eye and adnexa`, `Diseases of the ear and mastoid process`, `Diseases of the circulatory system`, `Diseases of the respiratory system`, `Diseases of the digestive system`, `Diseases of the skin`, `Diseases of the musculoskeletal system and connective tissue`, `Diseases of the genitourinary system`, `Pregnancy and childbirth`, `Congenital malformations and chromosomal abnormalities`, `Injury, poisoning and certain other consequences of external causes`. If none from the list apply, then and only then write `Other`, avoid it as much as possible.",
        "response": "`Disease_class(es)` (string)"
    },
    "Application_date": {
        "question": "What is the date of the application for drug approval? Format: `dd.mm.yyyy`. It is usually stated following `data of application` or similar.",
        "response": "`Application_date` (string)"
    },
    "Application_year": {
        "question": "What is the year of the application for drug approval? Format: `yyyy`. It is usually stated following `data of application` or similar.",
        "response": "`Application_year` (string)"
    },
    "Nonclinical_abridged": {
        "question": "Is the nonclinical part of the application abridged? Choose from the following options: `yes`, `no`. It is usually specified in the section `non-clinical data` or similar. If there is no information about nonclinical aspects, then it might be abridged, be attentive. Phrases like `an abridged evaluation`, `nonclinical data not available` or `no nonclinical documentation was submitted` indicate that it is abridged.",
        "response": "`Nonclinical_abridged` (string)"
    },
    "Referral_body": {
        "question": "For nonclinically abridged applications, what is the referral body? Else, write `NA`. If not specified, write `Not reported`.",
        "response": "`Referral_body` (string)"
    }
}
Australia_pairs = {
    "Marketing_authorisation_number": {
        "question": "What is the marketing authorisation number? If not specified, write `Not reported`.",
        "response": "`Marketing_authorisation_number` (string)"
    },
    "Procedure_number": {
        "question": "What is the procedure number? If not specified, write `Not reported`.",
        "response": "`Procedure_number` (string)."
    },
    "Drug_name": {
        "question": "What is the product name of the drug? It is usually specified in the introduction.",
        "response": "`Drug_name` (string)."
    },
    "Non_proprietary_name": {
        "question": "What is the non-proprietary name of the drug (also called active ingredient)? Only keep the name of the drug, ignore dosage and additional information.",
        "response": "`Non_proprietary_name` (string)."
    },
    "Marketing_authorisation_holder": {
        "question": "Who is the marketing authorisation holder (also called sponsor)? This is the company that holds the marketing authorisation for the drug or applied for it. Only keep the name of the company, ignore address, contact details and additional information.",
        "response": "`Marketing_authorisation_holder` (string)"
    },
    "Drug_class": {
        "question": "What is the drug class? Choose only from the following list: `Small molecule`, `Biologics`, `Peptides and proteins`, `Cell and gene therapy`, `Vaccine`, `Other`. Explanation of drug classes: \nSmall Molecules are low molecular weight compounds, typically synthesized chemically. Examples: aspirin, statins, antidepressants.\nBiologics are large, complex molecules derived from living organisms. Examples: monoclonal antibodies.\nPeptides and Proteins are short or long chains of amino acids not classified as full biologics. Examples: insulin, somatostatin.\nCell and Gene Therapies are therapies using modified cells or genes. Examples: CAR-T cell therapies, CRISPR-based gene therapies.\nVaccines are agents stimulating the immune system to prevent or mitigate diseases. Examples: mRNA vaccines, live-attenuated vaccines. \nOther should only be used if you are sure that the drug does not belong to any of the above classes. Try not to use it.",
        "response": "`Drug_class` (string)"
    },
    "Pharmaceutical_form": {
        "question": "What is the pharmaceutical form of the drug (dose form)? For example, it could be `solution for injection`, `cream`, `inhalation powder`, `tablet`, etc. It is usually specified in the report section where the drug is described, e.g. `about the product` or similar.",
        "response": "`Pharmaceutical_form` (string)"
    },
    "Administration_route": {
        "question": "How is the drug administered to the patient? It is usually specified in the report section where the drug is described, e.g. `about the product` or similar. Examples: `autologous`, `cutaneous`, `epicutaneous`, `inhalation`, `intramuscular`, `intratumoural`, `intravenous`, `inravitreal`, `nasal`, `ocular`, `oral`, `subcutaneous`, `subretinal`, `intravesical`, `intrathecal`, `vaginal`, etc. Other options are possible. If the administration route is not specified, write `Not reported`.",
        "response": "`Administration_route` (string)"
    },
    "Decision": {
        "question": "What is the decision of the authorisation body? Choose from the following: `approved`, `temporary authorisation`, `withdrawn`, `refused`, `conditional marketing authorisation`. It is usually explicitely stated in the introduction.",
        "response": "`Decision` (string)"
    },
    "Current_status": {
        "question": "What is the current status of the drug? Choose from the following: `authorised`, `authorised (under additional monitoring)`, `withdrawn`, `NA`, `revoked`. If not explicitely stated, it is likely to be `authorised`, but double-check the report",
        "response": "`Current_status` (string)"
    },
    "Decision_date": {
        "question": "What is the date of the decision? Format: `dd.mm.yyyy`. It is usually stated in the introduction.",
        "response": "`Decision_date` (string)"
    },
    "Decision_year": {
        "question": "What is the year the decision was made? Format: `yyyy`. It is usually stated in the introduction.",
        "response": "`Decision_year` (string)"
    },
    "Orphan_drug_status": {
        "question": "Is the drug designated as an orphan drug? Choose from the following options:  `yes`, `no`.",
        "response": "`Orphan_drug_status` (string)"
    },
    "Indication_extended": {
        "question": "Is the indication extended? Choose from the following options:  `yes`, `no`. If the type of submission is extension of indications, the answer is certainly `yes`.",
        "response": "`Indication_extended` (string)"
    },
    "Indication_requested": {
        "question": "What is the indication initially requested for approval of the drug? It is usually specified in the section about the product background.",
        "response": "`Indication_requested` (string)"
    },
    "Indication_approved": {
        "question": "If the drug is approved, what indication is it approved for? Otherwise, state `NA`. It is usually specified following `new approved therapeutic use` or similar.",
        "response": "`Indication_approved` (string)"
    },
    "Disease_class(es)": {
        "question": "What is the disease class/ disease classes of the drug according to ICD-11? The classes commanly aren't named directly in the report, so you have to conclude based on the implicit information in the report. Choose from the following list and select all that are applicable, separating by semicolon: `Infectious and parasitic diseases`, `Neoplasms`, `Diseases of the blood and blood-forming organs`, `Endocrine, nutritional, and metabolic diseases`, `Mental and behavioural disorders`, `Diseases of the nervous system`, `Diseases of the eye and adnexa`, `Diseases of the ear and mastoid process`, `Diseases of the circulatory system`, `Diseases of the respiratory system`, `Diseases of the digestive system`, `Diseases of the skin`, `Diseases of the musculoskeletal system and connective tissue`, `Diseases of the genitourinary system`, `Pregnancy and childbirth`, `Congenital malformations and chromosomal abnormalities`, `Injury, poisoning and certain other consequences of external causes`. If none from the list apply, then and only then write `Other`, avoid it as much as possible.",
        "response": "`Disease_class(es)` (string)"
    },
    "Application_date": {
        "question": "What is the date of the application for drug approval? Format: dd.mm.yyyy",
        "response": "`Application_date` (string)"
    },
    "Application_year": {
        "question": "What is the year of the application for drug approval? Format: yyyy",
        "response": "`Application_year` (string)"
    },
    "Nonclinical_abridged": {
        "question": "Is the nonclinical part of the application abridged? Choose from the following options: `yes`, `no`. It is usually specified in the section `nonclinical findings` or elsewhere in the text. If there is no information about nonclinical aspects, then it might be abridged, be attentive. Phrases like `an abridged evaluation`, `nonclinical data not available` or `no nonclinical documentation was submitted` indicate that it is abridged.",
        "response": "`Nonclinical_abridged` (string)"
    },
    "Referral_body": {
        "question": "For nonclinically abridged applications, what is the referral body? Else, write `NA`. It is usually specified in the section `nonclinical findings` or elsewhere in the text. If not specified, write `Not reported`.",
        "response": "`Referral_body` (string)"
    }
}

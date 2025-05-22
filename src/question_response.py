question_response_pairs = {
    "Origin": {
        "question": "What is the authorisation body which performs drug approval? Choose from the following: `Swissmedic`, `EMA`",
        "response": "`Origin` (string)"
    },
    "Marketing_authorisation_number": {
        "question": "What is the marketing authorisation number for Drugs approved by Swissmedic? For drugs approved by EMA: what is the document number?",
        "response": "`Marketing_authorisation_number` (string)"
    },
    "Drug": {
        "question": "What is the market name of the drug?",
        "response": "`Drug` (string)"
    },
    "Non_proprietary_name": {
        "question": "What is the non-proprietary name of the drug (name of the substance)?",
        "response": "`Non_proprietary_name` (string)"
    },
    "Drug_class": {
        "question": "What is the drug class? Choose from the following: `Small molecule`, `Biologics`, `Peptides and proteins`, `Cell and gene therapy`, or else `Vaccine`. Explanation of drug classes: \nSmall Molecules are low molecular weight compounds, typically synthesized chemically. Examples: aspirin, statins, antidepressants.\nBiologics are large, complex molecules derived from living organisms. Examples: monoclonal antibodies.\nPeptides and Proteins are short or long chains of amino acids not classified as full biologics. Examples: insulin, somatostatin.\nCell and Gene Therapies are therapies using modified cells or genes. Examples: CAR-T cell therapies, CRISPR-based gene therapies.\nVaccines are agents stimulating the immune system to prevent or mitigate diseases. Examples: mRNA vaccines, live-attenuated vaccines.",
        "response": "`Drug_class` (string)"
    },
    "Pharmaceutical_form": {
        "question": "What is the pharmaceutical form of the drug (application form)?",
        "response": "`Pharmaceutical_form` (string)"
    },
    "Administration_route": {
        "question": "How is the drug administered to the patient?",
        "response": "`Administration_route` (string)"
    },
    "Decision": {
        "question": "What is the decision of the authorisation body? Choose from the following: `approved`, `temporary authorisation`, `withdrawn`, `refused`",
        "response": "`Decision` (string)"
    },
    "Current_status": {
        "question": "What is the current status of the drug? Choose from the following: `authorised`, `authorised (under additional monitoring)`, `withdrawn`, `NA`",
        "response": "`Current_status` (string)"
    },
    "Decision_date": {
        "question": "What is the date of the decision? Format: dd.mm.yyyy",
        "response": "`Decision_date` (string)"
    },
    "Orphan_drug_status": {
        "question": "Is the drug designated as an orphan drug? Choose from the following: `yes`, `no`",
        "response": "`Orphan_drug_status` (string)"
    },
    "Indication_requested": {
        "question": "What is the indication requested for the drug?",
        "response": "`Indication_requested` (string)"
    },
    "Indication_approved": {
        "question": "What is the indication approved for the drug? If it is the same as the indication requested state: `same`",
        "response": "`Indication_approved` (string)"
    },
    "Disease_class(es)": {
        "question": "What is the disease class/ disease classes of the drug according to ICD-11? Choose from the following, more than one option is sometimes possible: `Infectious and parasitic diseases`, `Neoplasms`, `Diseases of the blood and blood-forming organs`, `Endocrine, nutritional, and metabolic diseases`, `Mental and behavioural disorders`, `Diseases of the nervous system`, `Diseases of the eye and adnexa`, `Diseases of the ear and mastoid process`, `Diseases of the circulatory system`, `Diseases of the respiratory system`, `Diseases of the digestive system`, `Diseases of the skin`, `Diseases of the musculoskeletal system and connective tissue`, `Diseases of the genitourinary system`, `Pregnancy and childbirth`, `Congenital malformations and chomosomal abnormalities`, `Injury, poisoning and certain other consequences of external causes`",
        "response": "`Disease_class(es)` (string)"
    },
    "Application_date": {
        "question": "What is the date of the application for drug approval? Format: dd.mm.yyyy",
        "response": "`Application_date` (string)"
    },
    "Nonclinical_pharmacology_species": {
        "question": "What is/are the species used for nonclinical pharmacology? Look under non-clinical aspects: pharmacology. Format: use singular form of the species name. For example, if the species is `mouse`, use `mouse` instead of `mice`. If there are multiple species, separate them with a comma. For example, `mouse, rat, hamster`. Possible species: `rat`, `mouse`, `hamster`, `guinea pig`, `rabbit`, `dog`, `cat`, `monkey`, `ferret`, `pig`, `sheep`, `goat`, `horse`, `cow`, `chicken`, `fish`.",
        "response": "`Nonclinical_pharmacology_species` (string)"
    },
    "Nonclinical_pharmacology_strain": {
        "question": "What is the strain used for nonclinical pharmacology? Look under non-clinical aspects: pharmacology. Format: strain + species name in singular form. If there are multiple strains, separate them with a comma. For example, `baboon monkey, cotton rat, NSG mouse`.",
        "response": "`Nonclinical_pharmacology_strain` (string)"
    },
    "Nonclinical_pharmacology_model": {
        "question": "What is the model used for nonclinical pharmacology? Look under non-clinical aspects: pharmacology. Format: model + species name in singular form. `Not reported` if not reported. NA if no nonclinical toxicology experiments have been conducted. If there are multiple models, separate them with a comma.",
        "response": "`Nonclinical_pharmacology_model` (string)"
    },
    "Nonclinical_pharmacokinetics_species": {
        "question": "What is the species used for nonclinical pharmacokinetics? Look under non-clinical aspects: pharmacokinetics. Format: use singular form of the species name. For example, if the species is `mouse`, use `mouse` instead of `mice`. If there are multiple species, separate them with a comma. For example, `mouse, rat, hamster`.Possible species: `rat`, `mouse`, `hamster`, `guinea pig`, `rabbit`, `dog`, `cat`, `monkey`, `ferret`, `pig`, `sheep`, `goat`, `horse`, `cow`, `chicken`, `fish`.",
        "response": "`Nonclinical_pharmacokinetics_species` (string)"
    },
    "Nonclinical_pharmacokinetics_strain": {
        "question": "What is the strain used for nonclinical pharmacokinetics? Look under non-clinical aspects: pharmacokinetics. Format: strain + species name in singular form. If there are multiple strains, separate them with a comma. For example, `baboon monkey, cotton rat, NSG mouse`.",
        "response": "`Nonclinical_pharmacokinetics_strain` (string)"
    },
    "Nonclinical_pharmacokinetics_model": {
        "question": "What is the model used for nonclinical pharmacokinetics? Look under non-clinical aspects: pharmacokinetics. Format: model + species name in singular form. `Not reported` if not reported. NA if no nonclinical toxicology experiments have been conducted. If there are multiple models, separate them with a comma.",
        "response": "`Nonclinical_pharmacokinetics_model` (string)"
    },
    "Nonclinical_toxicology_species": {
        "question": "What is the species used for nonclinical toxicology? Look under non-clinical aspects: toxicology. Format: use singular form of the species name. For example, if the species is `mouse`, use `mouse` instead of `mice`. If there are multiple species, separate them with a comma. For example, `mouse, rat, hamster`.Possible species: `rat`, `mouse`, `hamster`, `guinea pig`, `rabbit`, `dog`, `cat`, `monkey`, `ferret`, `pig`, `sheep`, `goat`, `horse`, `cow`, `chicken`, `fish`.",
        "response": "`Nonclinical_toxicology_species` (string)"
    },
    "Nonclinical_toxicology_strain": {
        "question": "What is the strain used for nonclinical toxicology? Look under non-clinical aspects: toxicology. Format: strain + species name in singular form. If there are multiple strains, separate them with a comma. For example, `baboon monkey, cotton rat, NSG mouse`. ",
        "response": "`Nonclinical_toxicology_strain` (string)"
    },
    "Nonclinical_toxicology_model": {
        "question": "What is the model used for nonclinical toxicology? Look under non-clinical aspects: toxicology. Format: model + species name in singular form. `Not reported` if not reported. NA if no nonclinical toxicology experiments have been conducted. If there are multiple models, separate them with a comma.",
        "response": "`Nonclinical_toxicology_model` (string)"
    }
}

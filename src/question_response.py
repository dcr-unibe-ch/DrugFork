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
        "question": "What is the indication requested for approval of the drug? Note: this is not the indication requested in the application process by the company.",
        "response": "`Indication_requested` (string)"
    },
    "Indication_approved": {
        "question": "What is the indication approved for the drug?",
        "response": "`Indication_approved` (string)"
    },
    "Disease_class(es)": {
        "question": "What is the disease class/ disease classes of the drug according to ICD-11? Choose from the following, more than one option is sometimes possible: `Infectious and parasitic diseases`, `Neoplasms`, `Diseases of the blood and blood-forming organs`, `Endocrine, nutritional, and metabolic diseases`, `Mental and behavioural disorders`, `Diseases of the nervous system`, `Diseases of the eye and adnexa`, `Diseases of the ear and mastoid process`, `Diseases of the circulatory system`, `Diseases of the respiratory system`, `Diseases of the digestive system`, `Diseases of the skin`, `Diseases of the musculoskeletal system and connective tissue`, `Diseases of the genitourinary system`, `Pregnancy and childbirth`, `Congenital malformations and chomosomal abnormalities`, `Injury, poisoning and certain other consequences of external causes` Explanation of drug classes: \n1. Infectious and parasitic diseases cover illnesses caused by pathogens such as bacteria, viruses, parasites, and fungi. This includes conditions like HIV/AIDS, tuberculosis, and malaria. \n2. Neoplasms includes benign and malignant tumors (cancers), in situ neoplasms, and those of uncertain behavior, affecting tissues and organs throughout the body. \n3. Diseases of the blood and blood-forming organs covers disorders like anemia, clotting disorders, and diseases affecting bone marrow and immune cells, including hemophilia and sickle cell disease. \n4. Endocrine, nutritional, and metabolic diseases encompasses hormonal and metabolic disorders such as diabetes, thyroid diseases, obesity, and nutritional deficiencies like scurvy or rickets. \n5. Mental and behavioural disorders includes psychiatric and neurodevelopmental disorders such as depression, anxiety, schizophrenia, autism spectrum disorders, and substance use disorders. \n6. Diseases of the nervous system covers disorders affecting the brain, spinal cord, and nerves, including epilepsy, multiple sclerosis, Parkinson’s disease, and migraines. \n7. Diseases of the eye and adnexa encompasses visual system diseases like cataracts, glaucoma, and infections or inflammations of the eye and its surrounding structures (adnexa). \n8. Diseases of the ear and mastoid process includes hearing and balance disorders such as otitis media, tinnitus, and Meniere’s disease, as well as mastoiditis. \n9. Diseases of the circulatory system covers heart and blood vessel conditions like hypertension, coronary artery disease, stroke, and heart failure. \n10. Diseases of the respiratory system encompasses disorders of the lungs and airways, such as asthma, chronic obstructive pulmonary disease (COPD), pneumonia, and sleep apnea. \n11. Diseases of the digestive system includes conditions affecting the gastrointestinal tract and associated organs, such as gastritis, liver cirrhosis, gallstones, and irritable bowel syndrome (IBS). \n12. Diseases of the skin covers dermatological conditions such as eczema, psoriasis, acne, and skin infections like cellulitis and fungal infections. \n13. Diseases of the musculoskeletal system and connective tissue encompasses conditions affecting bones, muscles, joints, and connective tissue, including arthritis, osteoporosis, and systemic lupus erythematosus (SLE). \n14. Diseases of the genitourinary system covers diseases of the kidneys, urinary tract, and reproductive organs, including urinary tract infections, chronic kidney disease, and infertility. \n15. Pregnancy and childbirth includes conditions related to pregnancy, labor, delivery, and the postpartum period, such as gestational diabetes, pre-eclampsia, and complications during birth. \n16. Congenital malformations and chromosomal abnormalities covers birth defects and genetic disorders present from birth, such as Down syndrome, spina bifida, and congenital heart defects. \n17. Injury, poisoning and certain other consequences of external causes includes trauma, burns, fractures, poisoning, and complications from external forces like accidents, violence, or medical procedures.",
        "response": "`Disease_class(es)` (string)"
    },
    "Application_date": {
        "question": "What is the date of the application for drug approval? Format: dd.mm.yyyy",
        "response": "`Application_date` (string)"
    },
    "Nonclinical_pharmacology_species": {
        "question": "What is/are the species used for nonclinical pharmacology? Look under non-clinical aspects: pharmacology. Format: use singular form of the species name. For example, if the species is `mouse`, use `mouse` instead of `mice`. If there are multiple species, separate them with a comma. For example, `mouse, rat, hamster`. Possible species: `rat`, `mouse`, `hamster`, `guinea pig`, `rabbit`, `dog`, `cat`, `monkey`, `ferret`, `pig`, `sheep`, `goat`, `horse`, `cow`, `chicken`, `fish`. `human` is not a valid species. If the species is not reported, use `Not reported`. If no nonclinical pharmacology experiments have been conducted, use `NA`. If there are multiple species, separate them with a comma and state all of them. Important: Only extract species that are *explicitly stated* as being used in *nonclinical toxicology*. Do not guess or infer.",
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
        "question": "What is the species used for nonclinical pharmacokinetics? Look under non-clinical aspects: pharmacokinetics. Format: use singular form of the species name. For example, if the species is `mouse`, use `mouse` instead of `mice`. If there are multiple species, separate them with a comma. For example, `mouse, rat, hamster`.Possible species: `rat`, `mouse`, `hamster`, `guinea pig`, `rabbit`, `dog`, `cat`, `monkey`, `ferret`, `pig`, `sheep`, `goat`, `horse`, `cow`, `chicken`, `fish`. `human` is not a valid species. If the species is not reported, use `Not reported`. If no nonclinical pharmacology experiments have been conducted, use `NA`. If there are multiple species, separate them with a comma and state all of them. Important: Only extract species that are *explicitly stated* as being used in *nonclinical toxicology*. Do not guess or infer.",
        "response": "`Nonclinical_pharmacokinetics_species` (string)"
    },
    "Nonclinical_pharmacokinetics_strain": {
        "question": "What is the strain used for nonclinical pharmacokinetics? Look under non-clinical aspects: pharmacokinetics. Format: strain + species name in singular form. If there are multiple strains, separate them with a comma. For example, `baboon monkey, cotton rat, NSG mouse`. ",
        "response": "`Nonclinical_pharmacokinetics_strain` (string)"
    },
    "Nonclinical_pharmacokinetics_model": {
        "question": "What is the model used for nonclinical pharmacokinetics? Look under non-clinical aspects: pharmacokinetics. Format: model + species name in singular form. `Not reported` if not reported. NA if no nonclinical toxicology experiments have been conducted. If there are multiple models, separate them with a comma.",
        "response": "`Nonclinical_pharmacokinetics_model` (string)"
    },
    "Nonclinical_toxicology_species": {
        "question": "What is the species used for nonclinical toxicology? Look under non-clinical aspects: toxicology. Format: use singular form of the species name. For example, if the species is `mouse`, use `mouse` instead of `mice`. If there are multiple species, separate them with a comma. For example, `mouse, rat, hamster`.Possible species: `rat`, `mouse`, `hamster`, `guinea pig`, `rabbit`, `dog`, `cat`, `monkey`, `ferret`, `pig`, `sheep`, `goat`, `horse`, `cow`, `chicken`, `fish`. `human` is not a valid species. If the species is not reported, use `Not reported`. If no nonclinical pharmacology experiments have been conducted, use `NA`. If there are multiple species, separate them with a comma and state all of them. Important: Only extract species that are *explicitly stated* as being used in *nonclinical toxicology*. Do not guess or infer.",
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

import os
import json
from dotenv import load_dotenv
import argparse
from openai import OpenAI
import openai

# for pdf-based datasets
system_prompt_holder = "Extract the core parent company (corporation) name from each of the following full legal company names. If no holder name provided, return 'Not Reported'. Remove any legal suffixes (e.g., Ltd, Limited, S.L., S.A., S.R.L.), country identifiers, or ownership types. Return only the base company name that is shared across all legal variations. If there are words like 'Group' or 'Company' or 'Pharma', etc., please drop them. We only need the unique core names of the corporation. For example, 'Takeda Pharmaceutical Company' should be returned as 'Takeda'; instead of 'Kowa Company', return 'Kowa'. No other comments or explanations are allowed."
system_prompt_disease_approved = "You are a medical expert. Your role is to extract disease names from approved indications for drug use. If no disease name provided, return 'Not Reported'. Return only the disease names, enclosing them into angle brackets and separating them with a semicolon if there are multiple disease names. You should return MeSH terms on the level of concepts. For example: write <Influenza> instead of <Influenza A>; write <Ovarian Neoplasms> instead of <Overian Cancer>; <Recurrent Ovarian Cancer>. Return only disease names and not the type of medication the patient receives (e.g. 'Chemotherapy' or 'Dialysis' are not relevant). Avoid any presumptions and stick to the text provided. Use proper MeSH-standard casing and phrasing where applicable. No other comments or explanations are allowed."
system_prompt_disease_requested = "You are a medical expert. Your role is to extract disease names from requested indications for drug use. If no disease name provided, return 'Not Reported'. Return only the disease names, enclosing them into angle brackets and separating them with a semicolon if there are multiple disease names. You should return MeSH terms on the level of concepts. For example: write <Influenza> instead of <Influenza A>; write <Ovarian Neoplasms> instead of <Overian Cancer>; <Recurrent Ovarian Cancer>. Return only disease names and not the type of medication the patient receives (e.g. 'Chemotherapy' or 'Dialysis' are not relevant). Avoid any presumptions and stick to the text provided. Use proper MeSH-standard casing and phrasing where applicable. No other comments or explanations are allowed."

# for FDA (and maybe HealthCanada)
system_prompt_disease_class = "You are a medical expert. What is/are the disease class or disease classes of the drug in the indication? Identify all applicable disease classes for the indication provided. Use the following list and select **all that apply**, separated by semicolons: `Infectious and parasitic diseases`, `Neoplasms`, `Diseases of the blood and blood-forming organs`, `Endocrine, nutritional, and metabolic diseases`, `Mental and behavioural disorders`, `Diseases of the nervous system`, `Diseases of the eye and adnexa`, `Diseases of the ear and mastoid process`, `Diseases of the circulatory system`, `Diseases of the respiratory system`, `Diseases of the digestive system`, `Diseases of the skin`, `Diseases of the musculoskeletal system and connective tissue`, `Diseases of the genitourinary system`, `Pregnancy and childbirth`, `Congenital malformations and chromosomal abnormalities`, `Injury, poisoning and certain other consequences of external causes`. If the disease classes are not explicitly stated, infer them based on indications, mechanism of action, or therapeutic area described in the text. For example, if the drug is used for small cell lung cancer, answer: `Neoplasms; Diseases of the respiratory system`. A drug for non-small cell lung cancer **and** non hodgkin lymphoma → `Neoplasms; Diseases of the respiratory system; Diseases of the blood and blood forming organs`. Use `Other` only if **none** of the listed categories fit, which should be rare. Be exhaustive and select every applicable class even if only briefly mentioned. No other comments or explanations are allowed. Answer only with the disease class(es)."
system_prompt_drug_class = "You are a medical expert. Identify the drug class based on the non-proprietary name of the drug. Choose only from the following list: `Small molecule`, `Biologics`, `Peptides and proteins`, `Cell and gene therapy`, `Vaccine`, `Other`. Explanation of drug classes: \nSmall Molecules are low molecular weight compounds, typically synthesized chemically. Examples: aspirin, statins, antidepressants.\nBiologics are large, complex molecules derived from living organisms. Examples: monoclonal antibodies.\nPeptides and Proteins are short or long chains of amino acids not classified as full biologics. Examples: insulin, somatostatin.\nCell and Gene Therapies are therapies using modified cells or genes. Examples: CAR-T cell therapies, CRISPR-based gene therapies.\nVaccines are agents stimulating the immune system to prevent or mitigate diseases. Examples: mRNA vaccines, live-attenuated vaccines. \nOther should only be used if you are sure that the drug does not belong to any of the above classes. Try not to use it. No other comments or explanations are allowed, answer only with the drug class."

def load_env_variables():
    """Load environment variables from .env file."""
    load_dotenv(override=True)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    return OPENAI_API_KEY

openai = OpenAI(api_key=load_env_variables())

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()  
    parser.add_argument("--input_file", type=str, help="Path to the input json file", required=True)
    parser.add_argument("--columns_of_interest", nargs='+', required=True, help="Columns to extract data from")
    parser.add_argument("--slice", type=int, default=-1, help="Slice of the dataset to process")
    parser.add_argument("--model", type=str, default="gpt-4o-mini", help="Model name", required=False)
    parser.add_argument("--save_file", type=str, help="Path to the output file", required=True)
    parser.add_argument("--temperature", type=float, default=0.1, help="Temperature for the model")
    parser.add_argument("--max_tokens", type=int, default=100, help="Max tokens for the model")
    parser.add_argument("--dataset", type=str, required=True, help="Dataset name")
    return parser.parse_args()

def load_json_file(file_path):
    """Load a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)
    
def extract_data(system_prompt, dataset_instance, model, temperature, max_tokens):
    """Generate disease names using OpenAI API."""
    
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": dataset_instance}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content.strip()

def get_prompt_for_column(column_of_interest):
    """Get the system prompt and output field based on the column of interest."""
    if column_of_interest == "Marketing_authorisation_holder":
        return [(system_prompt_holder, "Marketing_authorisation_holder_extracted")]
    elif column_of_interest == "Indication_approved":
        return [(system_prompt_disease_approved, "Indication_approved_extracted")]
    elif column_of_interest == "Indication_requested":
        return [(system_prompt_disease_requested, "Indication_requested_extracted")]
    elif column_of_interest == "Indications_and_usage":
        return [(system_prompt_disease_class, "Indications_and_usage_disease_class_extracted"), (system_prompt_disease_approved, "Indications_and_usage_disease_name_extracted")]
    elif column_of_interest == "Non_proprietary_name":
        return [(system_prompt_drug_class, "Non_proprietary_name_extracted")]
    else:
        raise ValueError(f"Unsupported column of interest: {column_of_interest}")

def main():
    args = parse_arguments()

    input_file = load_json_file(args.input_file)
    if args.slice != -1:
        # input_file = input_file[:args.slice]
        input_file = {k: v for k, v in list(input_file.items())[:args.slice]}

    if args.save_file:
        os.makedirs(os.path.dirname(args.save_file), exist_ok=True)

    for column_of_interest in args.columns_of_interest:

        prompts = get_prompt_for_column(column_of_interest)
        for system_prompt, output_field in prompts:


        # system_prompt, output_field = get_prompt_for_column(column_of_interest)

            for key, value in input_file.items():
                if not isinstance(value, dict):
                    print(f"[WARN] Skipped key '{key}' – expected dict, got {type(value).__name__}")
                    continue
                else:
                    input = value.get(column_of_interest, "")
                    
                    if input:
                        target = extract_data(system_prompt, input, args.model, args.temperature, args.max_tokens)
                        print(f"Source:\t{input}\n--Target:\t{target}")
                        print()
                        input_file[key][output_field] = target
                    else:
                        print(f"Source:\t{input}\n--Target:\tNo data found")
                        print()
                        input_file[key][output_field] = None


                with open(args.save_file, 'w') as output_file:
                    json.dump(input_file, output_file, indent=4)


if __name__ == "__main__":
    main()
import os
import json
from dotenv import load_dotenv
import argparse
from openai import OpenAI
import openai


system_prompt_holder = "Extract the core parent company (corporation) name from each of the following full legal company names. Remove any legal suffixes (e.g., Ltd, Limited, S.L., S.A., S.R.L.), country identifiers, or ownership types. Return only the base company name that is shared across all legal variations. If there are words like 'Group' or 'Company' or 'Pharma', etc., please drop them. We only need the unique core names of the corporation. For example, 'Takeda Pharmaceutical Company' should be returned as 'Takeda'; instead of 'Kowa Company', return 'Kowa'."
system_prompt_disease = "You are a medical expert. Your role is to extract disease names from approved indications for drug use. Return only the disease names in a comma-separated format. You should return MeSH terms on the level of concepts. For example: write 'Influenza' instead of 'Influenza A'; write 'Ovarian Neoplasms' instead of 'Overian Cancer, Recurrent Ovarian Cancer'. Return onlydisease names and not the type of medication the patient receives (e.g. 'Chemotherapy' or 'Dialysis' are not relevant). Avoid any presumptions and stick to the text provided."

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
    parser.add_argument("--slice", type=int, default=-1, help="Slice of the dataset to process")
    parser.add_argument("--model", type=str, default="gpt-4o-mini", help="Model name", required=False)
    parser.add_argument("--save_dir", type=str, help="Path to the output dir", required=False)
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



def main():
    args = parse_arguments()

    input_file = load_json_file(args.input_file)
    if args.slice != -1:
        input_file = {k: v for k, v in list(input_file.items())[:args.slice]}

    # TODO 
    # column_of_interest = "Marketing_authorisation_holder"
    column_of_interest = "Indication_approved"

    if column_of_interest == "Marketing_authorisation_holder":
        system_prompt = system_prompt_holder
    elif column_of_interest == "Indication_approved":
        system_prompt = system_prompt_disease

    for key, value in input_file.items():
        input = value.get(column_of_interest, "").strip()
        if input:

            target = extract_data(system_prompt, input, args.model, args.temperature, args.max_tokens)
            print(f"Source:\t{input}\n--Target:\t{target}")
            print()
        else:
            print(f"Source:\t{input}\n--Target:\tNo data found")
            print()

if __name__ == "__main__":
    main()
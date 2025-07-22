import os
import csv
import json
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import argparse
from jsonschema import validate, ValidationError
from openai import OpenAI
from datetime import datetime

from schema import json_schema
from question_response import EMA_pairs, SwissMedic_pairs, Japan_pairs, Australia_pairs


def load_env_variables():
    """Load environment variables from .env file."""
    load_dotenv(override=True)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GOOGLEAI_API_KEY = os.getenv("GOOGLEAI_API_KEY")
    return OPENAI_API_KEY, GOOGLEAI_API_KEY

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()  
    parser.add_argument("--file_list", type=str, help="Path to the file containing a list of PDFs", required=True)
    parser.add_argument("--data_dir", type=str, help="Path to the directory containing the PDFs", required=True)
    parser.add_argument("--model", type=str, default="gpt-4o", help="Model name", required=False)
    parser.add_argument("--save_dir", type=str, help="Path to the output dir", required=False)
    parser.add_argument("--temperature", type=float, default=0.1, help="Temperature for the model")
    parser.add_argument("--max_tokens", type=int, default=500, help="Max tokens for the model")
    parser.add_argument("--dataset", type=str, required=True, help="Dataset name")
    return parser.parse_args()

def handle_file(file_path, dataset_name):
    """Extract text from the PDF file."""
    if file_path.endswith('.pdf'):
        reader = PdfReader(file_path)
        if dataset_name == "Australia":
            max_pages = 40
        elif dataset_name == "Japan":
            max_pages = 60
        elif dataset_name == "SwissMedic" or dataset_name == "EMA":
            max_pages = 70
        else:
            max_pages = 80
        text = "".join([page.extract_text() or '' for page in reader.pages[:max_pages]])
    else:
        return None
    return text

def generate_response(text, client, model_name, file_name, question_response_pairs):
    """Generate a response from OpenAI API based on the extracted text."""

    system_role = "You are a helpful expert in drug approval processes, with an expertise in dataset annotation."
    user_prompt = f"""
        You are going to read a drug approval report. Read the text attentively and answer the following questions in the strictly specified JSON format with the specified keys:\n
        """ 
    for key, value in question_response_pairs.items():
        user_prompt += f"Question: {value['question']}\n"
        user_prompt += f"Response format: {value['response']}\n"
    user_prompt += "\n\n"
    user_prompt += """
        Generate only the answers to the above questions, in the correct order. Your response should contain these keys and only these keys, with appropriate values based on the report you are annotating. If no answer can be found in the text, write `Not reported` unless specified otherwise in the question-response pair instructions. Be as concise as possible. Think hard before responding.\n
        """
    user_prompt += f"TEXT: {text}\n"
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
            max_tokens=1000
        )
        response_content = response.choices[0].message.content.strip()
        if response_content.startswith("```json") and response_content.endswith("```"):
            response_content = response_content[7:-3].strip()
        try:
            response_json = json.loads(response_content)
            validate(instance=response_json, schema=json_schema)
            response_json["Document_name"] = file_name
            return {file_name: response_json}
        except json.JSONDecodeError:
            return {file_name: f"Error: The response is not valid JSON: {response_content}"}
        except ValidationError as ve:
            return {file_name: f"Error: The response does not match the expected schema: {ve.message}"}
    except Exception as e:
        return {file_name: f"Error generating response: {str(e)}"}

def save_to_csv(data, output_csv_file, question_response_pairs):
    """Save the results to a CSV file."""
    with open(output_csv_file, 'w', newline='') as csvfile:
        fieldnames = ["Document_name"] + [key for key in question_response_pairs.keys()]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for file_name, response in data.items():
            row = {"Document_name": file_name}
            if isinstance(response, dict):  # Only write the valid response as the data
                for key, value in response.items():
                    row[key] = value
            else:
                row["Error"] = response
            writer.writerow(row)

def process_files(args, file_list, client, model_name, save_dir, data_dir):
    """Process all files listed in the file."""

    timestamp = datetime.now().strftime('%Y%m%d')

    output_file = os.path.join(save_dir, f'{timestamp}_{args.dataset}_{model_name}.json')
    output_file_csv = os.path.join(save_dir, f'{timestamp}_{args.dataset}_{model_name}.csv')
    os.makedirs(save_dir, exist_ok=True)

    dataset_pairs = EMA_pairs if args.dataset == "EMA" else SwissMedic_pairs if args.dataset == "SwissMedic" else Japan_pairs if args.dataset == "Japan" else Australia_pairs


    existing_data = {}

    with open(file_list, 'r') as file:
        for line in file:
            file_name = line.strip()
            print(" " * 10, "*" * 5, " " * 10)
            print(f"--- Processing file: {file_name}...")
            file_path = os.path.join(data_dir, file_name)
            
            if os.path.exists(file_path):
                text = handle_file(file_path, args.dataset)
                if text:
                    response = generate_response(text, 
                                                 client, 
                                                 model_name=model_name, 
                                                 file_name=file_name, 
                                                 question_response_pairs=dataset_pairs
                                                )
                    print(f"--- Response:\n{response}")
                    existing_data[file_name] = response.get(file_name, "Error processing the file.")
                else:
                    existing_data[file_name] = "Error: No text extracted from the file."
            else:
                existing_data[file_name] = "Error: File not found."
    
    with open(output_file, 'w') as f:
        json.dump(existing_data, f, indent=4)
    print(f"All responses saved to {output_file}")

    save_to_csv(existing_data, 
                output_file_csv, 
                question_response_pairs=dataset_pairs)
    print(f"All responses saved to {output_file_csv}")

def main():
    args = parse_arguments()
    OPENAI_API_KEY, _ = load_env_variables()
    client = OpenAI(api_key=OPENAI_API_KEY)

    process_files(args, args.file_list, client, model_name=args.model, save_dir=args.save_dir, data_dir=args.data_dir)

if __name__ == "__main__":
    main()

import os
import json
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import argparse
from jsonschema import validate, ValidationError
from openai import OpenAI

from schema import json_schema
from question_response import question_response_pairs


def load_env_variables():
    """Load environment variables from .env file."""
    load_dotenv(override=True)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GOOGLEAI_API_KEY = os.getenv("GOOGLEAI_API_KEY")
    return OPENAI_API_KEY, GOOGLEAI_API_KEY

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()  
    parser.add_argument("--file_list", type=str, help="Path to the file containing a list of PDFs", required=True),
    parser.add_argument("--data_dir", type=str, help="Path to the directory containing the PDFs", required=True),
    parser.add_argument("--model", type=str, default="gpt-4o-mini", help="Model name", required=False)
    parser.add_argument("--save_dir", type=str, help="Path to the output dir", required=False)
    parser.add_argument("--temperature", type=float, default=0.7, help="Temperature for the model")
    parser.add_argument("--max_tokens", type=int, default=300, help="Max tokens for the model")
    return parser.parse_args()

def handle_file(file_path):
    """Extract text from the PDF file."""
    if file_path.endswith('.pdf'):
        reader = PdfReader(file_path)
        text = "".join([page.extract_text() or '' for page in reader.pages])
    else:
        return None
    return text

def generate_response(text, client, model_name, file_name):
    """Generate a response from OpenAI API based on the extracted text."""
    system_role = "You are a helpful expert in Swiss drug approval processes"
    user_prompt = f"""
        You are going to read a drug approval report. Read the text attentively and answer the following questions in the specified JSON format with the specified keys:\n
        """ 
    for key, value in question_response_pairs.items():
        user_prompt += f"Question: {value['question']}\n"
        user_prompt += f"Response format: {value['response']}\n"
    user_prompt += "\n\n"
    user_prompt += """
        Generate only the answers to the above questions, in the correct order. Your response should contain these keys and only these keys, with appropriate values based on the report you're analyzing. Be as concise as possible.\n
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
            return {file_name: response_json}
        except json.JSONDecodeError:
            return {file_name: f"Error: The response is not valid JSON: {response_content}"}
        except ValidationError as ve:
            return {file_name: f"Error: The response does not match the expected schema: {ve.message}"}
    except Exception as e:
        return {file_name: f"Error generating response: {str(e)}"}

def process_files(file_list, client, model_name, save_dir, data_dir):
    """Process all files listed in the file."""

    output_file = os.path.join(save_dir, f'{model_name}_responses.json')
    
    # Create the save directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)

    # Check if the common JSON file exists
    if os.path.exists(output_file):
        # Load the existing data
        with open(output_file, 'r') as f:
            existing_data = json.load(f)
    else:
        # Initialize an empty dictionary if the file doesn't exist
        existing_data = {}

    # Iterate over each file in the list and process it
    with open(file_list, 'r') as file:
        for line in file:
            file_name = line.strip()
            print(" " * 10, "*" * 5, " " * 10)
            print(f"--- Processing file: {file_name}...")
            file_path = os.path.join(data_dir, file_name)
            
            if os.path.exists(file_path):
                text = handle_file(file_path)
                if text:
                    response = generate_response(text, client, model_name=model_name, file_name=file_name)
                    print(f"--- Response:\n{response}")
                    existing_data[file_name] = response.get(file_name, "Error processing the file.")
                else:
                    existing_data[file_name] = "Error: No text extracted from the file."
            else:
                existing_data[file_name] = "Error: File not found."
    
    # Write the updated data back to the common JSON file
    with open(output_file, 'w') as f:
        json.dump(existing_data, f, indent=4)
    print(f"All responses saved to {output_file}")

def main():
    args = parse_arguments()
    OPENAI_API_KEY, _ = load_env_variables()
    client = OpenAI(api_key=OPENAI_API_KEY)

    # Process all files listed in the input file
    process_files(args.file_list, client, model_name=args.model, save_dir=args.save_dir, data_dir=args.data_dir)

if __name__ == "__main__":
    main()

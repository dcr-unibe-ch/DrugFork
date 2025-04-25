from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader
import json
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
    parser.add_argument("--filepath", type=str, help="Path to the input file", required=True)
    parser.add_argument("--file_name", type=str, help="Name of the input file", required=True)
    parser.add_argument("--model", type=str, default="gpt-4o-mini", help="Model name", required=False)
    parser.add_argument("--save_dir", type=str, help="Path to the output dir", required=False)
    parser.add_argument("--temperature", type=float, default=0.7, help="Temperature for the model")
    parser.add_argument("--max_tokens", type=int, default=300, help="Max tokens for the model")
    return parser.parse_args()

def handle_file(file_path):
    if file_path.endswith('.pdf'):
        reader = PdfReader(file_path)
        text = "".join([page.extract_text() or '' for page in reader.pages])
    else:
        return "Unsupported file type. Please upload a PDF.", None
    return text

def generate_response(text, client, model_name, file_name):

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
            max_tokens=300
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

def main():
    args = parse_arguments()
    OPENAI_API_KEY, _ = load_env_variables()
    client = OpenAI(api_key=OPENAI_API_KEY)
    text = handle_file(args.filepath)
    if text:
        response = generate_response(text, client, model_name=args.model, file_name=args.file_name)
        print(response)
    else:
        raise Exception("No text extracted from the file.")



if __name__ == "__main__":
    main()

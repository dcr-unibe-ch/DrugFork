import os
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
import argparse
import time

def load_env_variables():
    load_dotenv(override=True)
    return os.getenv("OPENAI_API_KEY")

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval_sheet", type=str, required=True, help="Path to the evaluation sheet CSV")
    parser.add_argument("--output_file", type=str, required=True, help="Path to write out the completed sheet")
    parser.add_argument("--model_name", type=str, required=True, help="Short model name to use for evaluation")
    parser.add_argument("--slice_size", type=int, default=-1, help="Slice for development purposes, how many rows to process")
    parser.add_argument("--temperature", type=float, default=0.1, help="Temperature for the LLM")
    parser.add_argument("--max_tokens", type=int, default=1, help="Maximum number of tokens for the LLM response")
    return parser.parse_args()

def find_column_triplets(df, suffix1="_llm", suffix2="_human", suffix3="_verdict_llm"):
    """
    Returns a list of tuples (col_llm, col_human, col_verdict) for
    each base column that has all three suffixed versions present.
    """
    cols = set(df.columns)
    triplets = []
    for c in cols:
        if c.endswith(suffix1):
            base = c[:-len(suffix1)]
            h = base + suffix2
            v = base + suffix3
            if h in cols and v in cols:
                triplets.append((c, h, v))
    return triplets

def generate_response(llm_val, human_val, client, model_name, temperature, max_tokens):
    system_role = f"""
        You are a fair judge, who also happens to be an expert in drug approval processes. Your task is to compare the responses given by two annotators and determine whether they agree or not. Answer only with `True`, `False`, or `Partial`. No other comments or explanations are allowed, answer with one word. Compare the responses and answer with:\n
        - `True` if they are identical or contain the same meaning, even if e.g. spelling or formulations are slightly different but mean essentially the same thing (e.g. `rat, cat` and `cats, rats` means exactly the same);\n
        - `False` if the responses disagree;\n
        - `Partial` if there is a substantial overlap between the responses, but some parts are different (e.g. `rat, cat` and `rat, cat, dog`, or if the annotators agree on the year but disagree about the day and month e.g. `05.06.2011` vs `20.08.2011`).
        """
    prompt = f"""
        Do the two annotators agree on the response to the question?\n
        Annotator 1: {llm_val!r}\n
        Annotator 2: {human_val!r}\n
        Answer with only `True`, `False`, or `Partial`. If a response is missing, consider it to be `not reported`.\n\n
        Your verdict is:
        """

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_role},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )

    verdict = response.choices[0].message.content.strip()
    if verdict not in {"True", "False", "Partial"}:
        verdict = "Other"

    return verdict

def main():
    args = parse_arguments()
    api_key = load_env_variables()
    client = OpenAI(api_key=api_key)

    df = pd.read_csv(args.eval_sheet, dtype=str)
    df.fillna("", inplace=True)
    df = df[:args.slice_size]

    triplets = find_column_triplets(df)
    for llm_col, human_col, verdict_col in triplets:
        print(f"\nJudging column: {llm_col[0:-4]}")

        for idx, row in df.iterrows():
            llm_val = row[llm_col].strip()
            human_val = row[human_col].strip()
            try:
                verdict = generate_response(llm_val, human_val, client, args.model_name, args.temperature, args.max_tokens)
            except Exception as e:
                print(f"Error generating response for row {idx}: {e}")
                verdict = "ERROR"
            print(f"\tRow {idx}: {llm_val} vs {human_val} -> {verdict}")

            df.at[idx, verdict_col] = verdict

            if idx % 10 == 0:
                df.to_csv(args.output_file, index=False)

    df.to_csv(args.output_file, index=False, encoding="utf-8")

if __name__ == "__main__":
    main()

import pandas as pd
import json
import argparse

def load_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        df = pd.DataFrame(data)
        df = df.transpose()
    return df

def load_from_csv(file_path):
    return pd.read_csv(file_path, encoding='utf-8')

def merge_dfs_with_suffixes(df_llm, df_annotated,
                            key="Marketing_authorisation_number",
                            suffix1="_llm",
                            suffix2="_human",
                            suffix3="_verdict_human",
                            suffix4="_verdict_llm"):

    df1 = df_llm.copy()
    df2 = df_annotated.copy()
    df1[key] = df1[key].str.lower()
    df2[key] = df2[key].str.lower()
    df1 = df1.drop_duplicates(subset=key)
    df2 = df2.drop_duplicates(subset=key)

    common_keys = set(df1[key]).intersection(df2[key])
    df1 = df1[df1[key].isin(common_keys)]
    df2 = df2[df2[key].isin(common_keys)]

    common_cols = sorted(set(df1.columns).intersection(df2.columns))
    df1 = df1[common_cols]
    df2 = df2[common_cols]

    df1 = df1.rename(columns={c: f"{c}{suffix1}" for c in df1.columns})
    df2 = df2.rename(columns={c: f"{c}{suffix2}" for c in df2.columns})

    key1 = key + suffix1
    key2 = key + suffix2
    merged = pd.merge(df1, df2,
                      left_on=key1, 
                      right_on=key2,
                      how="inner")
    
    for col in merged.select_dtypes(include="object"):
        merged[col] = merged[col].str.strip()
        merged[col] = merged[col].str.lower()

    for c in common_cols:
        col1 = c + suffix1
        col2 = c + suffix2
        col3 = c + suffix3
        col4 = c + suffix4
        merged[col3] = merged[col1] == merged[col2]
        merged[col4] = ""
    merged = merged[sorted(merged.columns)]

    return merged

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="Create an evaluation sheet from LLM and human annotated data.")
    parser.add_argument("--llm_file", help="file path to the LLM data (json)")
    parser.add_argument("--human_file", help="file path to the human annotated data (csv)")
    parser.add_argument("--output_file", help="output file path to save the evaluation sheet (csv)")
    return parser.parse_args()

def main():
    args = parse_args()
    df_llm = load_from_json(args.llm_file)
    df_annotated = load_from_csv(args.human_file)

    merged_df = merge_dfs_with_suffixes(df_llm, df_annotated)

    merged_df.to_csv(args.output_file, index=False, encoding='utf-8')
    print(f"Evaluation sheet saved to {args.output_file}")



if __name__ == "__main__":
    main()
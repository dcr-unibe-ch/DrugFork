import pandas as pd
import json

def json_to_csv(json_file, csv_file):
    df = pd.read_json(json_file)
    df = df.transpose()
    return df

    # df.to_csv(csv_file, header=False)



input = "./inference/combined/EMA_manually_cleaned.json"
output = "./inference/combined/EMA_manually_cleaned.csv"

df = json_to_csv(input, output)
print(df.head())
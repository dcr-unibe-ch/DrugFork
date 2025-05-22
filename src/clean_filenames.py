import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser(description="Clean up file names in a directory.")
    parser.add_argument("--dir_path", help="The directory to clean up.")
    return parser.parse_args()

def clean_file_names(dir_path):
    for filename in os.listdir(dir_path):
        new_name = filename.strip().lower().replace(" ", "_")
        os.rename(os.path.join(dir_path, filename), os.path.join(dir_path, new_name))

def main():
    args = parse_args()
    clean_file_names(args.dir_path)
    print(f"Cleaned file names in directory: {args.dir_path}")

if __name__ == "__main__":
    main()
import argparse

def find_common_lines(eval_file, full_file):
    common_lines = []
    with open(eval_file, 'r') as f1, open(full_file, 'r') as f2:
        lines1 = set(line.strip() for line in f1)
        lines2 = set(line.strip() for line in f2)
        common_lines = lines1.intersection(lines2)
    return common_lines

def remove_common_lines(input_file, common_lines, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line.strip() not in common_lines:
                outfile.write(line)

def parse_args():
    parser = argparse.ArgumentParser(description="Remove common lines from a file based on another file's content.")
    parser.add_argument("--eval_list", help="File with evaluation lines.")
    parser.add_argument("--full_list", help="File with full lines (including eval).")
    parser.add_argument("--output_file", help="File to save the output without common lines.")
    return parser.parse_args()

def main():
    args = parse_args()
    common_lines = find_common_lines(args.eval_list, args.full_list)
    remove_common_lines(args.full_list, common_lines, args.output_file)


if __name__ == "__main__":
    main()
# pattern_generator.py
"""
Generates a file named 'common_patterns.txt' by analyzing three text files
stored in a 'datasets' folder:
  1) rockyou_dataset.txt
  2) hibp_dataset.txt
  3) crackstation_dataset.txt

Assumptions:
  - Each file has one password per line.
  - The 'datasets' folder is in the same directory as this script, or adjust paths accordingly.

Steps:
  1) Load lines from each .txt file in 'datasets/'.
  2) Combine all lines into one large list.
  3) Count frequency of each password using collections.Counter.
  4) Sort them by frequency (descending).
  5) Take the top N (default 500) and write them to 'common_patterns.txt'.

Usage:
  python pattern_generator.py

Adjust the 'TOP_N' constant at the bottom if you need more/fewer patterns.
"""

import os
import collections

# Adjust these paths if needed
ROCKYOU_FILE = os.path.join("datasets", "rockyou_dataset.txt")
HIBP_FILE = os.path.join("datasets", "hibp_dataset.txt")
CRACKSTATION_FILE = os.path.join("datasets", "crackstation_dataset.txt")
OUTPUT_FILE = "common_patterns.txt"

def load_passwords_from_txt(filepath):
    """
    Reads a text file line by line, stripping whitespace.
    Returns a list of passwords (strings).
    """
    passwords = []
    if not os.path.isfile(filepath):
        print(f"[WARNING] File not found: {filepath}")
        return passwords

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if line:
                passwords.append(line)
    return passwords


def generate_common_patterns(top_n=500):
    """
    Merges passwords from the three dataset files, counts their frequency,
    selects the top N most common, and writes them to OUTPUT_FILE.
    """
    # 1) Load from each dataset file
    rockyou_passwords = load_passwords_from_txt(ROCKYOU_FILE)
    hibp_passwords = load_passwords_from_txt(HIBP_FILE)
    crackstation_passwords = load_passwords_from_txt(CRACKSTATION_FILE)

    # 2) Combine into one list
    all_passwords = rockyou_passwords + hibp_passwords + crackstation_passwords

    # 3) Count frequency
    counter = collections.Counter(all_passwords)

    # 4) Grab the top N
    most_common = counter.most_common(top_n)

    # 5) Write results to common_patterns.txt
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for pwd, _count in most_common:
            f.write(pwd + "\n")

    print(f"[INFO] Wrote top {top_n} patterns to '{OUTPUT_FILE}'.")
    print(f"[INFO] Total lines processed = {len(all_passwords)}")
    print(f"[INFO] Unique passwords found = {len(counter.keys())}")


if __name__ == "__main__":
    generate_common_patterns(top_n=500)

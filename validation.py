# validation.py
import os
PATTERNS = os.path.join("validation", "common_patterns.txt")
def validate_password_against_common_patterns(password: str, patterns_file: str = PATTERNS) -> bool:
    """
    Checks if the given 'password' appears in the 'common_patterns.txt' file.
    
    :param password: The newly generated password you want to validate.
    :param patterns_file: Path to the patterns file containing one password per line.
    :return: True if 'password' is found in the patterns file (i.e. it's 'common'), otherwise False.
    """
    try:
        with open(patterns_file, "r", encoding="utf-8") as f:
            for line in f:
                # Strip whitespace and compare
                if line.strip() == password:
                    return True
    except FileNotFoundError:
        print(f"[WARNING] Patterns file not found: {patterns_file}")
        # If file is missing, treat it as if the password isn't found.
        # Or you could raise an exception instead.
        return False

    return False  # Not found in the list

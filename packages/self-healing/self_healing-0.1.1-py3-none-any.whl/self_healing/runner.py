import subprocess, re
from .patcher import healer
from .data.values import font, reset_font
from .data.detail import details

def count_inputs(text):
    inside_single = False  # Track if inside single quotes
    inside_double = False  # Track if inside double quotes
    inside_triple_single = False  # Track if inside triple single quotes
    inside_triple_double = False  # Track if inside triple double quotes

    i = 0
    input_count = 0  # Initialize the counter for input()

    while i < len(text):
        # Check for triple single quotes
        if text[i:i+3] == "'''" and not (inside_double or inside_triple_double):
            inside_triple_single = not inside_triple_single
            i += 3
            continue

        # Check for triple double quotes
        if text[i:i+3] == '"""' and not (inside_single or inside_triple_single):
            inside_triple_double = not inside_triple_double
            i += 3
            continue

        # Check for single quotes
        if text[i] == "'" and not (inside_double or inside_triple_single or inside_triple_double):
            inside_single = not inside_single
            i += 1
            continue

        # Check for double quotes
        if text[i] == '"' and not (inside_single or inside_triple_single or inside_triple_double):
            inside_double = not inside_double
            i += 1
            continue

        # Check for input()
        if re.match(r'input\((.*)\)', text[i:i+7]) and not (inside_single or inside_double or inside_triple_single or inside_triple_double):
            input_count += 1  # Increment the counter when input() is valid
            i += 6  # Skip past the "input("
            continue

        i += 1

    return input_count

class SelfHealingRunner:
    def __init__(self, code, error_message= "", detail= details):
        self.code = code
        self.error_message = error_message
        self.details = detail

    def run(self):
        if count_inputs(self.code) >= 1:
            print(f"{font.white}Program started.{font.yellow} Enter values if needed{font.white}!")
        else: print(f"{font.white}Program started. Checking...{font.white}")
        self.result = subprocess.run(
            ["python", "-c", self.code],
            capture_output=True,
            text=True )

        if self.result.returncode == 0:
            return {"status": "Success", "message": self.result.stdout, "error": False}
        else:
            self.error_message = str(self.result.stderr)[:-1]
            return {"status": "Error", "message": self.result.stderr, "error": True}

    def heal_code(self):
        # Placeholder for AI-powered healing logic
        if self.error_message[-1:] == "\n":
            self.error_message = self.error_message[:-1]
        bug = healer(self.error_message, self.details)
        bug.heal()
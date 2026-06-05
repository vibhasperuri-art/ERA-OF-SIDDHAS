import ast

def validate_python(filename):
    print(f"Validating Python file: {filename}")
    try:
        content = open(filename, encoding="utf-8").read()
        ast.parse(content)
        print(f"  [SUCCESS] {filename} compiled successfully!")
        return True
    except Exception as e:
        print(f"  [ERROR] Python syntax error in {filename}: {e}")
        return False

def validate_brackets(filename):
    print(f"Validating brackets in: {filename}")
    try:
        content = open(filename, encoding="utf-8").read()
        
        # Simple stack-based bracket validator
        stack = []
        mapping = {')': '(', ']': '[', '}': '{'}
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            for char_num, char in enumerate(line, 1):
                if char in '([{':
                    stack.append((char, line_num, char_num))
                elif char in ')]}':
                    if not stack:
                        print(f"  [ERROR] Unmatched closing bracket '{char}' at line {line_num}, char {char_num}")
                        return False
                    top, l, c = stack.pop()
                    if top != mapping[char]:
                        print(f"  [ERROR] Mismatched bracket '{char}' at line {line_num}, char {char_num} (matches '{top}' from line {l}, char {c})")
                        return False
                        
        if stack:
            top, l, c = stack[0]
            print(f"  [ERROR] Unclosed bracket '{top}' from line {l}, char {c}")
            return False
            
        print(f"  [SUCCESS] {filename} brackets are perfectly balanced!")
        return True
    except Exception as e:
        print(f"  [ERROR] Failed to read/validate {filename}: {e}")
        return False

# List of files we modified
python_files = ["server.py"]
html_files = [
    "index.html",
    "course_hub.html",
    "interactive_lesson.html",
    "chanting.html",
    "pillar_hub.html",
    "vicara_sannidhi.html",
    "wisdom_hub.html",
    "glossary.html",
    "about.html"
]

all_ok = True
for f in python_files:
    if not validate_python(f):
        all_ok = False

for f in html_files:
    if not validate_brackets(f):
        all_ok = False

if all_ok:
    print("\n>>> ALL FILES VALIDATED SUCCESSFULLY! <<<")
else:
    print("\n>>> VALIDATION FAILED! PLEASE CHECK ERRORS. <<<")

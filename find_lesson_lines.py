import os

path = r"C:\Users\rajpe\.gemini\antigravity\scratch\era_of_siddhas\interactive_lesson.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split("\n")
for idx, line in enumerate(lines):
    if ".glass-nav {" in line:
        print(f"Found .glass-nav at line {idx+1}")
    if "@media (max-width: 900px)" in line:
        print(f"Found @media (max-width: 900px) at line {idx+1}")

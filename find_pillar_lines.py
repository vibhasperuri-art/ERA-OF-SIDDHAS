import os

path = r"C:\Users\rajpe\.gemini\antigravity\scratch\era_of_siddhas\pillar_hub.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split("\n")
for idx, line in enumerate(lines):
    if "header {" in line:
        print(f"Found header style at line {idx+1}")
    if "@media" in line:
        print(f"Found @media at line {idx+1}")

import os

files = ["sanctum.html", "sangha.html", "chanting.html"]
directory = r"C:\Users\rajpe\.gemini\antigravity\scratch\era_of_siddhas"

for hf in files:
    path = os.path.join(directory, hf)
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # print the lines around </style>
    lines = content.split("\n")
    for idx, line in enumerate(lines):
        if "</style>" in line:
            print(f"File {hf}: Found </style> at line {idx+1}")
            # print previous 3 lines
            for j in range(max(0, idx-3), idx):
                print(f"  {j+1}: {lines[j]}")
            print()

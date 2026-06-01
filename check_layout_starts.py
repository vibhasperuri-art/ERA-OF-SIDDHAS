import os

files = ["sanctum.html", "sangha.html", "chanting.html"]
directory = r"C:\Users\rajpe\.gemini\antigravity\scratch\era_of_siddhas"

out_file = open("layout_starts_output.txt", "w", encoding="utf-8")

for hf in files:
    path = os.path.join(directory, hf)
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    nav_end = content.find("</nav>")
    if nav_end != -1:
        out_file.write(f"=== File: {hf} layout start ===\n")
        out_file.write(content[nav_end+6:nav_end+500].strip() + "\n")
        out_file.write("-" * 50 + "\n\n")

out_file.close()
print("Done checking layout starts.")

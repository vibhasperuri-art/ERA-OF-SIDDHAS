import os

path = r"C:\Users\rajpe\.gemini\antigravity\scratch\era_of_siddhas\interactive_lesson.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

out_file = open("lesson_layout_output.txt", "w", encoding="utf-8")

# Let's find body start and containers
body_idx = content.find("<body")
body_close_idx = content.find(">", body_idx)
out_file.write("=== BODY TAG ===\n")
out_file.write(content[body_idx:body_close_idx+1] + "\n\n")

# Find main content container
# e.g., the div following </nav>
nav_close = content.find("</nav>")
if nav_close != -1:
    out_file.write("=== AFTER NAV ===\n")
    out_file.write(content[nav_close+6:nav_close+1000] + "\n")

out_file.close()
print("Done parsing lesson layout.")

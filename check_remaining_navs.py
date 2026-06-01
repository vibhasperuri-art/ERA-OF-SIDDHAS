import os

files = ["sanctum.html", "sangha.html", "chanting.html"]
directory = r"C:\Users\rajpe\.gemini\antigravity\scratch\era_of_siddhas"

for hf in files:
    path = os.path.join(directory, hf)
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    style_idx = content.find("<style>")
    style_end = content.find("</style>")
    nav_idx = content.find("<nav")
    nav_end = content.find("</nav>")
    
    print(f"=== File: {hf} ===")
    if nav_idx != -1 and nav_end != -1:
        print("NAV tag line count:", content[nav_idx:nav_end].count("\n"))
    if style_idx != -1 and style_end != -1:
        style_content = content[style_idx:style_end]
        glass_pos = style_content.find(".glass-nav")
        if glass_pos != -1:
            print("glass-nav css snippet:")
            print(style_content[glass_pos:glass_pos+200])
    print()

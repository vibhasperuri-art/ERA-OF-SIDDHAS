import os

path = r"C:\Users\rajpe\.gemini\antigravity\scratch\era_of_siddhas\interactive_lesson.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

out_file = open("lesson_nav_output.txt", "w", encoding="utf-8")

# Find the nav tag
start_nav = content.find("<nav")
end_nav = content.find("</nav>", start_nav)
if start_nav != -1 and end_nav != -1:
    out_file.write("=== NAV BLOCK ===\n")
    out_file.write(content[start_nav:end_nav+6] + "\n\n")

# Find the CSS rules for .glass-nav
start_style = content.find("<style>")
end_style = content.find("</style>", start_style)
if start_style != -1 and end_style != -1:
    style_content = content[start_style:end_style]
    nav_css_pos = style_content.find(".glass-nav")
    if nav_css_pos != -1:
        out_file.write("=== GLASS-NAV CSS ===\n")
        out_file.write(style_content[nav_css_pos:nav_css_pos+800] + "\n")

out_file.close()
print("Done parsing lesson nav.")

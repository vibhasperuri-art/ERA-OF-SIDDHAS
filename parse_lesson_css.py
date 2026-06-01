import os

path = r"C:\Users\rajpe\.gemini\antigravity\scratch\era_of_siddhas\interactive_lesson.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

out_file = open("lesson_layout_css.txt", "w", encoding="utf-8")

# Find style block
start_style = content.find("<style>")
end_style = content.find("</style>", start_style)
if start_style != -1 and end_style != -1:
    style_content = content[start_style:end_style]
    
    # Extract workspace-layout rules
    classes = [".workspace-layout", ".left-pane", ".right-pane", "body"]
    for cls in classes:
        pos = style_content.find(cls)
        if pos != -1:
            out_file.write(f"=== {cls} STYLE ===\n")
            out_file.write(style_content[pos:pos+400] + "\n\n")

out_file.close()
print("Done parsing CSS.")

with open("interactive_lesson.html", encoding="utf-8") as f:
    for line_num, line in enumerate(f, 1):
        if "scientific" in line and (".text" in line or "['text']" in line):
            print(f"{line_num}: {line.strip()}")

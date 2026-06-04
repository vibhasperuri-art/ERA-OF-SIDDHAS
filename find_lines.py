import re

content = open("interactive_lesson.html", encoding="utf-8").read()

lessons_match = re.search(r"const lessons\s*=\s*\{", content)
if lessons_match:
    start_pos = lessons_match.start()
    subcontent = content[start_pos:]
    
    n_match = re.search(r"nagara\s*:\s*\{", subcontent)
    if n_match:
        n_start_global = start_pos + n_match.start()
        print(f"nagara start: char {n_start_global}")
        # let's look for vastu:, upanishads:, yoga:, sthapatya:
        for k in ["vastu", "upanishads", "yoga", "sthapatya"]:
            km = re.search(rf"\b{k}\s*:\s*\{{", subcontent[n_match.start():])
            if km:
                char_idx = n_start_global + km.start()
                line_no = content[:char_idx].count("\n") + 1
                print(f"  Lesson '{k}': starts around line {line_no}")
else:
    print("lessons not found")

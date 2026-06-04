import re

content = open("interactive_lesson.html", encoding="utf-8").read()

match = re.search(r"const lessons\s*=\s*\{", content)
if match:
    start_pos = match.start()
    subcontent = content[start_pos:start_pos+300000]
    
    pillar = "nagara"
    p_pattern = rf"{pillar}\s*:\s*\{{"
    p_match = re.search(p_pattern, subcontent)
    if p_match:
        p_start = p_match.end()
        bracket_count = 1
        p_end = p_start
        while bracket_count > 0 and p_end < len(subcontent):
            if subcontent[p_end] == '{':
                bracket_count += 1
            elif subcontent[p_end] == '}':
                bracket_count -= 1
            p_end += 1
        
        pillar_content = subcontent[p_start:p_end]
        
        # Let's extract each lesson block
        # vastu, upanishads, yoga, sthapatya
        lessons_keys = ["vastu", "upanishads", "yoga", "sthapatya"]
        for key in lessons_keys:
            print(f"\n=================== LESSON: {key} ===================")
            k_pattern = rf"{key}\s*:\s*\{{"
            k_match = re.search(k_pattern, pillar_content)
            if k_match:
                k_start = k_match.end()
                bc = 1
                k_end = k_start
                while bc > 0 and k_end < len(pillar_content):
                    if pillar_content[k_end] == '{':
                        bc += 1
                    elif pillar_content[k_end] == '}':
                        bc -= 1
                    k_end += 1
                lesson_block = pillar_content[k_start:k_end]
                # print lines from this lesson_block
                for line in lesson_block.split("\n"):
                    safe = line.strip().encode("ascii", "replace").decode("ascii")
                    # print category, title, scientific.title, scientific.text, dharmicPrinciples, etc.
                    if any(x in line for x in ["category:", "title:", "scientific:", "text:", "dharmicPrinciples:"]):
                        print(f"  {safe[:120]}")
            else:
                print(f"  {key} block not found")
else:
    print("lessons object not found")

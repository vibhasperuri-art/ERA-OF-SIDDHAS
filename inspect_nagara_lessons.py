import re

content = open("interactive_lesson.html", encoding="utf-8").read()

match = re.search(r"const lessons\s*=\s*\{", content)
if match:
    start_pos = match.start()
    subcontent = content[start_pos:start_pos+300000]
    
    pillars = ["nagara", "rajya", "yuddham"]
    for pillar in pillars:
        print(f"\n--- Pillar: {pillar} ---")
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
            
            sub_matches = re.finditer(r"^\s{4,6}([a-zA-Z0-9_]+)\s*:\s*\{", pillar_content, re.MULTILINE)
            for sm in sub_matches:
                key = sm.group(1)
                block_start = sm.end()
                cat_match = re.search(r"category\s*:\s*[\"']([^\"']+)[\"']", pillar_content[block_start:block_start+200])
                title_match = re.search(r"title\s*:\s*[\"']([^\"']+)[\"']", pillar_content[block_start:block_start+200])
                
                cat_str = cat_match.group(1).encode("ascii", "replace").decode("ascii") if cat_match else "N/A"
                title_str = title_match.group(1).encode("ascii", "replace").decode("ascii") if title_match else "N/A"
                print(f"  Key: {key}")
                print(f"    Category: {cat_str}")
                print(f"    Title: {title_str}")
        else:
            print(f"Pillar {pillar} not found")
else:
    print("lessons object not found")

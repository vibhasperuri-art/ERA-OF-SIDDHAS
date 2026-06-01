import os
import re

directory = r"C:\Users\rajpe\.gemini\antigravity\scratch\era_of_siddhas"
html_files = ["index.html", "course_hub.html", "interactive_lesson.html", "admin.html", "sangha.html", "sanctum.html", "chanting.html"]

for hf in html_files:
    path = os.path.join(directory, hf)
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extract style block
    style_blocks = re.findall(r"<style>(.*?)</style>", content, re.DOTALL)
    print(f"=== File: {hf} style analysis ===")
    for sb in style_blocks:
        # Find any media query blocks in this style block
        # A simple parser for @media {...} blocks in style block
        pos = 0
        while True:
            match = re.search(r"@media", sb[pos:])
            if not match:
                break
            start = pos + match.start()
            # find matching braces
            brace_count = 0
            end = -1
            for j in range(start, len(sb)):
                if sb[j] == '{':
                    brace_count += 1
                elif sb[j] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end = j + 1
                        break
            if end != -1:
                media_block = sb[start:end]
                print(media_block)
                print("-" * 40)
                pos = end
            else:
                pos = start + 6
    print()

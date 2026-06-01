import os
import re
import sys

# Redirect stdout and stderr to search_output.txt
out_file = open("search_output.txt", "w", encoding="utf-8", buffering=1)
sys.stdout = out_file
sys.stderr = out_file

try:
    directory = r"C:\Users\rajpe\.gemini\antigravity\scratch\era_of_siddhas"
    html_files = [f for f in os.listdir(directory) if f.endswith(".html")]

    for hf in html_files:
        path = os.path.join(directory, hf)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Look for theme switchers and layouts
        set_theme_matches = re.findall(r"(<button[^>]*setTheme[^>]*>.*?</button>)", content)
        nav_blocks = re.findall(r"(<nav[^>]*>.*?</nav>)", content, re.DOTALL)
        media_queries = re.findall(r"(@media[^{]*\{[^}]*\})", content, re.DOTALL)
        
        print(f"=== File: {hf} ===")
        if set_theme_matches:
            print(f"Found {len(set_theme_matches)} setTheme buttons.")
            for btn in set_theme_matches:
                print("  ", btn.strip())
        if nav_blocks:
            print(f"Found nav block (first 500 chars):")
            print(nav_blocks[0][:500].strip() + "...")
        if media_queries:
            print(f"Found media queries:")
            for mq in media_queries:
                print("  ", mq.strip().replace("\n", " "))
        print()
    print("Done search.")
except Exception as e:
    print("Error:", e)
finally:
    out_file.close()

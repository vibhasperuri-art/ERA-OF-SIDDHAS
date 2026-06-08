import os
import re
import sys

# Force UTF-8 encoding for standard output
sys.stdout.reconfigure(encoding='utf-8')

workspace = r"C:\Users\rajpe\.gemini\antigravity\scratch\era_of_siddhas"

if not os.path.exists(workspace):
    print(f"Workspace {workspace} does not exist!")
    sys.exit(1)

count = 0
for filename in os.listdir(workspace):
    if filename.endswith(".html") and filename != "gift_wisdom.html":
        filepath = os.path.join(workspace, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already has gift_wisdom.html link
        if "gift_wisdom.html" in content:
            print(f"Skipping {filename}: already has gift_wisdom.html link.")
            continue
            
        # Pattern to find the Vicara Sannidhi link in navbars
        # It can be a href="vicara_sannidhi.html" or href="vicara_sannidhi.html?mode=wisdom" etc.
        # It can have different class attributes, including "active"
        pattern = r'(<a\s+href=["\']vicara_sannidhi\.html[^"\']*["\']\s+class=["\']nav-btn[^"\']*["\'](?:[^>]*?)>.*?</a>)'
        
        # Replace and insert the new Gift Wisdom link after it
        new_link = '\n    <a href="gift_wisdom.html" class="nav-btn">Gift Wisdom</a>'
        new_content, n = re.subn(pattern, r'\1' + new_link, content, flags=re.IGNORECASE)
        
        if n > 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filename}: added Gift Wisdom link to navigation menu ({n} replacements).")
            count += 1
        else:
            # Fallback: find any other nav link if vicara_sannidhi.html isn't present
            pattern_fallback = r'(<a\s+href=["\']about\.html["\']\s+class=["\']nav-btn[^"\']*["\'](?:[^>]*?)>.*?</a>)'
            new_link_fallback = '\n    <a href="gift_wisdom.html" class="nav-btn">Gift Wisdom</a>\n    '
            new_content, n = re.subn(pattern_fallback, new_link_fallback + r'\1', content, flags=re.IGNORECASE)
            if n > 0:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {filename} via fallback: added Gift Wisdom link before About link ({n} replacements).")
                count += 1
            else:
                print(f"Could not find nav menu anchor in {filename}.")

print(f"Finished updating navigation menus across {count} files.")

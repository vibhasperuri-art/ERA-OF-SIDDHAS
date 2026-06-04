import re

files_with_animation = [
    "index.html",
    "course_hub.html",
    "interactive_lesson.html",
    "chanting.html",
    "pillar_hub.html"
]

def patch_file_with_animation(filename):
    print(f"Patching {filename}...")
    content = open(filename, encoding="utf-8").read()
    
    # Locate the target block
    # We want to replace the mousemove, animateRing, and custom-cursor-active blocks
    target_pattern = r"document\.addEventListener\('mousemove',\s*\(e\)\s*=>\s*\{[^}]*mouseX\s*=\s*e\.clientX;[^}]*\}\);\s*function\s+animateRing\(\)\s*\{[^}]*\}\s*if\s*\(cursor\s*&&\s*cursorRing\)\s*\{[^}]*classList\.add\('custom-cursor-active'\);[^}]*animateRing\(\);[^}]*\}"
    
    # Or let's use a simpler, more precise string replacement since the whitespace might differ slightly.
    # Let's inspect the block from index.html:
    # document.addEventListener('mousemove', (e) => {
    #   mouseX = e.clientX;
    #   mouseY = e.clientY;
    #   cursor.style.left = mouseX + 'px';
    #   cursor.style.top = mouseY + 'px';
    # });
    # 
    # function animateRing() {
    #   ringX += (mouseX - ringX) * 0.2;
    #   ringY += (mouseY - ringY) * 0.2;
    #   cursorRing.style.left = ringX + 'px';
    #   cursorRing.style.top = ringY + 'px';
    #   requestAnimationFrame(animateRing);
    # }
    # 
    # if (cursor && cursorRing) {
    #   document.body.classList.add('custom-cursor-active');
    #   animateRing();
    # }
    
    old_block_nospace = """document.addEventListener('mousemove', (e) => {
  mouseX = e.clientX;
  mouseY = e.clientY;
  cursor.style.left = mouseX + 'px';
  cursor.style.top = mouseY + 'px';
});

function animateRing() {
  ringX += (mouseX - ringX) * 0.2;
  ringY += (mouseY - ringY) * 0.2;
  cursorRing.style.left = ringX + 'px';
  cursorRing.style.top = ringY + 'px';
  requestAnimationFrame(animateRing);
}

if (cursor && cursorRing) {
  document.body.classList.add('custom-cursor-active');
  animateRing();
}"""

    # We also check if there is indentation in files like pillar_hub.html
    # Let's normalize spaces and perform a regex replace or look for matches
    
    # Regex pattern to match the block:
    pattern = re.compile(
        r"document\.addEventListener\('mousemove',\s*\(e\)\s*=>\s*\{\s*"
        r"mouseX\s*=\s*e\.clientX;\s*"
        r"mouseY\s*=\s*e\.clientY;\s*"
        r"cursor\.style\.left\s*=\s*mouseX\s*\+\s*['\"]px['\"];\s*"
        r"cursor\.style\.top\s*=\s*mouseY\s*\+\s*['\"]px['\"];\s*"
        r"\}\);\s*"
        r"function\s+animateRing\(\)\s*\{\s*"
        r"ringX\s*\+=\s*\(mouseX\s*-\s*ringX\s*\)\s*\*\s*0\.2;\s*"
        r"ringY\s*\+=\s*\(mouseY\s*-\s*ringY\s*\)\s*\*\s*0\.2;\s*"
        r"cursorRing\.style\.left\s*=\s*ringX\s*\+\s*['\"]px['\"];\s*"
        r"cursorRing\.style\.top\s*=\s*ringY\s*\+\s*['\"]px['\"];\s*"
        r"requestAnimationFrame\(animateRing\);\s*"
        r"\}\s*"
        r"if\s*\(cursor\s*&&\s*cursorRing\)\s*\{\s*"
        r"document\.body\.classList\.add\('custom-cursor-active'\);\s*"
        r"animateRing\(\);\s*"
        r"\}",
        re.MULTILINE
    )
    
    new_block = """if (cursor && cursorRing) {
    document.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      cursor.style.left = mouseX + 'px';
      cursor.style.top = mouseY + 'px';
      if (!document.body.classList.contains('custom-cursor-active')) {
        document.body.classList.add('custom-cursor-active');
      }
    });

    function animateRing() {
      ringX += (mouseX - ringX) * 0.2;
      ringY += (mouseY - ringY) * 0.2;
      cursorRing.style.left = ringX + 'px';
      cursorRing.style.top = ringY + 'px';
      requestAnimationFrame(animateRing);
    }
    animateRing();
  }"""
    
    new_content, count = pattern.subn(new_block, content)
    if count > 0:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"  [SUCCESS] Patched {filename} ({count} replacement)")
    else:
        # Let's try matching with slightly different formatting or indentation
        # Sometimes there's spaces at the start of lines
        print(f"  [WARNING] Regex didn't match {filename}. Trying fallback replacement...")
        # Fallback search and replace using substring matching with wildcard spaces
        # Let's look for standard patterns and replace them
        # We can construct a dynamic regex that handles indentation
        indented_pattern = re.compile(
            r"([ \t]*)document\.addEventListener\('mousemove',.*?"
            r"if\s*\(cursor\s*&&\s*cursorRing\)\s*\{\s*"
            r"\1document\.body\.classList\.add\('custom-cursor-active'\);\s*"
            r"\1animateRing\(\);\s*"
            r"\s*\}",
            re.DOTALL
        )
        def repl(m):
            indent = m.group(1)
            return f"""{indent}if (cursor && cursorRing) {{
{indent}  document.addEventListener('mousemove', (e) => {{
{indent}    mouseX = e.clientX;
{indent}    mouseY = e.clientY;
{indent}    cursor.style.left = mouseX + 'px';
{indent}    cursor.style.top = mouseY + 'px';
{indent}    if (!document.body.classList.contains('custom-cursor-active')) {{
{indent}      document.body.classList.add('custom-cursor-active');
{indent}    }}
{indent}  }});

{indent}  function animateRing() {{
{indent}    ringX += (mouseX - ringX) * 0.2;
{indent}    ringY += (mouseY - ringY) * 0.2;
{indent}    cursorRing.style.left = ringX + 'px';
{indent}    cursorRing.style.top = ringY + 'px';
{indent}    requestAnimationFrame(animateRing);
{indent}  }}
{indent}  animateRing();
{indent}}}"""
        new_content, count = indented_pattern.subn(repl, content)
        if count > 0:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"  [SUCCESS] Patched {filename} using indented fallback ({count} replacement)")
        else:
            print(f"  [ERROR] Failed to patch {filename}")

for fn in files_with_animation:
    patch_file_with_animation(fn)

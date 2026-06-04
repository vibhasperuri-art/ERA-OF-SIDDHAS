# Append patching for wisdom_hub.html and vicara_sannidhi.html
import re

def patch_wisdom_hub():
    print("Patching wisdom_hub.html...")
    content = open("wisdom_hub.html", encoding="utf-8").read()
    
    # Target:
    #   // Custom Cursor Logic
    #   const cursor = document.getElementById('cursor');
    #   const cursorRing = document.getElementById('cursor-ring');
    # 
    #   document.addEventListener('mousemove', (e) => {
    #     if (cursor) {
    #       cursor.style.left = e.clientX + 'px';
    #       cursor.style.top = e.clientY + 'px';
    #     }
    #     if (cursorRing) {
    #       cursorRing.style.left = e.clientX + 'px';
    #       cursorRing.style.top = e.clientY + 'px';
    #     }
    #   });
    # 
    #   if (cursor && cursorRing) {
    #     document.body.classList.add('custom-cursor-active');
    #   }
    
    pattern = re.compile(
        r"// Custom Cursor Logic\s*"
        r"const cursor\s*=\s*document\.getElementById\('cursor'\);\s*"
        r"const cursorRing\s*=\s*document\.getElementById\('cursor-ring'\);\s*"
        r"document\.addEventListener\('mousemove',\s*\(e\)\s*=>\s*\{\s*"
        r"if\s*\(cursor\)\s*\{\s*cursor\.style\.left\s*=\s*e\.clientX\s*\+\s*['\"]px['\"];\s*cursor\.style\.top\s*=\s*e\.clientY\s*\+\s*['\"]px['\"];\s*\}\s*"
        r"if\s*\(cursorRing\)\s*\{\s*cursorRing\.style\.left\s*=\s*e\.clientX\s*\+\s*['\"]px['\"];\s*cursorRing\.style\.top\s*=\s*e\.clientY\s*\+\s*['\"]px['\"];\s*\}\s*"
        r"\}\);\s*"
        r"if\s*\(cursor\s*&&\s*cursorRing\)\s*\{\s*"
        r"document\.body\.classList\.add\('custom-cursor-active'\);\s*"
        r"\}",
        re.DOTALL
    )
    
    replacement = """// Custom Cursor Logic
  const cursor = document.getElementById('cursor');
  const cursorRing = document.getElementById('cursor-ring');

  if (cursor && cursorRing) {
    document.addEventListener('mousemove', (e) => {
      cursor.style.left = e.clientX + 'px';
      cursor.style.top = e.clientY + 'px';
      cursorRing.style.left = e.clientX + 'px';
      cursorRing.style.top = e.clientY + 'px';
      if (!document.body.classList.contains('custom-cursor-active')) {
        document.body.classList.add('custom-cursor-active');
      }
    });
  }"""
    
    new_content, count = pattern.subn(replacement, content)
    if count > 0:
        with open("wisdom_hub.html", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("  [SUCCESS] Patched wisdom_hub.html")
    else:
        print("  [ERROR] Failed to patch wisdom_hub.html with regex, trying substring replacement")
        # Let's do a direct replacement of the tail part
        old_part = """  document.addEventListener('mousemove', (e) => {
    if (cursor) {
      cursor.style.left = e.clientX + 'px';
      cursor.style.top = e.clientY + 'px';
    }
    if (cursorRing) {
      cursorRing.style.left = e.clientX + 'px';
      cursorRing.style.top = e.clientY + 'px';
    }
  });

  if (cursor && cursorRing) {
    document.body.classList.add('custom-cursor-active');
  }"""
        
        new_part = """  if (cursor && cursorRing) {
    document.addEventListener('mousemove', (e) => {
      cursor.style.left = e.clientX + 'px';
      cursor.style.top = e.clientY + 'px';
      cursorRing.style.left = e.clientX + 'px';
      cursorRing.style.top = e.clientY + 'px';
      if (!document.body.classList.contains('custom-cursor-active')) {
        document.body.classList.add('custom-cursor-active');
      }
    });
  }"""
        if old_part in content:
            new_content = content.replace(old_part, new_part)
            with open("wisdom_hub.html", "w", encoding="utf-8") as f:
                f.write(new_content)
            print("  [SUCCESS] Patched wisdom_hub.html using fallback")
        else:
            print("  [ERROR] Fallback replacement failed for wisdom_hub.html")

def patch_vicara_sannidhi():
    print("Patching vicara_sannidhi.html...")
    content = open("vicara_sannidhi.html", encoding="utf-8").read()
    
    old_part = """const cursor = document.getElementById('cursor');
const cursorRing = document.getElementById('cursor-ring');

document.addEventListener('mousemove', (e) => {
  cursor.style.left = e.clientX + 'px';
  cursor.style.top = e.clientY + 'px';
  cursorRing.style.left = e.clientX + 'px';
  cursorRing.style.top = e.clientY + 'px';
});

document.body.classList.add('custom-cursor-active');"""

    new_part = """const cursor = document.getElementById('cursor');
const cursorRing = document.getElementById('cursor-ring');

if (cursor && cursorRing) {
  document.addEventListener('mousemove', (e) => {
    cursor.style.left = e.clientX + 'px';
    cursor.style.top = e.clientY + 'px';
    cursorRing.style.left = e.clientX + 'px';
    cursorRing.style.top = e.clientY + 'px';
    if (!document.body.classList.contains('custom-cursor-active')) {
      document.body.classList.add('custom-cursor-active');
    }
  });
}"""

    if old_part in content:
        new_content = content.replace(old_part, new_part)
        with open("vicara_sannidhi.html", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("  [SUCCESS] Patched vicara_sannidhi.html")
    else:
        # Check with slightly different spacings
        pattern = re.compile(
            r"const cursor\s*=\s*document\.getElementById\('cursor'\);\s*"
            r"const cursorRing\s*=\s*document\.getElementById\('cursor-ring'\);\s*"
            r"document\.addEventListener\('mousemove',\s*\(e\)\s*=>\s*\{\s*"
            r"cursor\.style\.left\s*=\s*e\.clientX\s*\+\s*['\"]px['\"];\s*"
            r"cursor\.style\.top\s*=\s*e\.clientY\s*\+\s*['\"]px['\"];\s*"
            r"cursorRing\.style\.left\s*=\s*e\.clientX\s*\+\s*['\"]px['\"];\s*"
            r"cursorRing\.style\.top\s*=\s*e\.clientY\s*\+\s*['\"]px['\"];\s*"
            r"\}\);\s*"
            r"document\.body\.classList\.add\('custom-cursor-active'\);",
            re.DOTALL
        )
        new_content, count = pattern.subn(new_part, content)
        if count > 0:
            with open("vicara_sannidhi.html", "w", encoding="utf-8") as f:
                f.write(new_content)
            print("  [SUCCESS] Patched vicara_sannidhi.html using regex")
        else:
            print("  [ERROR] Failed to patch vicara_sannidhi.html")

patch_wisdom_hub()
patch_vicara_sannidhi()

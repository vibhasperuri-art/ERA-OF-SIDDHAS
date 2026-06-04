import re

files = [
    "index.html",
    "course_hub.html",
    "interactive_lesson.html",
    "vicara_sannidhi.html",
    "wisdom_hub.html",
    "chanting.html",
    "pillar_hub.html"
]

def patch_file(filename):
    print(f"Adding cursor opacity to {filename}...")
    content = open(filename, encoding="utf-8").read()
    
    # 1. Add opacity: 0 to .custom-cursor
    # We look for .custom-cursor definition and insert opacity: 0; and add opacity to transition
    cursor_pattern = re.compile(
        r"(\.custom-cursor\s*\{\s*position:\s*fixed;.*?transition:\s*[^;]*?)(;[ \t\r\n]*box-shadow:[^;]*;)",
        re.DOTALL
    )
    
    # Let's do direct string replacements since they are highly consistent
    # For .custom-cursor:
    old_cursor_style = """  .custom-cursor {
    position: fixed;
    top: 0; left: 0;
    width: 8px; height: 8px;
    background: var(--gold-bright);
    border-radius: 50%;
    pointer-events: none;
    z-index: 1000002;
    transform: translate(-50%, -50%);
    transition: width 0.3s, height 0.3s, background 0.3s;
    box-shadow: 0 0 15px 3px var(--gold-bright);
  }"""

    new_cursor_style = """  .custom-cursor {
    position: fixed;
    top: 0; left: 0;
    width: 8px; height: 8px;
    background: var(--gold-bright);
    border-radius: 50%;
    pointer-events: none;
    z-index: 1000002;
    transform: translate(-50%, -50%);
    transition: width 0.3s, height 0.3s, background 0.3s, opacity 0.3s;
    box-shadow: 0 0 15px 3px var(--gold-bright);
    opacity: 0;
  }"""

    # For .custom-cursor-ring:
    old_ring_style = """  .custom-cursor-ring {
    position: fixed;
    top: 0; left: 0;
    width: 44px; height: 44px;
    border: 1.5px solid var(--gold);
    border-radius: 50%;
    pointer-events: none;
    z-index: 1000001;
    transform: translate(-50%, -50%);
    transition: transform 0.15s ease-out, width 0.3s, height 0.3s, border-color 0.3s;
    box-shadow: inset 0 0 10px var(--glow), 0 0 10px var(--glow);
  }"""

    new_ring_style = """  .custom-cursor-ring {
    position: fixed;
    top: 0; left: 0;
    width: 44px; height: 44px;
    border: 1.5px solid var(--gold);
    border-radius: 50%;
    pointer-events: none;
    z-index: 1000001;
    transform: translate(-50%, -50%);
    transition: transform 0.15s ease-out, width 0.3s, height 0.3s, border-color 0.3s, opacity 0.3s;
    box-shadow: inset 0 0 10px var(--glow), 0 0 10px var(--glow);
    opacity: 0;
  }"""

    # We also need to add the active opacity rule:
    # body.custom-cursor-active .custom-cursor,
    # body.custom-cursor-active .custom-cursor-ring {
    #   opacity: 1;
    # }
    # We can append this right after body.custom-cursor-active style
    old_active_body = """  body.custom-cursor-active,
  body.custom-cursor-active a,
  body.custom-cursor-active button,
  body.custom-cursor-active .tab,
  body.custom-cursor-active .article-card,
  body.custom-cursor-active .theme-btn {
    cursor: none !important;
  }"""
    
    new_active_body = old_active_body + """
  body.custom-cursor-active .custom-cursor,
  body.custom-cursor-active .custom-cursor-ring {
    opacity: 1;
  }"""

    # For index.html, vicara_sannidhi.html, etc., the classes might be slightly different in the body selector list.
    # Let's check and replace them or just add a general rule:
    active_rule = """
  body.custom-cursor-active .custom-cursor,
  body.custom-cursor-active .custom-cursor-ring {
    opacity: 1 !important;
  }"""

    modified = False
    if old_cursor_style in content:
        content = content.replace(old_cursor_style, new_cursor_style)
        modified = True
    else:
        # Check for slight spacing/newlines differences and replace
        # Let's try matching with regex
        pattern_cursor = re.compile(
            r"(\.custom-cursor\s*\{\s*position:\s*fixed;.*?transition:\s*[^;]*?)(;[ \t\r\n]*box-shadow:[^;]*;\s*\})",
            re.DOTALL
        )
        content, count = pattern_cursor.subn(r"\1, opacity 0.3s\2", content)
        if count > 0:
            # Add opacity: 0; before the closing }
            # Wait, let's just make it simple:
            # Find the closing brace of .custom-cursor and add opacity: 0;
            # A regex pattern is safer
            content = re.sub(r"(\.custom-cursor\s*\{[^}]*?box-shadow:[^;]*;)", r"\1\n    opacity: 0;", content)
            modified = True

    if old_ring_style in content:
        content = content.replace(old_ring_style, new_ring_style)
        modified = True
    else:
        # Check for ring style and patch
        content = re.sub(
            r"(\.custom-cursor-ring\s*\{\s*position:\s*fixed;.*?transition:\s*[^;]*?)(;[ \t\r\n]*box-shadow:[^;]*;\s*\})",
            r"\1, opacity 0.3s\2",
            content,
            flags=re.DOTALL
        )
        content = re.sub(r"(\.custom-cursor-ring\s*\{[^}]*?box-shadow:[^;]*;)", r"\1\n    opacity: 0;", content)
        modified = True

    # Check if we already have the active rule, otherwise add it
    if "body.custom-cursor-active .custom-cursor" not in content:
        # Insert active_rule before </style>
        content = content.replace("</style>", active_rule + "\n</style>")
        modified = True

    if modified:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  [SUCCESS] Patched {filename}")
    else:
        print(f"  [WARNING] No changes made to {filename}")

for fn in files:
    patch_file(fn)

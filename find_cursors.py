import glob

files = ["chanting.html", "course_hub.html", "index.html", "interactive_lesson.html", "pillar_hub.html", "vicara_sannidhi.html", "wisdom_hub.html"]

for f in files:
    try:
        content = open(f, encoding="utf-8").read()
        has_cursor_div = 'id="cursor"' in content or "id='cursor'" in content
        has_ring_div = 'id="cursor-ring"' in content or "id='cursor-ring'" in content
        print(f"{f}: has_cursor_div={has_cursor_div}, has_ring_div={has_ring_div}")
    except Exception as e:
        print(f"Error {f}: {e}")

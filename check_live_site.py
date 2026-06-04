import urllib.request
import sys

urls = {
    "Wisdom Hub": "https://vibhasperuri-art.github.io/ERA-OF-SIDDHAS/wisdom_hub.html",
    "Interactive Lesson": "https://vibhasperuri-art.github.io/ERA-OF-SIDDHAS/interactive_lesson.html",
    "Vicara Sannidhi": "https://vibhasperuri-art.github.io/ERA-OF-SIDDHAS/vicara_sannidhi.html"
}

all_good = True
for name, url in urls.items():
    print(f"Checking live {name} at: {url}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8")
            
            # Check for cursor touch screen fix
            if "if (cursor && cursorRing)" in html:
                print(f"  [PASS] Custom cursor refactoring is present in the code.")
            else:
                print(f"  [FAIL] Custom cursor refactoring not found!")
                all_good = False
                
            # Content checks
            if name == "Wisdom Hub":
                if "Manasara (Manasara Shilpa Shastra)" in html and "Aparajita Priccha" in html:
                    print(f"  [PASS] Samhitas content is present in Wisdom Hub.")
                else:
                    print(f"  [FAIL] Samhitas content not found in Wisdom Hub!")
                    all_good = False
            elif name == "Interactive Lesson":
                if "Mayamatam in Action: The Lotus City of Madurai" in html and "The Agamas & Dahara Vidya" in html:
                    print(f"  [PASS] Concentric zoning and Agamas are present in the curriculum.")
                else:
                    print(f"  [FAIL] Concentric zoning or Agamas not found in the curriculum!")
                    all_good = False
    except Exception as e:
        print(f"  [ERROR] Failed to fetch or check {name}: {e}")
        all_good = False

if all_good:
    print("\n>>> VERIFICATION COMPLETE: ALL LIVE PAGES ARE FULLY UPDATED AND CORRECT! <<<")
else:
    print("\n>>> VERIFICATION FAILED: SOME CHANGES ARE NOT YET REFLECTED ON THE LIVE SITE! <<<")

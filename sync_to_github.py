"""Sync project files to GitHub using PyGitHub REST API."""
import os, base64, json, time
from urllib.request import urlopen, Request
from urllib.error import HTTPError

REPO = "vibhasperuri-art/ERA-OF-SIDDHAS"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
BRANCH = "main"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Files to sync (relative paths)
FILES_TO_SYNC = [
    "server.py",
    "js/api.js",
    "requirements.txt",
    "render.yaml",
    "index.html",
    "about.html",
    "admin.html",
    "begin-journey.html",
    "chanting.html",
    "course_hub.html",
    "gift_wisdom.html",
    "glossary.html",
    "interactive_lesson.html",
    "pillar_hub.html",
    "sangha.html",
    "vicara_sannidhi.html",
    "wisdom_hub.html",
    "manifest.json",
    "sitemap.xml",
    "sw.js",
]

def gh_api(endpoint, method="GET", data=None):
    url = f"https://api.github.com/repos/{REPO}/{endpoint}"
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "EOS-Sync"
    }
    body = json.dumps(data).encode() if data else None
    req = Request(url, data=body, headers=headers, method=method)
    try:
        resp = urlopen(req)
        return json.loads(resp.read().decode())
    except HTTPError as e:
        err_body = e.read().decode()
        print(f"  HTTP {e.code}: {err_body[:200]}")
        return None

def get_file_sha(path):
    result = gh_api(f"contents/{path}?ref={BRANCH}")
    if result and "sha" in result:
        return result["sha"]
    return None

def upload_file(rel_path):
    full_path = os.path.join(BASE_DIR, rel_path.replace("/", os.sep))
    if not os.path.exists(full_path):
        print(f"  SKIP (not found): {rel_path}")
        return False
    
    with open(full_path, "rb") as f:
        content = base64.b64encode(f.read()).decode()
    
    sha = get_file_sha(rel_path)
    data = {
        "message": f"Cloud deploy: update {rel_path}",
        "content": content,
        "branch": BRANCH,
    }
    if sha:
        data["sha"] = sha
    
    result = gh_api(f"contents/{rel_path}", method="PUT", data=data)
    if result and "content" in result:
        print(f"  OK: {rel_path}")
        return True
    else:
        print(f"  FAIL: {rel_path}")
        return False

def main():
    if not TOKEN:
        print("ERROR: Set GITHUB_TOKEN environment variable first!")
        print("  PowerShell: $env:GITHUB_TOKEN = 'ghp_your_token_here'")
        return
    
    print(f"Syncing {len(FILES_TO_SYNC)} files to {REPO}...")
    ok = 0
    fail = 0
    for f in FILES_TO_SYNC:
        print(f"Uploading: {f}")
        if upload_file(f):
            ok += 1
        else:
            fail += 1
        time.sleep(0.5)  # rate limit
    
    print(f"\nDone! {ok} uploaded, {fail} failed.")

if __name__ == "__main__":
    main()

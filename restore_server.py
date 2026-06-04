import urllib.request

url = "https://raw.githubusercontent.com/vibhasperuri-art/ERA-OF-SIDDHAS/main/server.py"
try:
    print("Downloading clean server.py from GitHub...")
    response = urllib.request.urlopen(url)
    clean_code = response.read()
    with open("server.py", "wb") as f:
        f.write(clean_code)
    print("Successfully restored server.py to clean state!")
except Exception as e:
    print(f"Error restoring server.py: {e}")

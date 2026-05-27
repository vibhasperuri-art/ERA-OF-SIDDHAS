import sys
import os

# Redirect stdout and stderr to a log file immediately so we can view it
log_file = open(r"C:\Users\rajpe\.gemini\antigravity\scratch\era_of_siddhas\server.log", "w", encoding="utf-8", buffering=1)
sys.stdout = log_file
sys.stderr = log_file

print("Starting server runner script...")
print("Current Working Directory:", os.getcwd())

try:
    import uvicorn
    from server import app
    print("Dependencies imported successfully. Starting uvicorn...")
    log_file.flush()
    uvicorn.run(app, host="127.0.0.1", port=8080, log_level="debug")
except Exception as e:
    print("FATAL ERROR starting uvicorn:", e)
    log_file.flush()

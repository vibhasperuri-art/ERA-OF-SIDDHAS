import os

# Directory containing the HTML files
BASE_DIR = r"C:\Users\rajpe\.gemini\antigravity\scratch\era_of_siddhas"

def restore_file(filepath):
    print(f"Processing {filepath}...")
    try:
        # Read the file as UTF-8 (which currently yields the mojibake characters)
        with open(filepath, 'r', encoding='utf-8-sig') as f: # utf-8-sig automatically handles and strips the BOM
            corrupted_text = f.read()
        
        # Encode back to cp1252 bytes to recover the original raw bytes
        original_bytes = corrupted_text.encode('cp1252')
        
        # Decode the recovered bytes as UTF-8 to get the clean text
        restored_text = original_bytes.decode('utf-8')
        
        # Write the clean text back as UTF-8 (without BOM)
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            f.write(restored_text)
            
        print(f"  [SUCCESS] Restored {os.path.basename(filepath)}")
    except Exception as e:
        print(f"  [ERROR] Failed to restore {os.path.basename(filepath)}: {e}")

def main():
    # Process all HTML files in the base directory
    for file in os.listdir(BASE_DIR):
        if file.endswith(".html"):
            filepath = os.path.join(BASE_DIR, file)
            restore_file(filepath)

if __name__ == "__main__":
    main()

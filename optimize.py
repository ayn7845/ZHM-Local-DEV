import os
import re

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        content = file.read()
    
    if not re.search(r'owner\s*=\s*(WST|TUM|CHO)', content, re.IGNORECASE):
        return False
    
    #content = re.sub(r'buildings\s*=\s*\{[^}]*(?:\{[^}]*\}[^}]*)*\}', '', content, flags=re.DOTALL)

    #content = re.sub(r'resources\s*=\s*\{[^}]*(?:\{[^}]*\}[^}]*)*\}', '', content, flags=re.DOTALL)
    
    content = re.sub(r'victory_points\s*=\s*\{[^}]*(?:\{[^}]*\}[^}]*)*\}', '', content, flags=re.DOTALL)
    
    content = re.sub(r'local_supplies\s*=\s*[\d\.]+', 'local_supplies = 0.0', content)
    
    content = re.sub(r'manpower\s*=\s*[\d\.]+', 'manpower = 1', content)
    
    content = re.sub(r'state_category\s*=\s*\w+', 'state_category = wasteland', content)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    return True

def scan_and_process_directory(directory):
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                if process_file(file_path):
                    print(f"Processed: {file_path}")
                else:
                    print(f"Skipped: {file_path}")

directory_to_scan = input("Enter the directory path to scan: ").strip()
if os.path.isdir(directory_to_scan):
    scan_and_process_directory(directory_to_scan)
else:
    print("Invalid directory path.")
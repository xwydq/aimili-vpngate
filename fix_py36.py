import os
import re
import subprocess

FILES = [
    "vpn_utils.py",
    "proxy_server.py",
    "vpngate_manager.py"
]

def fix_subprocess(content):
    content = content.replace("capture_output=True, text=True", "stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True")
    content = content.replace("capture_output=True", "stdout=subprocess.PIPE, stderr=subprocess.PIPE")
    content = content.replace("text=True", "universal_newlines=True")
    return content

for file in FILES:
    print(f"Processing {file}...")
    # Strip hints
    subprocess.run(["/Users/xuco/Library/Python/3.9/bin/strip-hints", file, "--outfile", file], check=True)
    
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Remove future annotations
    content = re.sub(r'from __future__ import annotations\n', '', content)
    
    # Fix subprocess
    content = fix_subprocess(content)
    
    with open(file, "w", encoding="utf-8") as f:
        f.write(content)

# Install script
print("Processing install.sh...")
with open("install.sh", "r", encoding="utf-8") as f:
    content = f.read()
content = fix_subprocess(content)
# Python 3.6 inside install.sh might need type hint stripping too? It's embedded python!
content = re.sub(r'-> tuple\[.*?\]:', ':', content)
content = re.sub(r'-> str:', ':', content)
content = re.sub(r'-> int:', ':', content)
content = re.sub(r'-> bool:', ':', content)
content = re.sub(r'-> dict\[.*?\]:', ':', content)
content = re.sub(r'from __future__ import annotations\n', '', content)

with open("install.sh", "w", encoding="utf-8") as f:
    f.write(content)

print("Done!")

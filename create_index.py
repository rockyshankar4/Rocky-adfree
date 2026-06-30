import json
import os

# This creates a basic index file structure that Cloudstream expects
data = {
    "name": "CNCVerse Ad-Free",
    "description": "Ad-free extension list",
    "plugins": []
}

# Find all .cs3 files generated in the build folders
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.cs3'):
            # This is a simplified logic; usually, you'd extract metadata here
            data['plugins'].append({"name": file, "url": file})

with open('CNC.json', 'w') as f:
    json.dump(data, f, indent=4)
print("CNC.json created successfully.")

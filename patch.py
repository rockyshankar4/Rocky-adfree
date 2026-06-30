import os
import re

def patch_files():
    target_dir = '.' 
    patched_count = 0

    print("Scanning all directories for redirects and deprecated API calls...")

    for root, dirs, files in os.walk(target_dir):
        # Safely skip git and build folders without breaking the path logic
        if '.git' in root or '/build/' in root:
            continue

        for file in files:
            if file.endswith('.kt'):
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                original_content = content

                # 1. Safely neutralize omg10.com redirect
                if 'omg10.com' in content:
                    content = re.sub(r'(?:www\.)?omg10\.com', '127.0.0.1', content)

                # 2. Fix Cloudstream API deprecation (upgrading 'rating' to 'score')
                if 'rating' in content:
                    # Catch assignments like "rating =" or "rating="
                    content = re.sub(r'\brating\s*=', 'score =', content)
                    # Catch property accesses like "it.rating"
                    content = re.sub(r'\.rating\b', '.score', content)
                    # Catch named arguments like "rating:"
                    content = re.sub(r'\brating\s*:', 'score:', content)
                
                # If changes were made, write them back to the file
                if content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    patched_count += 1
                    print(f"✅ Patched file: {filepath}")

    print(f"Finished patching. Total files modified: {patched_count}")

if __name__ == '__main__':
    patch_files()

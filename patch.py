import os
import re

def patch_files():
    target_dir = '.' 
    patched_count = 0

    print("Scanning all directories for redirects and API patches...")

    for root, dirs, files in os.walk(target_dir):
        if '.git' in root or '/build/' in root:
            continue

        for file in files:
            if file.endswith('.kt'):
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                original_content = content

                # Strip the invisible BOM character if it exists to prevent syntax errors
                if content.startswith('\ufeff'):
                    content = content[1:]

                # 1. Safely neutralize omg10.com redirect
                if 'omg10.com' in content:
                    content = re.sub(r'(?:www\.)?omg10\.com', '127.0.0.1', content)

                # 2. Force Kotlin to ignore the deprecation error without breaking the file structure
                if 'rating' in content and 'DEPRECATION_ERROR' not in content:
                    content = '@file:Suppress("DEPRECATION", "DEPRECATION_ERROR")\n' + content
                
                if content != original_content:
                    # Write back as standard UTF-8 (Python automatically leaves out the BOM)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    patched_count += 1
                    print(f"✅ Patched file: {filepath}")

    print(f"Finished patching. Total files modified: {patched_count}")

if __name__ == '__main__':
    patch_files()

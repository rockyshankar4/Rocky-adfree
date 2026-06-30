import os
import re

def patch_files():
    target_dir = '.' 
    patched_count = 0

    print("Scanning all directories for redirects and deprecated API calls...")

    for root, dirs, files in os.walk(target_dir):
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
                    new_lines = []
                    for line in content.split('\n'):
                        # If the line contains a string, use targeted replacements to protect CSS selectors
                        if '"' in line or "'" in line:
                            # Matches: rating = 
                            line = re.sub(r'\brating\s*=', 'score =', line)
                            # Matches: rating:
                            line = re.sub(r'\brating\s*:', 'score:', line)
                            # Matches: object.rating or object?.rating
                            line = re.sub(r'([\w)\]]\s*\??\.)rating\b', r'\g<1>score', line)
                            # Matches: rating?, rating,, or rating)
                            line = re.sub(r'\brating(\s*[?,)])', r'score\1', line)
                            new_lines.append(line)
                        else:
                            # If no strings exist on the line, safely replace the word completely
                            new_lines.append(re.sub(r'\brating\b', 'score', line))
                    
                    content = '\n'.join(new_lines)
                
                if content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    patched_count += 1
                    print(f"✅ Patched file: {filepath}")

    print(f"Finished patching. Total files modified: {patched_count}")

if __name__ == '__main__':
    patch_files()

import os
import re

def patch_files():
    target_dir = 'src'
    patched_count = 0

    print("Scanning for redirects and deprecated API calls...")

    for root, _, files in os.walk(target_dir):
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
                    # Replaces instances like "rating = " with "score = "
                    content = re.sub(r'\brating\s*=', 'score =', content)
                    # Replaces instances like "it.rating" with "it.score"
                    content = re.sub(r'\.rating\b', '.score', content)
                
                # If changes were made, write them back to the file
                if content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    patched_count += 1
                    print(f"✅ Patched file: {filepath}")

    print(f"Finished patching. Total files modified: {patched_count}")

if __name__ == '__main__':
    patch_files()

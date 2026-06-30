import os
import re

def patch_redirects():
    target_dir = 'src'
    patched_count = 0

    print("Scanning for omg10.com redirects...")

    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.kt'):
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                if 'omg10.com' in content:
                    # Safely replace the domain with localhost to avoid breaking quotation syntax
                    new_content = re.sub(r'(?:www\.)?omg10\.com', '127.0.0.1', content)
                    
                    if content != new_content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        patched_count += 1
                        print(f"✅ Safely neutralized redirect in: {filepath}")

    print(f"Finished patching. Total files modified: {patched_count}")

if __name__ == '__main__':
    patch_redirects()

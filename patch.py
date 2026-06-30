import os
import re

def patch_redirects():
    # Target the directory containing the Kotlin source files
    target_dir = 'src'
    patched_count = 0

    print("Scanning for omg10.com redirects...")

    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.kt'):
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Check if the domain is in the file
                if 'omg10.com' in content:
                    # NOTE: Adjust the regex below based on exactly how the redirect is coded.
                    # This example replaces the target domain with an empty string or benign URL,
                    # or you can use regex to strip out the entire block.
                    # Here, we replace instances of the URL to short-circuit the redirect.
                    new_content = re.sub(r'https?://(?:www\.)?omg10\.com[^"\'\s]*', '""', content)
                    
                    if content != new_content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        patched_count += 1
                        print(f"✅ Patched redirect in: {filepath}")

    print(f"Finished patching. Total files modified: {patched_count}")

if __name__ == '__main__':
    patch_redirects()

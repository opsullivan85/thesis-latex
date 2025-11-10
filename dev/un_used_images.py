# find all unused images in the LaTeX project

import os
import glob
import re

# 1. Find all *.tex files in and below "../../"
root = os.path.join(os.path.dirname(__file__), "..")
tex_files = glob.glob(os.path.join(root, "**/*.tex"), recursive=True)

# 2. Find all images in "../../images"
image_files = [f for f in glob.glob(os.path.join(root, "images/**/*"), recursive=True) if os.path.isfile(f)]

# 3. Find all image references in latex
referenced = set()
for tex in tex_files:
    with open(tex, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        # Match \includegraphics with optional options
        matches = re.findall(r'\\includegraphics(?:\[.*?\])?\{([^}]+)\}', content, re.DOTALL)
        for match in matches:
            # Normalize: remove newlines, collapse whitespace to single space, strip
            clean_match = re.sub(r'\s+', ' ', match.replace('\n', '')).strip()
            referenced.add(clean_match)

# 4. See what isn't referenced
image_paths = set()
for img in image_files:
    rel_path = os.path.relpath(img, root)
    image_paths.add(rel_path)

print("All images found:")
for img in sorted(image_paths):
    print(img)

print("\nAll references found:")
for ref in sorted(referenced):
    print(ref)

unused = image_paths - referenced

print("\nUnused images:")
for u in sorted(unused):
    print(u)
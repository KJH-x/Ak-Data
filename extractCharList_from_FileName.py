import re

import pyperclip

# Find matches
matches = re.compile(r'(char_(\d+)_([^_]+))_\d+').findall(pyperclip.paste())

# Filter unique entries and prepare for numerical sorting
# Store as (int(num), full_string, original_num_string, label)
unique_sorted_prep = []
seen_full = set()

for full, num_str, label in matches:
    if full not in seen_full:
        seen_full.add(full)
        unique_sorted_prep.append((int(num_str), full, num_str, label))

# Sort numerically by the first element (int_num)
unique_sorted_prep.sort()

# Format the sorted results
results = [f"{full}\t{num}\t{label}" for _, full, num, label in unique_sorted_prep] # _ is the int value used for sorting

# Copy to clipboard
pyperclip.copy('\n'.join(results))
print("Processed and copied to clipboard.")
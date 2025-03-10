import json
import os
import re

import pandas as pd

csv_file_path = input("input (import) CSV file path:")
file_name = os.path.splitext(os.path.basename(csv_file_path))[0]
df = pd.read_csv(csv_file_path, dtype=str)

# Sort tags
empty_columns = [col for col in df.columns if df[col].isna().any() or (df[col] == "").any()]
duplicate_columns = [col for col in df.columns if df[col].duplicated().any()]


def is_cjk(char) -> bool:
    return bool(re.search(r'[\u4E00-\u9FFF\u3400-\u4DBF\u3040-\u30FF\uAC00-\uD7AF]', char))


def get_preview(col, max_len=30, max_preview=10):
    """Generate a flexible column preview with CJK-aware trimming."""
    unique_values = df[col].dropna().unique()[:max_preview]
    preview = ", ".join(map(str, unique_values))

    # Calculate true display length
    display_len = 0
    output = ""

    for char in preview:
        char_len = 2 if is_cjk(char) else 1
        if display_len + char_len > max_len:
            output += "..."
            break
        output += char
        display_len += char_len

    return output


# Create formatted list of columns
column_data = []
for i, col in enumerate(df.columns):
    preview_text = get_preview(col)
    col_display_name = f"{'[D]' if col in duplicate_columns else ''}{'[E]' if col in empty_columns else ''}{col}".strip()

    column_data.append((col_display_name, preview_text, col))

column_data.sort(key=lambda x: x[0], reverse=True)

# Display table
print("\nAvailable columns:")
print(f"{'No':>3}  {'Tag':^30} {'Tag Content Preview'}")
print("-" * 70)
for idx, data in enumerate(column_data):
    if "[D]" in data[0] or "[E]" in data[0]:
        print(f"{idx+1:>3}. {data[0]:>30} {data[1]}")
    else:
        print(f"{idx+1:>3}. {data[0]:<30} {data[1]}")

# User selects the first-level key
while True:
    try:
        choice = int(input("\nChoose a column number as the first-level key: ")) - 1
        if 0 <= choice < len(df.columns):
            first_level_key = column_data[choice][-1]
            break
        else:
            print("Invalid selection, try again.")
    except ValueError:
        print("Enter a valid number.")


# Convert to JSON
json_data = {}
for _, row in df.iterrows():
    key = str(row[first_level_key])
    if pd.isna(key) or key == "":
        continue

    # Remove keys with (NaN, "")
    filtered_row = {col: row[col] for col in df.columns if col !=
                    first_level_key and pd.notna(row[col]) and row[col] != ""}
    if filtered_row:
        json_data[key] = filtered_row


json_file_path = os.path.join(os.path.dirname(csv_file_path), f"{file_name}.{first_level_key}.json")


with open(json_file_path, "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=4, ensure_ascii=False)

print(f"\nJSON file saved as {json_file_path}")

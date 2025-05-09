import csv

input_path = 'data/complex-name-skill.csv'

# Read the CSV file
with open(input_path, newline='',encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)
    rows = list(reader)
    rows = [row for row in rows if any(cell.strip() for cell in row)]

# Sort by numeric value of second column, but keep the original strings (preserves leading zeros)
rows.sort(key=lambda row: int(row[1]if row[1].isdigit() else 0))

# Optional: write to a new CSV file
output_path = 'data/complex-name-skill.sorted.csv'
with open(output_path, 'w', newline='',encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows(rows)

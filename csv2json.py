import csv
import json


def csv_to_json(csv_file, json_file) -> None:
    with open(csv_file, mode='r', encoding='utf-8') as csvfp:
        reader = csv.DictReader(csvfp)
        result = []

        for row in reader:
            first_col = list(row.keys())[0]
            first_col_value = row[first_col]

            remaining_data = {key: value for key, value in row.items() if key != first_col}
            result.append({first_col_value: remaining_data})

        with open(json_file, mode='w', encoding='utf-8') as jsonfp:
            json.dump(result, jsonfp, indent=4, ensure_ascii=False)


if __name__=="__main__":
    csv_to_json(input("input csv path:"), input("input json path:"))

import csv
import json
import re
import urllib.parse
from typing import Any, Dict, List, Tuple

import requests
from bs4 import BeautifulSoup

# === === === === === === === === 干员基本信息 === === === === === === === ===


def save_operator_html(output_file: str) -> str:
    url = "https://prts.wiki/w/干员一览"
    encoded_url = urllib.parse.quote(url, safe=":/?=&")

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(encoded_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        filter_data = soup.find("div", {"id": "filter-data"})
        if filter_data:
            with open(output_file, "w", encoding="utf-8") as file:
                file.write(str(filter_data))
            print("√ ⭳ wiki_list.html")

            return str(filter_data)
        else:
            raise Exception("ERROR: No div with id='filter-data'")
    else:
        raise Exception(f"ERROR: Failed to retrieve the page. Status code: {response.status_code}")


def extract_data(html: str) -> Tuple[List[str], List[Any]]:
    soup = BeautifulSoup(html, 'html.parser')
    columns = [div for div in soup.find_all('div', recursive=False)]

    headers = [
        "data-zh", "data-profession", "data-rarity", "data-en", "data-ja", "data-id", "data-sex",
        "data-birth_place", "data-team", "data-logo", "data-race", "data-nation", "data-group"
        "data-hp", "data-atk", "data-def", "data-res",
        "data-re_deploy", "data-cost", "data-block", "data-interval",  "data-position",
        "data-tag", "data-obtain_method", "data-potential", "data-trust", "data-phy", "data-flex",
        "data-tolerance", "data-plan", "data-skill", "data-adapt", "data-sortid", "data-subprofession",
    ]

    data_list: List[Any] = []
    for col in columns:
        rows = col.find_all('div', recursive=False)
        for row in rows:
            data: Any = {header.removeprefix("data-"): row.get(header, '') for header in headers}
            data_list.append(data)

    return headers, data_list


def save_to_csv(headers: List[str], data_list: List[Any], output_file: str):
    with open(output_file, mode='w+', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=[header.removeprefix("data-") for header in headers])
        writer.writeheader()
        writer.writerows(data_list)


html_content = save_operator_html(r'data/wiki_list.html')
headers, data_list = extract_data(html_content)
save_to_csv(headers, data_list, r'data/wiki_list.csv')

print("√ wiki_list.csv")


# === === === === === === === === 技能组 === === === === === === === ===

def save_skill_json(output_file: str) -> str:
    url = "https://raw.githubusercontent.com/Arkfans/ArknightsName/refs/heads/main/data/skill.json"
    encoded_url = urllib.parse.quote(url, safe=":/?=&")

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(encoded_url, headers=headers)

    if response.status_code == 200:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(str(response.text))
        print("√ ⭳ skill.json")
        return str(response.text)
    else:
        raise Exception(f"ERROR: Failed to retrieve the page. Status code: {response.status_code}")


def save_skill_csv(jsoncontent: str, input_patch: str, output_file: str):
    data: Dict[str, Dict[str, str]] = json.loads(jsoncontent)
    all_tags = ["zh_CN", "ja_JP", "en_US"]

    pattern = re.compile(r"(skchr|skcom|sktok)_([^_]+)(?:_(.+))?")
    csv_data = [["name", "type", "object", "version"] + ["zh_CN", "ja_JP", "en_US"]]

    for name, attributes in data.items():
        match = pattern.match(name)
        if match:
            type_part, object_part, version_part = match.groups()
            version_part = version_part if version_part else "-"  # Default to "-"
        else:
            type_part, object_part, version_part = "-", "-", "-"

        row: List[str] = [name, type_part, object_part, version_part] + [attributes.get(tag, "-") for tag in all_tags]
        csv_data.append(row)

    with open(output_file, "w+", encoding="utf-8", newline="") as csvfp, \
            open(input_patch, "r", encoding="utf-8", newline="") as patchfp:
        writer = csv.writer(csvfp)
        writer.writerows(csv_data)
        print("√ ↺ skill.csv")

        csvfp.writelines(patchfp.readlines())
        print("√ ↺ skill.pathch.csv")


json_content = save_skill_json(r"data/skill.json")
save_skill_csv(json_content, r"data/skill.patch.csv", r"data/skill.csv")

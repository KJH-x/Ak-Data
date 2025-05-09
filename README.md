# Ak-Data

Data from arknights

## Usage

run `Update.py`
->

``` log
√ ⭳ wiki_list.html
√ wiki_list.csv
√ ⭳ skill.json
√ ↺ skill.csv
√ ↺ skill.pathch.csv (use patch)

-> updated (git tracked): skill.csv, wiki_list.csv
```

run `csv2md.py`
->

```log
-> updated (git tracked): wiki_list.md

```

resources update:
`头像：imgs\干员头像\Everything.regex.note.txt`
`立绘：imgs\干员立绘\Everything.regex.note.txt`

run extractCharList_from_FileName.py
copy xlsx col1, compare
paste patch, sorted

## src folder

| src name    | src path                                             |
| ----------- | ---------------------------------------------------- |
| chararts    | `./chararts/*`                                       |
| skinpack    | `./skinpack/*`                                       |
| char avatar | `./spritepack/ui_char_avatar_\d+/char_\d+_\S+_.+.png` |

## Major Data

[complex-name-skill](data/complex-name-skill.md)
[wiki_list](data/wiki_list.md)

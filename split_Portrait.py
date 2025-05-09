# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownMemberType=false
# pyright: reportOptionalIterable=false
# pyright: reportGeneralTypeIssues=false
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from PIL import Image
from tqdm import tqdm


def is_empty(image: Image.Image) -> bool:
    if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
        return all(pixel == 0 for pixel in image.getchannel("A") .getdata())
    return True


def process_file(file: str, progress_bar: tqdm) -> None:
    image = Image.open(file)
    # -> {"file", ".png"}
    file_base, ext = os.path.splitext(file)

    for index in config:
        # crop
        rect = config[index]
        cropped = image.crop((rect["x1"], rect["y1"], rect["x2"], rect["y2"]))

        if is_empty(cropped):
            continue

        if rect["rotate"]:
            cropped = cropped.rotate(rect["rotate"], expand=True)

        cropped.save(f"{file_base}.{index}{ext}")

    progress_bar.update(1)


if __name__ == "__main__":
    with open("config/180x360_from_1024x1024.json", mode='r', encoding='utf-8') as jsonfile:
        config = json.load(jsonfile)
    with open("config/path.txt", mode='r', encoding='utf-8') as pathfp:
        path = pathfp.read().splitlines()

    # # parallel processing

    with tqdm(total=len(path), desc="Processing files", unit="file") as progress_bar:
        with ThreadPoolExecutor(max_workers=16) as executor:
            # submit mission
            futures = [executor.submit(process_file, file, progress_bar) for file in path]

            for future in as_completed(futures):
                future.result()

    # Single processing
    # with tqdm(total=len(path), desc="Processing files", unit="file") as progress_bar:
    #     for file in path:
    #         process_file(file, progress_bar)

    print("All files processed.")
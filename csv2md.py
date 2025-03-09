import pandas as pd


def csv_to_markdown(file_path: str) -> str:
    df = pd.read_csv(file_path)
    return df.to_markdown(index=False)


if __name__=="__main__":
    markdown_output = csv_to_markdown(input("input csv path:")).replace("nan", "-")
    with open(input("input markdown path:"), mode='w+', encoding='utf-8')as mdfp:
        mdfp.write(markdown_output)
        # MD047/single-trailing-newline: Files should end with a single newline character
        mdfp.writelines("\n")

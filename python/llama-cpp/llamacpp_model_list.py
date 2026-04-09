import os
import json
from pathlib import Path
import re

# -hfで呼び出すDL済み　hoge/fuga-gguf-128k-Q4_K　などのモデル名リストを作る
# コピペして適当なtxtに保存
#
# %USERPROFILE%\.cache\huggingface内を再帰的に全検索して
# gemma-3-1b-it-Q4_K_M.ggufなど拡張子.gguf（シムリンク）を見つけたら
# 3つ上のmodels--ggml-org--gemma-3-1b-it-GGUFフォルダ名を取得し
# ggml-org/gemma-3-1b-it-GGUF　という呼び出しリストを作る


base = os.getenv("USERPROFILE")  # %USERPROFILE%と同じ
directory = os.path.join(
    base, ".cache\huggingface"
)  # %USERPROFILE%\.cache\huggingfaceディレクトリ


def find_json_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".gguf"):
                yield os.path.join(root, file)


def main():
    print(rf"C:\Users\アカウント名\.cache\huggingface内を探し、")
    print(f"-hfオプションでDLされたGGUFファイルを探して")
    print(rf"foo/bar_GGUF:Q8_0")
    print(rf"hoge/fuga_GGUF:Q4_0")
    print("などのDL済みモデルリストを出力します。\n")

    answer = input(rf"実行して良いですか？( yes か no を入力): ").strip()
    print(rf"{answer}が入力されました")
    if re.match(r"^(yes|y|ｙ|Ｙ|Ｙｅｓ|ＹＥＳ)$", answer, re.IGNORECASE):
        list = []
        for json_file in find_json_files(directory):
            print(f"ファイル: {json_file}")
            my_dir = Path(json_file).parent.parent.parent.name
            d = my_dir.split("--")

            base_name = os.path.splitext(json_file)[0]
            parts = base_name.split(".")
            quantize = parts[-1] if len(parts) > 1 else ""
            if re.match(r"^([A-Z]+_)?(I?Q)\d+[A-Z0-9_]*$", quantize, re.IGNORECASE):
                result = f"{d[1]}/{d[2]}:{quantize}"
            else:
                result = f"{d[1]}/{d[2]}"
            list.append(result)

        print("\n################################")
        print("#     以下をコピーして使用     #")
        print("################################\n")
        for i in list:
            print(i)
    input("\nEnterを押すと終了します...")


if __name__ == "__main__":
    main()

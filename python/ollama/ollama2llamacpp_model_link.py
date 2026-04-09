import os
import json
from pathlib import Path

directory = r"E:\lib\.ollama\manifests"  # .ollamaのmanifestsディレクトリ
blobs_dir = r"E:\lib\.ollama\blobs"  # .ollamaのblobsディレクトリ　中にsha256-(GGUF本体)が詰まってる
save_dir = r"G:\lib\llama-cpp\models"  # シンボリックリンクの保存先

# https://www.reddit.com/r/LocalLLaMA/comments/1hdbfgn/ollama_sharing_a_single_copy_of_model_files_with/?tl=ja
# のWin版Pythonバージョン(OllamaでDLしたモデルをllama-cppで共有したい人用)
# mklink link.txt Souce.txt でシンボリックリンクのコマンドを作るだけなので、
# バッチファイルに保存するか直接コピーして、管理者権限のコマンドプロンプトで実行すると
# シンボリックリンクが出来る


def find_json_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            # ファイルは拡張子がないので.jsonが付いているか確認してはいけない
            yield os.path.join(root, file)


def read_json_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def main():
    print("OllamaでDLしたモデルをllama-cppで共有したい人用のPythonです\n")
    # location = input(
    #     "OllamaのSetting＞Model locationで指定したパスを、フルパスで入力してください: "
    # ).strip()

    list = []
    for json_file in find_json_files(directory):
        print(f"ファイル: {json_file}")
        my_file = Path(json_file).name
        my_dir = Path(json_file).parent.name
        gguf = f"{my_dir}_{my_file}.gguf"
        gguf_full_path = os.path.join(save_dir, gguf)
        content = read_json_file(json_file)
        for layer in content.get("layers", []):
            if layer["mediaType"].endswith(".model"):
                souce_file = layer["digest"].replace(":", "-")
                souce_full_path = os.path.join(blobs_dir, souce_file)
                l = f'mklink "{gguf_full_path}" "{souce_full_path}"'
                list.append(l)

    print("\n################################")
    print("#     以下をコピーして使用     #")
    print("################################\n")
    for i in list:
        print(i)


if __name__ == "__main__":
    main()

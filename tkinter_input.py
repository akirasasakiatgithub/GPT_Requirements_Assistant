import re
import sys
import tkinter as tk
from tkinter import messagebox
# import nest_asyncio
# nest_asyncio.apply()
# print(sys.executable)
# print(sys.version)


#tkinterバージョン

def is_japanese(text):
    
    """
    文字列が日本語を含んでいるか確認する関数。
    日本語（ひらがな、カタカナ、漢字）の判定を行う。
    """
    return bool(re.search(r'[\u3040-\u30FF\u4E00-\u9FFF]', text))

def split_into_sentences(text):

    """
    日本語の文章を句点「。」、改行、感嘆符、疑問符で分割してリストとして辞書に格納する。
    空行も文末として扱う。
    """
    # 文を句点、感嘆符、疑問符、改行で分割、リストに格納
    sentences = re.split(r'[。！？…\n]', text)
    # 空白文字をトリムし、空の要素を除去し、リストを辞書に格納
    sentences_dict = {}
    sentences_dict["definition"] = [sentence.strip() for sentence in sentences if sentence.strip()] 

    return sentences_dict

def process_multiline_input():
    """
    テキストウィジェットから入力を受け取り、処理する関数。
    """
    user_input = text_widget.get("1.0", tk.END).strip()  # テキストウィジェットの内容を取得

    # 日本語が含まれているか確認
    if not is_japanese(user_input):
        messagebox.showerror("エラー", "日本語が含まれていません。")
        return

    # 文ごとに分割してリストを作成
    sentences = split_into_sentences(user_input)
    messagebox.showinfo("結果", f"分割された文のリスト:\n{sentences}")
    

# Tkinter GUIの構築
root = tk.Tk()
root.title("日本語文字列処理ツール")
root.geometry("500x400")

# 説明ラベル
label = tk.Label(root, text="複数行の日本語文字列を入力してください:")
label.pack(pady=10)

# テキストウィジェット（複数行の入力用）
text_widget = tk.Text(root, height=15, width=60)
text_widget.pack(pady=10)

# 実行ボタン
process_button = tk.Button(root, text="処理する", command=process_multiline_input)
process_button.pack(pady=10)

# メインループ
root.mainloop()

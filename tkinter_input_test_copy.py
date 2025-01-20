import re
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import os

# 設定ファイルパス
SETTINGS_FILE = "settings.json"

def load_settings():
    """設定を読み込む関数"""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

def save_settings(settings):
    """設定を保存する関数"""
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, ensure_ascii=False, indent=4)

def remove_settings(SETTINGS_FILE):
    # ファイルが存在するか確認して削除
    if os.path.exists(SETTINGS_FILE):
        try:
            os.remove(SETTINGS_FILE)
            print(f"{SETTINGS_FILE} を削除しました。")
        except Exception as e:
            print(f"ファイルを削除できませんでした: {e}")
    else:
        print(f"{SETTINGS_FILE} が見つかりません。")

def is_japanese(text):
    """
    文字列が日本語を含んでいるか確認する関数。
    """
    return bool(re.search(r'[\u3040-\u30FF\u4E00-\u9FFF]', text))

def split_into_sentences(text):
    """
    日本語の文章を分割する関数。
    """
    sentences = re.split(r'[。！？…\n]', text)
    sentences_dict = {}
    sentences_dict["definition"] = [sentence.strip() for sentence in sentences if sentence.strip()]
    return sentences_dict

def show_output_message(title, message, message_type="info"):
    """
    出力を表示するための汎用メッセージボックス。
    """

    # print(message)
    if message_type == "info":
        msbox = tk.Toplevel()
        msbox.title(title)
        msbox.geometry("400x170")

        label = tk.Label(msbox, text=message, justify="left")
        label.pack(pady=20)

        button = tk.Button(msbox, text="OK", command=msbox.destroy)
        button.pack(pady=10)

        msbox.transient(root)
        msbox.grab_set()
        msbox.wait_window()

    elif message_type =="result" or message_type == "origin":
        msbox = tk.Toplevel()
        msbox.title(title)
        msbox.geometry("400x600")

        label = tk.Label(msbox, text=message, wraplength=250, justify="left")
        label.pack(pady=20)

        button = tk.Button(msbox, text="OK", command=msbox.destroy)
        button.pack(pady=10)

        msbox.transient(root)
        msbox.grab_set()
        msbox.wait_window()

    elif message_type == "error":
        messagebox.showerror(title, message)
    

def show_messagebox_with_skip(title, message, key):
    """
    再表示させないことが可能なメッセージボックスを表示する関数（オリジナルなので destroy や wait_window 等が必要）
    """
    settings = load_settings()

    # jsonの指定keyの表示設定がTrueなら表示しない。第二引数の False はデフォルト値の設定
    if settings.get(key, False):
        return  

    # チェックボックスがオンならTrue（以降スキップ）をjsonに保存して、メッセージを閉じる
    def on_close():
        if skip_var.get(): # チェックボックスがオンなら
            settings[key] = True
            save_settings(settings)
        msbox.destroy()

    # keyに合わせてサブウィンドウ作成
    if key == "skip_notice":
        msbox = tk.Toplevel()
        msbox.title(title)
        msbox.geometry("350x250")

    elif key == "new_definition":
        msbox = tk.Toplevel()
        msbox.title(title)
        msbox.geometry("350x250")

    elif key == "input_definition":
        msbox = tk.Toplevel()
        msbox.title(title)
        msbox.geometry("350x600")

    # 引数のmessageをラベルとして追加
    label = tk.Label(msbox, text=message, wraplength=300, justify="left")
    label.pack(pady=10)

    # チェックボックス
    skip_var = tk.BooleanVar() #True（オン）または False（オフ）として状態管理
    skip_checkbox = tk.Checkbutton(msbox, text="次回以降再表示しない", variable=skip_var)
    skip_checkbox.pack(pady=10)

    button = tk.Button(msbox, text="OK", command=on_close)
    button.pack(pady=10)

    msbox.transient(root)  # メインウィンドウの前に表示
    msbox.grab_set()      # フォーカスを固定
    root.wait_window(msbox) # このメッセージボックスが閉じられるまでrootのみ処理を停止
    # msbox.protocol("WM_DELETE_WINDOW", on_close)  # サブウィンドウの「閉じる」ボタンを制御

def process_multiline_input(text_widget, skip_var, has_arg, callback=None):
    """
    エントリorテキストウィジェットから入力を受け取り、処理する関数。returnで返せないのでcallbackで保存
    """
    # スキップチェックボックスがオンの場合
    if skip_var.get():
        show_messagebox_with_skip("確認", "入力がスキップされました。", "skip_notice")
        root.destroy()
        return

    # 入力を取得
    user_input = text_widget.get("1.0", tk.END).strip()

    # 入力が空の場合
    if not user_input:
        show_output_message("エラー", "入力が空です。再入力してください。", "error")
        return  # 再入力を促す

    # 日本語が含まれていない場合
    if not is_japanese(user_input):
        show_output_message("エラー", "日本語が含まれていません。再入力してください。", "error")
        text_widget.delete("1.0", tk.END)
        return  # 再入力を促す

    # 正常な入力の場合
    sentences = split_into_sentences(user_input)
    if has_arg: # ＝初回以降
        show_messagebox_with_skip("明確化された要求定義", "\n".join(sentences["definition"]), "input_definition")
    else:
        show_output_message("入力された要求定義", "\n".join(sentences["definition"]), "origin")

    # コールバックで結果を渡す
    if callback:
        callback(sentences)

    # 入力完了後にウィンドウを閉じる
    root.destroy()

def create_gui(callback, argments=None):
    """
    GUIを構築し、Tkinterアプリケーションを開始する関数。
    """
    global root
    root = tk.Tk()
    root.title("Clarify")
    root.geometry("1000x600")


    # スキップチェックボックスの値の初期化
    skip_var = tk.BooleanVar()  # チェックボックスの状態を管理する変数
    
    
    if argments:
        has_arg = True
        show_messagebox_with_skip(
            "新たな定義の入力",
            "曖昧な定義を、より明確で具体的なものにしてください。",
            "new_definition"
        )
        text = (f"\n「{argments['sentence']}」\n\nという要求の\n\n”{argments['amb_str']}”\n\nという表現は\n\n"
                f"{argments['reason']}\n\nという理由で曖昧です。\n{argments['amb_str']}の内容をより明確、具体的に示してください。\n\n"
                f"この場合の一先ず明確な回答というのは、例えば「{argments['example'][0]}」、「{argments['example'][1]}」、「{argments['example'][2]}」のようなものです。"
                 "※明確にしない場合は「この入力をスキップする」にチェックを入れてください。")
        
    else:
        show_output_message(
            "要求定義の入力",
            "複数行の要求定義を入力してください。\n一つの要求を一つの文で入力してください。"
        )
        text = "複数行の要求定義を入力してください。\n一つの要求を一つの文で入力してください。\nタイトル、見出しの前にはその階層に従い # ~ #### + 半角スペースをつけて下さい。\n（例：# タイトル、　## 大見出し、　#### 小見出し）"
        
    text_widget = tk.Text(root, height=30, width=120)
    text_widget.pack(pady=10)

    if argments:
        skip_checkbox = tk.Checkbutton(root, text="この入力をスキップする", variable=skip_var)
        skip_checkbox.pack(pady=10)



    

    # 説明ラベル
    label = tk.Label(root, text=text, justify="left")
    label.pack(pady=10)

    # スキップチェックボックス
    
    

    # 実行ボタン
    process_button = tk.Button(
        root,
        text="OK",
        command=lambda: process_multiline_input(text_widget, skip_var, has_arg, callback)
    )
    process_button.pack(pady=10)

    root.mainloop()

def input_requirement(argments=None):
    # 結果を保持するリスト（外部で受け取れるようにする）
    result_container = None

    def handle_sentences(sentences_dict):
        """
        コールバック関数: sentences_dictをresult_containerに保存。
        """
        nonlocal result_container
        result_container = sentences_dict

    # Tkinterアプリケーションを実行
    create_gui(handle_sentences, argments)

    # Tkinter終了後に結果を取得
    return result_container

if __name__ == "__main__":
    final_sentences = input_requirement()
    # print("mainから取得された文リスト:", final_sentences)

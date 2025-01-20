import re

def is_japanese(text):
    """
    文字列が日本語を含んでいるか確認する関数。
    日本語（ひらがな、カタカナ、漢字）の判定を行う。
    """
    return bool(re.search(r'[\u3040-\u30FF\u4E00-\u9FFF]', text))

def split_into_sentences(text):
    """
    日本語の文章を句点「。」や改行で分割してリストに格納する。
    """
    # 文を句点「。」または改行で分割
    sentences = re.split(r'[。！？]', text)
    # 空白文字をトリムし、空の要素を除去
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return sentences

def process_input():
    """
    複数行の日本語文字列を受け取り、日本語か確認し、文ごとにリストに格納する。
    """
    print("複数行の要件定義を入力してください（終了後Enterを押してください）:")
    # 一度に複数行の文字列を受け取る
    user_input = input(">>> ")

    # 日本語が含まれているか確認
    if not is_japanese(user_input):
        print("日本語が含まれていません。")
        return []

    # 文ごとに分割してリストに格納
    return split_into_sentences(user_input)

# 実行例
if __name__ == "__main__":
    lines = process_input()
    if lines:
        print("以下の文の曖昧さを確認します。:")
        print(lines)
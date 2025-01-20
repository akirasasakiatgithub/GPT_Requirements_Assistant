import re
import sys
# import ipdb


def input_requirement(argments=None):

    def is_japanese(text):
        """
        文字列が日本語を含んでいるか確認する関数。
        日本語（ひらがな、カタカナ、漢字）の判定を行う。
        """
        return bool(re.search(r'[\u3040-\u30FF\u4E00-\u9FFF]', text))
    
    def split_into_sentences(text):
        """
        日本語の文章を句点「。」、改行、感嘆符、疑問符で分割してリストに格納する。
        空行も文末として扱う。
        """
        # 文を句点、感嘆符、疑問符、改行で分割
        sentences = re.split(r'[。！？…\n]', text)
        # 空白文字をトリムし、空の要素を除去
        sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
        return sentences

    def process_multiline_input(argments=None):
        """
        複数行の日本語文字列を受け取り、日本語か確認し、文ごとにリストに格納する。
        """

        if argments:
            print(f"{argments[2]}は{argments[3]}という理由で曖昧です。\n（○○に入る言葉を入力して下さい。明確にしない場合は「 （半角スペース）」を入力してください。（Enter → Ctrl+Z → Enterで終了））より具体的には{argments[2]}とは○○という意味です。:")
        else:
            print("複数行の要件定義を入力してください。一つの要件を一つの文で入力してください。（Enter → Ctrl+Z → Enterで終了）:")

        while True:
            # 標準入力から複数行の文字列を読み取る
            user_input = sys.stdin.read()

            #ipdb.set_trace()

            # Ctrl+ZのASCIIコード '\x1a' を取り除く
            user_input = user_input.replace('\x1a', '').strip()

            # 日本語が含まれているか確認
            if user_input == '-':
                return "ごめんね"
            elif not is_japanese(user_input):
                print("日本語が含まれていません。再入力してください。")
                continue
            else:
                # 文ごとに分割してリストに格納
                return split_into_sentences(user_input)

    #ipdb.set_trace()
    input_result = process_multiline_input(argments)
    return input_result
  
        
# 使用例
if __name__ == '__main__':
    input_result = input_requirement()
    print(input_result)



import os
import openai
import ast
from tkinter import messagebox

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("API key not found. Set the OPENAI_API_KEY environment variable.")

# OpenAI APIキーを設定
openai.api_key = api_key

def extract_amb(input_dict):
    requirement = input_dict["definition"]
    prompt = f"""システム設計のリスト形式の要求定義「{requirement}」について、要求定義工程において問題となる曖昧さを厳密に分析しその部分を抽出してください。
要求定義の解説：
このリスト形式の要求定義は以下の規則に従って書かれています。
1. タイトル、見出し、各要求定義文ごとにリストの要素として格納されています。
2. タイトル、見出しにはマークダウン形式に従い「# ~ ####」が初めに付けられ、各要求とは区別されています。
3. 数字だけの要素は付加情報を示すものです。

以下の厳密な指示に従ってください：
1. 曖昧さの判定は各要求定義文についてのみ行い、タイトル、見出しについては行わないでください。
2. 曖昧な部分を特定する際は、各要求定義文の中で不明確または多義的な部分を探してください。
3. 各曖昧な部分について、以下の辞書を要素とするリスト形式で正確に報告してください。：
   - pos_in_doc：リストrequirementのその曖昧な部分の抜き出し元の要素のindex番号（半角数字）
   - pos_in_sen：先頭を０番目とした時のその曖昧な部分の文の先頭から数えた開始位置（半角数字）
   - sentence:リストrequirementのその曖昧さを含む要素全体
   - amb_str：その曖昧な部分の正確な文字列
   - reason：その曖昧な部分が曖昧であると言える理由を示した文字列
4. 曖昧さの指摘は要求定義工程のアウトプットとして適切な内容・レベルにしてください。
出力形式の例：
[
    {{ 'pos_in_doc': リストrequirementのindex番号（半角数字）,  'pos_in_sen': 先頭を０番目とした時のその曖昧な部分の文の先頭から数えた開始位置（半角数字）, 'sentence':リストrequirementのその曖昧さを含む要素全体, 'amb_str': '曖昧な部分の正確な文字列', 'reason': '曖昧な部分が曖昧であると言える理由を示した文字列' }},
    {{ 'pos_in_doc': リストrequirementのindex番号（半角数字）,  'pos_in_sen': 先頭を０番目とした時のその曖昧な部分の文の先頭から数えた開始位置（半角数字）, 'sentence':リストrequirementのその曖昧さを含む要素全体, 'amb_str': '曖昧な部分の正確な文字列', 'reason': '曖昧な部分が曖昧であると言える理由を示した文字列' }}
]

重要な注意点：
- 厳密に形式を守ってください。
- 曖昧な部分がない場合は、空のリスト [] を返してください。
- Pythonのリスト形式、辞書形式を正確に使用してください。
- 追加の説明や解説は不要です。
- 曖昧な部分が曖昧であると言える理由を示した文字列の語尾は「～だから」という形で統一してください。
- 出力は、上記の形式のPythonの辞書のリストのみにしてください。"""

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert in identifying and precisely formatting ambiguities in system design requirements."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=5000,
        temperature=0.2  # ランダムさを抑える設定
    )

    result = response.choices[0].message.content

    # 追加の検証と変換
    try:
        # 不要な文字を除去し、リテラル評価を試みる
        clean_result = result.strip('```python\n```')
        amb_dicts = ast.literal_eval(clean_result)
        print("抽出された曖昧さ:\n", amb_dicts)
        return amb_dicts
    except (SyntaxError, ValueError) as e:
        message = (f"結果のパースに失敗しました。処理を中止します。生のレスポンス:\n{result}")
        messagebox.showerror("エラー", message)
        raise ValueError("APIからのレスポンスが不正な形式です。処理を中断します。") from e

# 出力:リスト内の曖昧さ辞書
if __name__ == '__main__':
    amb_list = extract_amb(input_result)





def extract_amb_sub(input_dict):
    requirement = input_dict["difinition"]

    prompt = f"""以下のシステム設計のリスト形式の要件定義「{requirement}」において、要件定義として問題となる曖昧さを検出し、考えられる問題点を抽出してください。
    ただし、あまりにも些細な曖昧さや、文脈的に明らかなものは許容対象とします。また、ユーザーが一般に理解しやすいレベルでの曖昧さを対象としてください。
要件定義の解説：
- このリストの要件定義は各要件文ごとに要素として整理されています。
- タイトルや見出しには「・（中黒）」が先頭についており、要件と区別されています。

以下の指示に従ってください：
1. 各要件文において明らかに解釈が分かれる可能性のある部分を特定してください。
2. 各曖昧な部分について、以下のリスト形式で報告してください。：
   - 文章の一連の中でその曖昧な部分を含む文の番号（0から始まる数値）
   - その曖昧な部分の文内での開始位置（0から始まる数値）
   - 曖昧な部分の文字列
   - 曖昧であると言える理由を示した文字列

出力形式の例：
[
    [0, 10, '曖昧な表現', 'その曖昧な表現が曖昧である理由'],
    [1, 5, '別の曖昧な表現', 'その別の曖昧な表現が曖昧である理由']
]

重要な注意点：
- 厳密なPythonのリスト形式での出力を守ってください。
- 曖昧さがない場合は、空のリスト []を返してください。
- 追加の説明は必要ありません。
- 曖昧であると言える理由を示した文字列の語尾は「～だから」という形で統一してください。

出力は、上記の形式のPythonリストのみにしてください。"""

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert in analyzing and identifying ambiguity in system design requirements."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=1.2  # 応答のノイズを増やして柔軟性を持たせる
    )

    result = response.choices[0].message.content

    # 追加の検証と変換
    try:
        clean_result = result.strip('```python\n```')
        amb_dict = ast.literal_eval(clean_result)
        print("抽出された曖昧さ:\n", amb_dict)
        return amb_dict
    except (SyntaxError, ValueError):
        print("結果のパースに失敗しました。生のレスポンス:")
        print(result)
        return []

# 出力:ネストされた曖昧さリスト
if __name__ == '__main__':
    amb_list = extract_amb_sub(["要件1の説明", "要件2の説明", "要件3の説明"])



def reconstruct_requirements(input_dict, lang_trans_list):

    if not lang_trans_list:
        result = """申し訳ありませんが、具体的な要求定義や曖昧さの解説が提供されていないため、修正を行うことができません。具体的な要求定義と曖昧さの解説を提供していた
だければ、それをもとに明確な要求定義を作成いたします。"""

    else:
        print("\n\n\n\n\n")

        letter_body = "\n".join(input_dict["definition"])
        lang_trans_doc = "\n".join(lang_trans_list)

        prompt = f"""## 修正対象: 曖昧な表現を含んだ要求定義

    以下の要求定義には曖昧な表現が含まれています。曖昧さの解説と共に記載しますので、これをもとに **具体的で明確な要求定義** に再構成して出力してください。
    \n## 曖昧な表現を含んだ要求定義\n{letter_body}\n{print(f"letter_body: {letter_body}")}

    \n## 曖昧さの解説\n{lang_trans_doc}\n{print(f"lang_trans_doc: {lang_trans_doc}")}

    
    \n## 重要な注意点：
    -厳密に以下の指示に従ってください。
    -**具体的で明確な要求定義**は曖昧な表現を含んだ要求定義のうち、曖昧さの解説の対象になっている部分だけを、そこで提示された具体的で明確な説明に置き換える形で作成してください。
    -曖昧な部分を含んだ要求定義の中で、曖昧さの解説に載っていない部分は曖昧な表現を残したままであっても、曖昧な部分を含んだ要求定義をそのままの形で残して下さい。
    -**具体的で明確な要求定義**には曖昧な部分を含んだ要求定義の見出しも対応する場所に再現して下さい。
    -余計な情報は付加せず、与えられた情報だけを使って出力してください。"""
        
        response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a competent assistant who adheres to the prompts."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=5000,
        temperature=0.2  # ランダムさを抑える設定
        )

        result = response.choices[0].message.content

    return result
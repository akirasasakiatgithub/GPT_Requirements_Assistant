import os
import openai
import ast

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("API key not found. Set the OPENAI_API_KEY environment variable.")

# OpenAI APIキーを設定
openai.api_key = api_key

# 時間があれば、元の文を示す仕様に変える（○○の××は△△という理由で曖昧です。）
def extract_amb(requirement):
    prompt = f"""システム設計のリスト形式の要件定義「{requirement}」において、要件定義において問題となる曖昧さを厳密に分析しその部分を抽出してください。
要件定義の解説：
このリスト形式の要件定義は以下の規則に従って書かれています。
1. タイトル、見出し、各要件文ごとにリストの要素として格納されています。
2. タイトル、見出しには「・（中黒）」が初めに付けられ、各要件とは区別されています。
3. 数字だけの要素は付加情報を示すものです。

以下の厳密な指示に従ってください：
1. 曖昧さの判定は各要件文についてのみ行い、タイトル、見出しについては行わないでください。
2. 曖昧な部分を特定する際は、各要件文の中で不明確または多義的な部分を探してください。
3. 各曖昧な部分について、以下のリスト形式で正確に報告してください：
   - リストの添え字０番目：先頭を０番目とした時のその曖昧な部分を含む文を文章の初めから数えた時の番号（半角数字）
   - リストの添え字１番目：先頭を０番目とした時のその曖昧な部分の文の先頭から数えた開始位置（半角数字）
   - リストの添え字２番目：曖昧な部分の正確な文字列
   - リストの添え字３番目：曖昧な部分が曖昧であると言える理由を示した文字列
4. 付加情報を示す数字だけの要素は、無視して文字列の要素だけを対象にしてください。

出力形式の例：
[
    [先頭を０番目とした時のその曖昧な部分を含む文を文章の初めから数えた時の番号（半角数字）, 先頭を０番目とした時のその曖昧な部分の文の先頭から数えた開始位置（半角数字）, '曖昧な部分の正確な文字列', '曖昧な部分が曖昧であると言える理由を示した文字列'],
    [先頭を０番目とした時のその曖昧な部分を含む文を文章の初めから数えた時の番号（半角数字）, 先頭を０番目とした時のその曖昧な部分の文の先頭から数えた開始位置（半角数字）, '曖昧な部分の正確な文字列', '曖昧な部分が曖昧であると言える理由を示した文字列']
]

重要な注意点：
- 厳密に形式を守ってください
- 曖昧な部分がない場合は、空のリスト []を返してください
- Pythonのリスト形式を正確に使用してください
- 追加の説明や解説は不要です
- 曖昧な部分が曖昧であると言える理由を示した文字列の語尾は「～だから」という形で統一してください。

出力は、上記の形式のPythonのリストのみにしてください。"""

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert in identifying and precisely formatting ambiguities in system design requirements."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.2  # ランダムさを抑える設定
    )

    result = response.choices[0].message.content

    # 追加の検証と変換
    try:
        # 不要な文字を除去し、リテラル評価を試みる
        clean_result = result.strip('```python\n```')
        ambiguities = ast.literal_eval(clean_result)
        print("抽出された曖昧さ:\n", ambiguities)
        return ambiguities
    except (SyntaxError, ValueError) as e:
        print("結果のパースに失敗しました。生のレスポンス:")
        print(result)
        raise ValueError("APIからのレスポンスが不正な形式です。処理を中断します。") from e

# 出力:ネストされた曖昧さリスト
if __name__ == '__main__':
    amb_list = extract_amb(input_result)





def extract_amb_sub(requirement=list):
    prompt = f"""以下のシステム設計のリスト形式の要件定義「{requirement}」において、要件定義として問題となる曖昧さを検出し、考えられる問題点を抽出してください。ただし、あまりにも些細な曖昧さや、文脈的に明らかなものは許容対象とします。また、ユーザーが一般に理解しやすいレベルでの曖昧さを対象としてください。
要件定義の解説：
- このリストの要件定義は各要件文ごとに要素として整理されています。
- タイトルや見出しには「・（中黒）」が先頭についており、要件と区別されています。

以下の指示に従ってください：
1. 各要件文において明らかに解釈が分かれる可能性のある部分を特定してください。
2. 各曖昧な部分について、以下のリスト形式で報告してください：
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
        ambiguities = ast.literal_eval(clean_result)
        print("抽出された曖昧さ:\n", ambiguities)
        return ambiguities
    except (SyntaxError, ValueError):
        print("結果のパースに失敗しました。生のレスポンス:")
        print(result)
        return []

# 出力:ネストされた曖昧さリスト
if __name__ == '__main__':
    amb_list = extract_amb_sub(["要件1の説明", "要件2の説明", "要件3の説明"])



def reconstruct_requirements(input_result, lang_trans_list):

    letter_body = "\n".join(input_result)
    lang_trans_doc = "\n".join(lang_trans_list)

    prompt = f"""## 修正対象: 曖昧な要件定義と解説

以下の要件定義には曖昧な表現が含まれています。曖昧さの解説と共に記載しますので、これをもとに **具体的で明確な要件定義** に再構成して出力してください。
\n## 曖昧な表現を含んだ要件定義\n{letter_body}\n

\n## 曖昧さの解説\n{lang_trans_doc}\n

\n## 期待する出力形式\n

-余計な情報は付加せず、与えられた情報だけを使って出力してください。"""
    
    response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are the expert in defining system requirements. You are responsible for modifying ambiguous requirement definitions to be clear and specific."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=1000,
    temperature=0.2  # ランダムさを抑える設定
    )

    result = response.choices[0].message.content

    return result
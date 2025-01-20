import openai



def extract_amb(requirement):
    prompt = f"""{requirement}の中にシステム設計の要件定義において曖昧と判断される部分はありますか？例に示すように、ネスト状に文ごとの曖昧な部分を格納し、変数ambiguitiesに格納してください。
例：
[
    ['１つ目の曖昧さを含む文の１つ目の曖昧な部分', '１つ目の曖昧さを含む文の２つ目の曖昧な部分', '１つ目の曖昧さを含む文の３つ目の曖昧な部分'],
    ['２つ目の曖昧さを含む文の１つ目の曖昧な部分', '２つ目の曖昧さを含む文の２つ目の曖昧な部分'],
    ['１つ目の曖昧さを含む文の１つ目の曖昧な部分', '１つ目の曖昧さを含む文の２つ目の曖昧な部分', '１つ目の曖昧さを含む文の３つ目の曖昧な部分'] 
]"""

    response = openai.Completion.create(
    engine="gpt-4-turbo",
    prompt=prompt,
    max_tokens=1000,
    temperature=0.6,
    n=1,
    stop=None,
)

    amb_def = response['choices'][0]['text']
    return amb_def
import sys
#import asyncio  # 非同期処理用
import ipdb

from input_requirement import input_requirement as inp
from use_openai_api import extract_amb as exam



input_result = inp()

amb_list = exam(input_result)

def create_question(amb_list):
    amb_mid_def = []
    amb_comp_def = []

    for index, amb_part in enumerate(amb_list):

        # 回答入力(リスト形式)
        # 初回は曖昧な文のリストが返るのに対して、今回はユーザーの回答が返る
        input = inp(amb_part)

        # 曖昧さ定義をパスした時の処理
        if not input:
            amb_list.remove(amb_list[index])
            continue

        # 一度実行したリストを読まない印をつける。多分必要ない。
        # 必要なら後でamb_partのリストを必要な形に修正
        # amb_part.append(True)

        # 回答を曖昧さ（質問）に紐づけ
        # 多分いらない
        input.append(index)
        # 曖昧さへの回答をその為のリストへ加える
        # 回答が複数行（複数要素のリストかどうかで処理を分ける）
        if len(input) > 2:
            [amb_mid_def.append(input[i]) for i in range(len(input)) if input[i] != input[-1]]
        else:
            amb_mid_def.append(input)

        # 曖昧さ検出（ネストされたリスト形式）
        new_amb_list = exam(input)

        if new_amb_list:
            # amb_listに挿入する新たなリストにどの回答に紐づけるかの情報を付与
            # 回答のIDを表現するため、新たな曖昧さが指す曖昧さのID（index）を要素として追加
            # （文内IDのはnew_amb_partに含まれているはずなので追加のコードは記述していない）
            [new_amb_part.append(index) for new_amb_part in new_amb_list]

            # （回答に含まれる）新たな曖昧さリストを現在の曖昧さリストの直後に挿入
            [amb_list.insert(index+i+1, new_amb_list[i]) for i in range(len(new_amb_list))]
        # もう一度for文を回して、曖昧さ（質問）によって参照されていない回答だけをチェックする処理に変更
        # else:
        #     amb_mid_def[index].append(True)
            # amb_comp_def.append(input)
            # amb_comp_def[-1].append(index)
    
    return amb_list, amb_mid_def


if amb_list:

    amb_def_list, amb_list = create_question(amb_list)

    print(amb_def_list, amb_list)

else:
    print("曖昧さは見つかりませんでした。")

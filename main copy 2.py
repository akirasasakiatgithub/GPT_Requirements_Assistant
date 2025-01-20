import sys
#import asyncio  # 非同期処理用
import ipdb

from input_requirement import input_requirement as inp
from use_openai_api import (extract_amb as exam,  reconstruct_requirements as recon)

input_result = inp()

amb_list = exam(input_result)

def clarify_ambiguity(amb_list):
    def_list = []
    index = 0
    d_id = 0

    # 初期のリストの要素のIDを加える
    [amb_part.append(i) for i, amb_part in enumerate(amb_list)]
    [amb_part.append(None) for amb_part in (amb_list)]

    while index < len(amb_list):

        amb_part = amb_list[index]

        # 回答入力(リスト形式)
        # 初回は曖昧な文のリストが返るのに対して、今回はユーザーの回答が返る
        input = inp(amb_part)

        # 曖昧さ定義をパスした時の処理
        if not input:
            amb_list.remove(amb_part)
            continue

        # 一度実行したリストを読まない印をつける。多分必要ない。
        # 必要なら後でamb_partのリストを必要な形に修正
        # amb_part.append(True)

        # 回答固有のID
        input.append(d_id)

        # 回答を曖昧さ（質問）に紐づけ
        input.append(amb_part[4])

        # 曖昧さへの回答をその為のリストへ加える
        # 回答が複数行（複数要素のリストかどうかで処理を分ける）
        # if len(input) > 2:
        #     [def_list.append(input[i]) for i in range(len(input)) if input[i] != input[-1]]
        # else:
        def_list.append(input)


        # 曖昧さ検出（ネストされたリスト形式）
        # examの内容を変更するかも
        new_amb_list = exam(input)

        if new_amb_list:
            # 新たな曖昧さにも固有のIDを追加
            [new_amb_part.append(len(amb_list)+i) for i, new_amb_part in enumerate(new_amb_list)]

            # amb_listに挿入する新たなリストにどの回答に紐づけるかの情報を付与
            [new_amb_part.append(d_id) for new_amb_part in new_amb_list]

            # 
            [amb_list.insert(index+i+1, new_amb_list[i]) for i in range(len(new_amb_list))]
        
        else:
            def_list[d_id].append(True)
            # amb_comp_def.append(input)
            # amb_comp_def[-1].append(index)
        d_id+=1
        index+=1
     
    # for amb_part in amb_list:
        
    #     [each_def.append(True) for each_def in amb_comp_def if type(amb_part[-1]) == int and each_def[-1] == amb_part[-1]]
    
    return amb_list, def_list

# def compose_requirements(def_list, amb_list):

#     for index in range(len(amb_list)):

#         for def_part in def_list:
#             # 回答を回避した曖昧さは削除しているので曖昧さに対して、必ず回答がある前提
#             # 回答が指す曖昧さ
#             def_part[1]




if amb_list:

    def_list, amb_list = clarify_ambiguity(amb_list)

    print(def_list, amb_list)

    # amb_list = 
    # def_list = 
         
    trans_list = [(dp[0], ap[2]) for ap in amb_list for dp in def_list if dp[2] == ap[4]]

    lang_trans_list = [f"{ap}は{dp}という意味です。" for dp, ap in trans_list]

    comp_req = recon(input_result, lang_trans_list)

    print(comp_req)

    with open("reconstruct_requrements", "w", encoding="utf-8") as file:
        file.writelines(comp_req)

else:
    print("曖昧さは見つかりませんでした。")

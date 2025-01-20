#import asyncio  # 非同期処理用
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

        # 曖昧さ定義をスキップした時の処理
        if not input:
            amb_list.remove(amb_part)
            continue

        # 回答固有のID
        input.append(d_id)

        # 回答を曖昧さ（質問）に紐づけ
        input.append(amb_part[4])

        # 曖昧さへの回答をその為のリストへ加える
        def_list.append(input)


        # 曖昧さ検出（ネストされたリスト形式）
        new_amb_list = exam(input)

        if new_amb_list:
            # 新たな曖昧さにも固有のIDを追加
            max_id = max(ap[4] for ap in amb_list)
            [new_amb_part.append(max_id+i+1) for i, new_amb_part in enumerate(new_amb_list)]

            # amb_listに挿入する新たなリストにどの回答に紐づけるかの情報を付与
            [new_amb_part.append(d_id) for new_amb_part in new_amb_list]

            # 新たな曖昧さを現在処理中の曖昧さの直後に加える
            [amb_list.insert(index+i+1, new_amb_list[i]) for i in range(len(new_amb_list))]
        
        else:
            def_list[d_id].append(True)
        d_id+=1
        index+=1
    
    return amb_list, def_list


if amb_list:

    # returnと受け取りで変数が逆になっている！　未修整　下のコードを逆にする必要あり
    def_list, amb_list = clarify_ambiguity(amb_list)

    print(def_list, amb_list)
         
    trans_list = [(dp[0], ap[2]) for ap in amb_list for dp in def_list if dp[2] == ap[4]]

    lang_trans_list = [f"{ap}は{dp}という意味です。" for dp, ap in trans_list]

    comp_req = recon(input_result, lang_trans_list)

    print(comp_req)

    with open("reconstruct_requrements", "w", encoding="utf-8") as file:
        file.writelines(comp_req)

else:
    print("曖昧さは見つかりませんでした。")

def new_create_question(amb_list):
    amb_mid_def = []
    amb_comp_def = []

    for index, amb_part in enumerate(amb_list):

        # 回答入力(リスト形式)
        # 初回は曖昧な文のリストが返るのに対して、今回はユーザーの回答が返る
        input = inp(amb_part)

        # 一度実行したリストを読まない印をつける。多分必要ない。
        # 必要なら後でamb_partのリストを必要な形に修正
        amb_part.append(True)

        if not index == 0:
            input.append(index-1)
        # 曖昧さへの回答をその為のリストへ加える
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
        else:
            amb_part.append(True)
            # amb_comp_def.append(input)
            # amb_comp_def[-1].append(index)
    
    return amb_list, amb_mid_def

            
            


        




        


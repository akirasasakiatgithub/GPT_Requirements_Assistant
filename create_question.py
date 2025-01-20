def create_question(amb_list):
    amb_def = []
    for index, amb_part in enumerate(amb_list)):
        # 回答入力(リスト形式)
        # 初回は曖昧な文のリストが返るのに対して、今回はユーザーの回答が返る
        input_result = inp(amb_part)

        # 曖昧さ定義をパスした時の処理
        # if amb_part[2] == input_result:
        #     amb_list.remove(amb_part)
        #     continue

        # 曖昧さ検出（ネストされたリスト形式）
        new_amb_list = exam(input_result)
        
        if new_amb_list:
            # 新たな曖昧さが指す曖昧さのID（index）を要素として追加
            [new_amb_list[i].append(index) for i in range(len(new_amb_list))]
            # その文の先頭から何文字目か？（文内ID）
            [new_amb_list[i].append(amb_part[1]) for i in range(len(new_amb_list))]

            # （回答に含まれる）新たな曖昧さリストを現在の曖昧さリストの直後に挿入
            [amb_list.insert(index+i+1, new_amb_list[i]) for i in range(len(new_amb_list))]
        else:
            amb_def.append(input_result)

    return amb_def, amb_list



def create_question(amb_list):
    amb_def_list = []
    i = 0
    while i < len(amb_list):
        # 回答入力(リスト形式)
        # 初回は曖昧な文のリストが返るのに対して、今回はユーザーの回答が返る
        input_result = inp(amb_list[i])
        
        # 曖昧さ定義をパスした時の処理
        if not input_result:
            # indexを前に詰めるためdelで削除
            del amb_list[i]
            continue
        # 曖昧さの質問でリストをつくり現在の曖昧さリストの直後に挿入
        inp_str = input_result[0]
        inp_part = [None, None, inp_str]
        amb_list.insert(i+1, inp_part)

        # 曖昧さ検出（ネストされたリスト形式）
        new_amb_list = exam(input_result)
        
        if new_amb_list:
            # 新たな曖昧さが指す曖昧さのID（index）を要素として追加
            [new_amb_list.append(i) for new_amb_list in new_amb_list]
            [new_amb_list.append(amb_list[i][1]) for new_amb_list in new_amb_list]

            # （回答に含まれる）新たな曖昧さリストを現在の曖昧さリストの直後に挿入
            [amb_list.insert(i+k+2, new_amb_list) for k, new_amb_list in enumerate(new_amb_list)]
        else:
            amb_def_part = [i, inp_str]
            amb_def_list.append(amb_def_part)

        i += 1

    return amb_def_list, amb_list
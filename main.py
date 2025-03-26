from tkinter_input import (input_requirement as inp, show_output_message as show, remove_settings as remove_set)
from use_openai_api import (extract_amb as exam,  reconstruct_requirements as recon)
import markdown2
import pdfkit

# wkhtmltopdfのパスを指定
config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

while True:
    input_result = inp()

    ai_response = exam(input_dict=input_result)
    # amb_list ⇒　辞書のリスト
    amb_list = ai_response["amb_info"]
    is_valid = ai_response["is_valid"]
    if is_valid:   
        break
    else:
        show("エラー", "質問への回答として不適切です。\n再入力してください。", "error")


def clarify_ambiguity(amb_list):
    def_list = []
    index = 0
    d_id = 0

    # 初期のリストの要素（辞書）のIDを加える
    for i, amb_part in enumerate(amb_list):
        amb_part["amb_id"] = i
        amb_part["aimed_def"] = None

    while index < len(amb_list):

        # openaiが抽出した曖昧さ情報のリスト
        amb_part = amb_list[index]

        # 回答入力(辞書内リスト形式)
        # 初回は曖昧な文の（辞書内）リストが返るのに対して、今回はユーザーの回答が返る
        input = inp(amb_part)

        # 曖昧さ定義をスキップした時の処理
        if not input:
            amb_list.remove(amb_part)
            continue

        # 回答固有のID
        input["def_id"] = d_id

        # 回答を曖昧さ（質問）に紐づけ
        input["aimed_amb"] = amb_part["amb_id"]

        # 適切な解答が成されるまで再入力を促す
        while True:
        
            # 曖昧さ検出（辞書内リスト内辞書形式）
            ai_response = exam(input_dict=input, amb_part=amb_part) # 1ターン前に自身が返した曖昧さを引数として用いる。
            # new_amb_list 辞書のリスト
            new_amb_list = ai_response["amb_info"]
            is_valid = ai_response["is_valid"]
            
            if is_valid:
                # 回答が適切ならその為のリストへ加える
                def_list.append(input)
                break
            else:
                show("エラー", "質問への回答として不適切です。\n再入力してください。", "error")
                # 元のinputを上書き
                input = inp(amb_part)

                # 曖昧さ定義をスキップした時の処理
                if not input:
                    amb_list.remove(amb_part)
                    break

                # 回答が改められたので再度追加処理
                input["def_id"] = d_id
                input["aimed_amb"] = amb_part["amb_id"]


        if new_amb_list:
            # 新たな曖昧さにも固有のIDを追加
            # [new_amb_part.append(len(amb_list)+i) for i, new_amb_part in enumerate(new_amb_list)]
            max_id = max(ap["amb_id"] for ap in amb_list)
            for i, new_amb_part in enumerate(new_amb_list):
                new_amb_part["amb_id"] = max_id + i + 1

            # amb_listに挿入する新たなリストにどの回答に紐づけるかの情報を付与
            for new_amb_part in new_amb_list:
                new_amb_part["aimed_def"] = d_id

            # 新たな曖昧さを現在処理中の曖昧さの直後に加える
            [amb_list.insert(index+i+1, new_amb_part) for i, new_amb_part in enumerate(new_amb_list)]
        
        # else:
        #     # 曖昧さが生まれなかった場合は新たな定義としてチェック（未使用＆全ての辞書にキーを追加しないと後でエラーになる）
        #     def_list[d_id]["final_answer"] = True
        d_id+=1
        index+=1
    
    return amb_list, def_list


if amb_list:
    
    amb_list, def_list = clarify_ambiguity(amb_list)

    # print(amb_list, def_list)
         
    trans_list = [[dp["definition"], ap["amb_str"], ap["sentence"]] for ap in amb_list for dp in def_list if dp["aimed_amb"] == ap["amb_id"]]

    lang_trans_list = [f"{asen}の{astr}は{df}という意味です。" for df, astr, asen in trans_list]

    with open("clarification requests", "w", encoding="utf-8") as file:
        file.writelines(lang_trans_list)

    comp_req = recon(input_result, lang_trans_list)

    show("新しい要求定義", comp_req, "result")

    with open("reconstruct_requrements.md", "w", encoding="utf-8") as file:
        file.writelines(comp_req)

    # CSSでフォント指定
    css = """
    <style>
    body {
        font-family: 'Meiryo';
    }
    </style>
    """

    # MarkdownをHTMLに変換
    html_content = css + markdown2.markdown(comp_req)

    

    with open("reconstruct_requrements.html", "w", encoding="utf-8") as file:
        file.writelines(html_content)

    # HTMLをPDFに変換して保存
    try:
        pdfkit.from_string(html_content, "reconstruct_requirement.pdf")
        print("PDF successfully created: reconstruct_requirement.pdf")
    except Exception as e:
        print(f"Error generating PDF: {e}")
        
else:
    show("解析結果", "曖昧さは見つかりませんでした。")


remove_set()

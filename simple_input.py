print("要件定義を入力してください。:")

lines = []

while True:
    line = input()
    if line == "":
        break
    lines.append(line)



# 入力の確認
print("以下の文章の曖昧さを調べます。")
for line in lines:
    print(line)
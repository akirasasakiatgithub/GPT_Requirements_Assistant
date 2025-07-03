# Clarify  -GPT_Requirements_Assistant
機能の概要
chatGPTのAPIを使い、要求定義の曖昧さを検出してユーザーに回答を促し、曖昧さが無くなるまで繰り返します。 最後に曖昧さの無くなった要求定義を再構成して提示します。

Overview
This tool leverages natural language processing with the OpenAI API to detect ambiguities in requirement definitions. When ambiguity is found, the user is prompted to provide a clearer definition. Repeat the clarification process until all ambiguities are resolved. The finalized requirements are then reconstructed and displayed.


### 動画による機能紹介　Explanation of functions by video
 [![アプリの使い方を見る](https://img.youtube.com/vi/gp6HOuigVDY/0.jpg)](https://www.youtube.com/watch?v=gp6HOuigVDY)



## exeファイルをダウンロードして使用する場合の手順
※openAIのAPIキーが必要です。  
※新規ユーザーには、アカウント作成時に一定の無料クレジットが付与されますが、使用回数によってはAPI利用料が発生します。

1. OpenAIのアカウントを作成し、APIキーを取得
   
- OpenAI公式サイトにアクセス：
  https://platform.openai.com/signup

- アカウントを作成し、ログイン後に以下のURLでAPIキーを発行：
  https://platform.openai.com/account/api-keys

- 発行されたAPIキー（sk-xxxx...）をコピーして控えておきます。

2. フォルダ内にある `env.example` を `env` にリネームし、取得したAPIキーを記入

OPENAI_API_KEY=your-api-key-here の your-api-key-here の部分を取得したAPIキーに書き換えて下さい。

3. `main.exe` をダブルクリックして起動

以上でアプリがOpenAI APIと接続して動作します。

`.env` が見つからない、またはAPIキーが空だとエラーになります。
`.env` は `main.exe` と同じフォルダに置く必要があります。

# Clarify - 自然言語処理を用いた要求定義サポートアプリ

## 概要
ClarifyはAI機能を用いて要求定義のサポートをするアプリです。
AIが入力された要求定義から曖昧さを検出し、明確化を促す質問を利用者に対して行い、それに対する回答によって明確な要求に書き換えます。
元の要求定義や回答から曖昧さが無くなるまでそれを繰り返し、最終的に明確化された新たな要求定義を生成します。

## Overview
Clarify is an application that uses AI to support requirements definition.
The AI analyzes the input requirements and identifies any ambiguities, then asks the user clarifying questions. Based on the user's responses, it rewrites the ambiguous parts into clearer statements.
This process is repeated until all ambiguities are resolved, resulting in a newly generated, unambiguous requirements definition.

## デモ動画  Demo video
https://www.youtube.com/watch?v=VijwWptPW3Y
[![使い方を見る](https://img.youtube.com/vi/VijwWptPW3Y/0.jpg)](https://www.youtube.com/watch?v=VijwWptPW3Y)

## 特徴（主な機能）

- 曖昧と判定された理由を表示
- 解答例の提案
- 文脈を考慮した曖昧さと適切さの判定
- 最終的な出力への見出し情報の反映
- スキップ機能

## Features

- Displays the reason why a statement is considered ambiguous
- Suggests example answers
- Evaluates ambiguity and appropriateness based on context
- Reflects heading information in the final output
- Skip function for bypassing specific steps

## exeファイルをダウンロードして使用する場合の手順

このツールにはOpenAIのAPIキーが必要です。アプリケーションを実行するには、以下の手順に従ってセットアップしてください。
※新規ユーザーにはアカウント作成時に一定の無料クレジットが付与されますが、使用回数によってはAPI利用料が発生します。

### 1. OpenAIのアカウントを作成し、APIキーを取得
   
- OpenAI公式サイトにアクセス：
  https://platform.openai.com/signup

- アカウントを作成し、ログイン後に以下のURLでAPIキーを発行：
  https://platform.openai.com/account/api-keys

- 発行されたAPIキー（sk-xxxx...）をコピーして控えておきます。

### 2. `Assets` の `Clarify.zip` をダウンロードし解凍

- GitHubリリースページの `Assets` から `Clarify.zip` をダウンロードし、任意の場所に展開します。

### 3. `.env`ファイルの作成とAPIキーの入力

-  `.env.example` を `.env` にリネームします。
- `.env.example` をテキストエディタで開きます。
- OPENAI_API_KEY=your-api-key-here の your-api-key-here の部分を消して、取得したAPIキーを貼り付けて下さい。

### 4. `main.exe` をダブルクリックして起動

- `main.exe` をダブルクリックして起動します。

以上でアプリがOpenAI APIと接続して動作します。

`.env` が見つからない、またはAPIキーが空だとエラーになります。
`.env` は `main.exe` と同じフォルダに置く必要があります。  


### 1. Create an OpenAI account and obtain an API key

- Visit the official OpenAI website:  
  https://platform.openai.com/signup

- After creating an account and logging in, generate an API key from the following page:  
  https://platform.openai.com/account/api-keys

- Copy and save the issued API key (e.g., sk-xxxx...).

### 2. Download and extract `Clarify.zip` from `Assets`

- Go to the GitHub Releases page and download `Clarify.zip` from the `Assets` section.  
  Extract the contents to a location of your choice.

### 3. Create a `.env` file and input your API key

- Rename `.env.example` to `.env`.  
- Open `.env` in a text editor.  
- Replace `your-api-key-here` in the line `OPENAI_API_KEY=your-api-key-here` with your actual API key.

### 4. Launch the application by double-clicking `main.exe`

- Double-click `main.exe` to start the application.

The app will now connect to the OpenAI API and run.

If the `.env` file is missing or the API key is empty, an error will occur.  
Make sure the `.env` file is placed in the same folder as `main.exe`.

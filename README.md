# TACT

![TACT Logo](assets/TACT%20Image.webp)

**Token Analysis and Counting Tool**

## 概要

**TACT** は、テキスト内のトークン数を正確にカウントし、分析するためのシンプルかつ強力なツールです。ユーザーフレンドリーなGUIを提供し、さまざまなOpenAIモデルに対応しています。デベロッパーや研究者、ライターなど、テキスト解析が必要なすべてのユーザーに最適です。

## 特徴

- **直感的なGUI**: シンプルで使いやすいインターフェース。
- **複数モデル対応**: CSVファイルからモデルを追加・変更可能。
- **トークン数のコピー**: クリップボードにトークン数を簡単にコピー。
- **トークン数の保存**: 結果をテキストファイルやCSVファイルとして保存。
- **カスタマイズ可能**: PRISMスタイルを基にしたカスタマイズ可能なデザイン。
- **Aboutセクション**: アプリの情報とライセンスを確認。

## スクリーンショット

![TACT Main Interface](assets/screenshot_main.png)
![TACT About Section](assets/screenshot_about.png)

## インストール

### 前提条件

- **Python 3.x** がインストールされていること。
- `pip` がインストールされていること。

### 必要なライブラリのインストール

1. **リポジトリをクローン**

    ```bash
    git clone https://github.com/your-username/TACT.git
    cd TACT
    ```

2. **仮想環境の作成（オプション）**

    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3. **依存関係のインストール**

    ```bash
    pip install -r requirements.txt
    ```

## 使用方法

1. **アプリケーションの起動**

    ```bash
    python src/tact.py
    ```

2. **テキストの入力**

    テキストボックスにトークンをカウントしたいテキストを入力します。

3. **モデルの選択**

    ドロップダウンメニューから使用するモデルを選択します。デフォルトではGPT-3.5-turboとGPT-4が含まれています。追加のモデルを使用したい場合は、「Load Models CSV」ボタンからCSVファイルをロードします。

4. **トークンのカウント**

    「Count Tokens」ボタンをクリックすると、テキスト内のトークン数が表示されます。

5. **結果のコピーと保存**

    - **Copy Count**: トークン数をクリップボードにコピーします。
    - **Save Count**: トークン数をテキストファイルやCSVファイルとして保存します。

6. **About**

    「About」ボタンをクリックして、アプリの詳細情報とライセンスを確認します。

## モデルの追加

1. **CSVファイルの準備**

    以下のフォーマットでCSVファイルを作成します：

    ```csv
    model_name,encoding_name
    GPT-3.5-turbo,gpt-3.5-turbo
    GPT-4,gpt-4
    ```

2. **CSVファイルのロード**

    アプリ内の「Load Models CSV」ボタンをクリックし、作成したCSVファイルを選択します。

## フォルダ構成

- **LICENSE**: MITライセンスのテキストファイル。
- **README.md**: プロジェクトの概要、インストール方法、使用方法などを記載。
- **requirements.txt**: プロジェクトで必要なPythonライブラリを記載。
- **.gitignore**: Gitに含めたくないファイルやフォルダを指定。
- **src/**: ソースコードとモデルCSVファイルを格納。
- **assets/**: GUIで使用する画像やアイコンなどのアセット。
- **docs/**: ドキュメントやユーザーマニュアル。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細については、[LICENSE](LICENSE) ファイルを参照してください。

## 著作権

© 2024 KookyOstrich

## 貢献

貢献を歓迎します！バグ報告、新機能の提案、プルリクエストなど、お気軽にお知らせください。

## サポート

何か問題が発生した場合は、[Issues](https://github.com/KookyOstrich/TACT/issues) セクションで報告してください。


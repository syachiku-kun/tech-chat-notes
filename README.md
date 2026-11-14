# tech-chat-notes
技術関連チャットのノート化 / 相談があったり回答があったりした技術的内容を、自動的にまとめてノート化(QandAのように可視化)する Windows 向けデスクトップアプリを目標とする。利用者が各自ダウンロードしてローカルで使用する。

## ドキュメント

| 分類 | ドキュメント | 内容 |
| :--- | :--- | :--- |
| 要件 | [機能要件・非機能要件](docs/requirements/機能要件・非機能要件.md) | 提供する機能と運用上の前提 |
| 要件 | [技術スタック選定・システム構成](docs/requirements/技術スタック選定・システム構成.md) | 技術候補の比較、採否、未決事項 |
| 要件 | [システム構成図](docs/requirements/システム構成図.md) | 画面・処理・データの責務と流れ |
| 要件 | [ローカル Embedding モデル選定](docs/requirements/ローカルEmbeddingモデル選定.md) | 意味検索モデルの候補と評価項目 |
| 要件 | [生成 AI の調査メモ](docs/requirements/生成AIの調査文.md) | Codex の接続方式に関する調査記録 |
| 仕様 | [画面仕様書](docs/specifications/画面仕様書.md) | 画面と操作、画面モック |
| 仕様 | [API 仕様書](docs/specifications/API仕様書.md) | ローカル HTTP エンドポイントと入出力 |
| 仕様 | [DB 仕様書](docs/specifications/DB仕様書.md) | テーブル案と論理・物理 ER 図 |

## Python での開発開始手順（Windows / PowerShell）

現在の `main.py` は開発用の起動画面です。取込・要約・検索などの機能は実装途中です。

1. [Python 公式の Windows 向け配布ページ](https://www.python.org/downloads/windows/)から Python 3.13 の 64-bit インストーラーをダウンロードして実行します。インストーラーに「Add python.exe to PATH」が表示された場合は有効にします。
2. 新しい PowerShell を開き、Python を確認します。

   ```powershell
   py -3.13 --version
   ```

3. [Poetry 公式の Windows 向け手順](https://python-poetry.org/docs/#installation)で Poetry を導入します。

   ```powershell
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -3.13 -
   ```

   PowerShell を開き直して `poetry --version` を確認します。コマンドが見つからない場合は、Poetry の公式手順に従って `%APPDATA%\Python\Scripts` を `PATH` に追加します。

4. このリポジトリを取得してルートに移動し、`pyproject.toml` に指定したライブラリを導入します。

   ```powershell
   git clone https://github.com/maro-syachiku/tech-chat-notes.git
   cd tech-chat-notes
   poetry install
   ```

   既にリポジトリを取得済みなら、ルートで `poetry install` だけ実行します。Python 3.13 以外の環境が選ばれた場合は、`poetry env use` で Python 3.13 の実行ファイルを指定してから再実行します。

5. メインウィンドウを起動します。

   ```powershell
   poetry run python .\src\tech_chat_notes\main.py
   ```

起動すると「tech-chat-notes の開発用起動画面」と表示されます。SQLite は Python 標準ライブラリを使用します。Embedding モデルと Codex の接続方式は未決定のため、この起動画面では使いません。


## 現在の設計方針

- Windows 向け portable デスクトップアプリとして開発する。
- CustomTkinter、SQLite、LanceDB Embedded、PyInstaller を初期構成として採用する。
- 意味検索の Embedding はローカル実行を前提とし、モデルは評価後に確定する。
- 要約には Codex を使う。アプリから呼び出す接続方式と認証方式は未決定。トーク本文を外部送信する範囲と送信先を利用者に示す。
- LINE トークは利用者が保存した `.txt` から取り込み、LINE API には接続しない。

詳しい前提と未決事項は各要件・構成資料を参照してください。候補や設計案は、採用・実装済みと明記されていない限り確定仕様ではありません。

## お知らせ

* issue上のやり取りが持つ公開範囲は、リポジトリが持つ公開範囲を引き継ぐらしいです。
* そのため、このリポジトリは一時的にプライベートとしています。
* 最終的には「ソースコード公開用の別リポジトリを作成する」「このリポジトリはパブリックでも問題ない」の2択を検討する必要があると思われます。

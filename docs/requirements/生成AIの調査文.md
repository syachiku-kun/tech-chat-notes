## 質問概要

インストール不要なポータブル可能な、GPTモデル等と通信することによって回答を得ることができる方法を教えて。

## 結論

本プロジェクトでは要約用生成 AI に Codex を使うことを決定した。アプリからの接続方式と認証方式は未決定であり、この文書は方式を比較するための調査記録である。

調査時点の候補として、公式 Codex CLI の portable 版や Codex App Server などを比較している。利用する方式を確定する前に、現行の公式仕様と利用条件を再確認する。

## 調査メモ

調査時点では、公式 Codex CLI の portable 版と OpenCode の portable 版を有力候補としている。

どちらも次の使い方が可能です。

- OpenAI APIキーを使わず、ChatGPTアカウントでOAuth認証する
- 初回認証後は、プロンプトを渡して非対話形式でGPTモデルを実行する
- Windowsにグローバルインストールせず、ダウンロードした実行ファイルを起動する
- PowerShellやPythonなど、外部プログラムから呼び出す

Codex CLIはOpenAI公式、OpenCodeはサードパーティ製です。両者とも非対話実行とChatGPT認証を公式ドキュメントで確認できます。

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub+4



## 1. 候補の比較

| 方法               | OAuth      | 非対話実行          | ポータブル性           | 評価        |
| ---------------- | ---------- | -------------- | ---------------- | --------- |
| Codex CLI        | 対応         | `codex exec`   | Windows実行ファイルあり  | 最有力       |
| OpenCode CLI     | 対応         | `opencode run` | Windows ZIPあり    | 有力        |
| Codex App Server | Codex認証を利用 | JSON-RPC       | Codex実行ファイルを利用可能 | アプリ組み込み向け |
| Codex SDK        | Codex認証を利用 | プログラムから実行      | Node.js環境が必要     | 開発者向け     |
| Pi Coding Agent  | 対応         | Print / RPCモード | 通常はNode.js環境が必要  | 条件付き      |

ここでは「ポータブル」を、管理者権限やシステムへのインストールなしで実行できることとしています。認証情報や設定まで実行ファイルと同じフォルダに保存できるかは別の条件です。

## 2. Codex CLI：最も確実な方法

OpenAI公式

Windows / macOS / Linux

入手先：[Codex CLI GitHub Releases](https://github.com/openai/codex/releases?utm_source=chatgpt.com)

Windows x64では、Release Assetsから `codex-x86_64-pc-windows-msvc.exe.zip` を選び、展開します。npmやNode.jsのインストールは不要です。配布ZIPに含まれる補助ファイルもそのまま保持してください。

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub+1



### 実行例（PowerShell）

以下は `C:\Tools\codex` に展開した場合の例です。

```
# 実行ファイル
$exe = "C:\Tools\codex\codex-x86_64-pc-windows-msvc.exe"

# 設定・認証情報の保存先を指定
$env:CODEX_HOME = "C:\Tools\codex\data"
New-Item -ItemType Directory -Force $env:CODEX_HOME | Out-Null

# 認証情報をファイルに保存
'cli_auth_credentials_store = "file"' |
  Set-Content "$env:CODEX_HOME\config.toml" -Encoding ascii

# 初回のみブラウザでOAuth認証
& $exe login

# 非対話で実行
& $exe exec --skip-git-repo-check --sandbox read-only `
  "Python 3.13の特徴を3つ説明してください"
```

最終回答をファイルに保存する場合：

```
& $exe exec --skip-git-repo-check `
  -o "C:\Tools\codex\result.txt" `
  "Python 3.13の特徴を3つ説明してください"
```

JSON Lines形式で実行結果や進捗を取得する場合：

```
& $exe exec --json --skip-git-repo-check `
  "Python 3.13の特徴を3つ説明してください"
```

`codex exec` は原則として最終回答を標準出力に出します。`--json` はJSONLイベント形式になり、外部プログラムとの連携に利用できます。

[image](https://www.google.com/s2/favicons?domain=https://learn.chatgpt.com\&sz=32)

ChatGPT Learn+1



### ポータブル化の注意点

`CODEX_HOME` を指定することで、設定と認証キャッシュを任意の場所に変更できます。これは公式の設定です。

[image](https://www.google.com/s2/favicons?domain=https://learn.chatgpt.com\&sz=32)

ChatGPT Learn+1



ただし、OAuth認証キャッシュにはアクセストークンが含まれます。ポータブルフォルダごと他人に配布したり、Gitリポジトリに含めたりしないでください。別PCへの移動時は、そのPCで再認証する運用が安全です。

また、GUIがない環境では `codex login --device-auth` によるデバイスコード認証も利用できます。ただし、認証方式の有効化が必要な場合があります。

## 3. OpenCode CLI：Codex以外の有力候補

オープンソース / サードパーティ製

Windows / macOS / Linux

入手先：[OpenCode公式サイト](https://opencode.ai/docs/?utm_source=chatgpt.com)

OpenCodeもChatGPT Plus / ProによるOAuth認証を標準サポートしています。Windows向けのスタンドアロンCLIバイナリも配布されています。

[image](https://www.google.com/s2/favicons?domain=https://opencode.ai\&sz=32)

OpenCode+1



### 利用手順

まず配布ZIPを展開して、PowerShellから実行します。以下では `opencode.exe` という名前にした場合を想定しています。

```
# 初回認証
.\opencode.exe
```

初回は画面内で `/connect` を実行し、OpenAI → Sign in with ChatGPT を選択します。

認証後は対話画面を閉じ、次のように実行します。

```
# 通常の非対話実行
.\opencode.exe run "Python 3.13の特徴を説明して"

# JSONL形式の出力
.\opencode.exe run --format json "Python 3.13の特徴を説明して"

# 利用可能なモデルを確認
.\opencode.exe models
```

モデルを指定する場合は、利用可能なモデルIDを確認して `--model openai/<model-id>` を付けます。

OpenCodeにはバックグラウンドサービス機能もあり、CLIから繰り返しプロセスを起動する方式だけでなく、常駐プロセスへ接続する構成も可能です。

[image](https://www.google.com/s2/favicons?domain=https://opencode.ai\&sz=32)

OpenCode+1



Codexとの主な違いは、複数のLLMプロバイダーに対応している点です。ただし、ChatGPTのOAuthで利用できるモデルは、認証先とアカウントの権限に依存します。

## 4. pi-rust：単一バイナリ型の追加候補

入手先：[pi-rust Releases](https://github.com/yannelli/pi-rust/releases?utm_source=chatgpt.com)

標準のPi Coding AgentはNode.jsが必要ですが、Rust移植版の `pi-rust` はNode.jsを必要としません。

- Windows x64用の配布ZIPあり
- OpenAI CodexのOAuthログインに対応
- `pi -p` で非対話実行
- `--mode json` でJSONイベント取得
- `--mode rpc` で外部アプリケーションから制御可能

利用例：

```
# 初回認証
.\pi.exe
# 対話画面で /login から OpenAI Codex を選択

# 非対話実行
.\pi.exe -p "Python 3.13の特徴を説明して"

# JSONイベント取得
.\pi.exe --mode json -p "Python 3.13の特徴を説明して"
```

`PI_CODING_AGENT_DIR` を使い、設定や認証情報の保存場所も変更できます。

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub+1



ただし、pi-rustは独立したコミュニティ実装です。OpenAI公式のCodex CLIよりも、将来の認証方式やモデル仕様変更による互換性リスクを重視する必要があります。

## 5. アプリケーションへ組み込む方法

単発の処理だけでなく、独自アプリケーションから繰り返しGPTを呼び出す場合は、Codex App Serverも候補です。

構成イメージ

独自アプリケーション

Python / Rust / C# など

プロセス起動・JSON-RPC通信

Codex App Server

codex app-server

ChatGPT認証による通信

OpenAIのCodexモデル実行基盤

`codex app-server` は標準入出力を使ったJSON-RPC通信に対応しており、会話の継続、実行イベントの取得、承認処理などを実装できます。

[image](https://www.google.com/s2/favicons?domain=https://learn.chatgpt.com\&sz=32)

ChatGPT Learn+1



なお、Codex SDKにもTypeScript版だけでなくPython版があります。TypeScript版はNode.js、Python版はPython 3.10以降が必要です。SDKを実行環境と一緒に同梱する構成は可能ですが、単体EXEとして扱いたいならCLIやApp Serverの直接利用が簡単です。

[image](https://www.google.com/s2/favicons?domain=https://learn.chatgpt.com\&sz=32)

ChatGPT Learn



## 6. 運用上の重要な制約

APIキー不要と、APIを使用していないことは別です。 OAuth方式でも内部ではネットワーク経由でOpenAIのサービスと通信します。

また、ChatGPTのOAuth認証によってOpenAI Platform APIの全機能が使えるわけではありません。利用可能なモデルはCodex側の対応状況と契約プランに依存します。

特に以下は注意が必要です。

- 初回のOAuth認証には通常、利用者によるブラウザ操作が必要です。
- ChatGPTプランに応じた利用回数・レート制限があります。
- 外部アプリからの繰り返し実行では、認証情報の更新、タイムアウト、エラー処理が必要です。
- 複数ユーザー向けサービスに組み込む場合は、個人のChatGPT認証を共有するのではなく、利用規約・認証設計を別途検討する必要があります。

## 推奨する選び方

| 目的                       | 推奨                     |
| ------------------------ | ---------------------- |
| 外部プログラムから1回ずつGPTを実行      | Codex CLI              |
| 複数プロバイダーを切り替えたい          | OpenCode               |
| Node.jsなしの軽量な単体アプリが必要    | Codex CLI / pi-rust    |
| RustやPythonのアプリに深く組み込みたい | Codex App Server       |
| 継続的な会話・状態管理が必要           | Codex App Server / SDK |

今回の条件で最初に検証すべきなのは、Codex CLIのWindows向けZIP版 + `codex exec` + `CODEX_HOME` の構成です。

この方法であれば、npm・Node.jsのインストールを前提とせず、実行ファイルを同梱したアプリケーションから非対話でGPTを利用できます。

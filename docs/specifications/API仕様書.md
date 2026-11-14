# API 仕様書（設計案）

## 共通仕様

画面から利用する HTTP API のエンドポイント案。現在は未実装。アプリのプロセス内で起動するローカル API を想定し、`127.0.0.1` のみで待ち受ける。独立したバックエンドの配布や公開サーバーは設けない。採用する HTTP ライブラリ、ポート、起動・終了方法は実装前に決める。

- ベースパス：`/api`。以下のエンドポイントはベースパスからの相対パス。
- API 仕様バージョン：`1`。URL には含めない。
- 本文：JSON（`Content-Type: application/json; charset=utf-8`）。パスで指定したローカルファイルの読込はアプリ自身が行う。
- ID：UUID v4 文字列。日時：UTC の ISO 8601 文字列（例：`2026-11-14T12:00:00Z`）。
- エラー本文：`{"code": "文字列", "message": "利用者向け概要"}`。トーク本文、認証情報、外部サービスの生レスポンスは含めない。
- 共通ステータス：`400` 入力不正、`404` 対象なし、`409` 状態競合、`500` 内部エラー。各エンドポイント固有の応答は下記に記載する。
- ローカル API の呼び出し元制限と認証方式は未決定。実装前に決める。

---
# エンドポイントは検討中
---
## imports

利用者が選択した LINE の `.txt` ファイルを解析し、トークルームとメッセージを SQLite に保存する。取込件数と重複件数を返す。

### `POST /imports`

保存済み LINE `.txt` を取り込む。

| リクエスト（JSON） | 型 | 内容 |
| :--- | :--- | :--- |
| `file_path` | `string` | 利用者が選択したローカル `.txt` の絶対パス |

| レスポンス（`201`） | 型 | 内容 |
| :--- | :--- | :--- |
| `import_batch_id` | `string (uuid)` | 取込履歴 ID |
| `imported_count` | `integer` | 新規メッセージ数 |
| `duplicate_count` | `integer` | 重複メッセージ数 |

ファイル不在は `404`、形式不明は `422`。文字コードと重複判定方法は実データ確認後に決める。

## 要約

### `GET /conversations/{conversation_id}/summary-preview`

Codex に送る対象を実行前に確認する。

| リクエスト | 型 | 場所・内容 |
| :--- | :--- | :--- |
| `conversation_id` | `string (uuid)` | パス。対象会話 |
| `from_at`, `to_at` | `string (date-time)` | クエリ。対象期間の開始・終了 |

| レスポンス（`200`） | 型 | 内容 |
| :--- | :--- | :--- |
| `target_count` | `integer` | 対象メッセージ数 |
| `destination` | `string` | 利用者に示す Codex の送信先 |
| `send_scope` | `string` | 利用者に示す送信範囲 |

### `POST /summary-runs`

手動またはアプリ起動中の定期要約を開始する。処理を待たずに実行 ID を返す。

| リクエスト（JSON） | 型 | 内容 |
| :--- | :--- | :--- |
| `conversation_id` | `string (uuid)` | 対象会話 |
| `from_at`, `to_at` | `string (date-time)` | 対象期間 |
| `trigger` | `string` | `manual` または `scheduled` |

| レスポンス（`202`） | 型 | 内容 |
| :--- | :--- | :--- |
| `run_id` | `string (uuid)` | 実行履歴 ID |
| `status` | `string` | 初期状態。状態値は未決定 |

### `GET /summary-runs/{run_id}`

| リクエスト | 型 | 場所・内容 |
| :--- | :--- | :--- |
| `run_id` | `string (uuid)` | パス。実行履歴 ID |

| レスポンス（`200`） | 型 | 内容 |
| :--- | :--- | :--- |
| `run_id` | `string (uuid)` | 実行履歴 ID |
| `status` | `string` | 現在の処理状態 |
| `summary_ids` | `array<string (uuid)>` | 作成された要約 ID |
| `error` | `object \| null` | 失敗時のみ `code` と `message` |

## 要約・分類

### `GET /summaries`

| リクエスト | 型 | 場所・内容 |
| :--- | :--- | :--- |
| `conversation_id` | `string (uuid), optional` | クエリ。省略時は全会話 |

| レスポンス（`200`） | 型 | 内容 |
| :--- | :--- | :--- |
| `items` | `array<object>` | 要約一覧 |
| `items[].id` | `string (uuid)` | 要約 ID |
| `items[].body` | `string` | 要約本文 |
| `items[].from_at`, `items[].to_at` | `string (date-time)` | 対象期間 |
| `items[].tag_ids` | `array<string (uuid)>` | タグ ID |
| `items[].is_bookmarked` | `boolean` | ブックマーク状態 |

### `PATCH /summaries/{summary_id}`

| 区分 | フィールド | 型 | 内容 |
| :--- | :--- | :--- | :--- |
| パス | `summary_id` | `string (uuid)` | 編集対象 |
| リクエスト JSON | `body` | `string` | 新しい要約本文 |
| レスポンス `200` | `summary` | `object` | 更新後の要約。`GET /summaries` の要素と同じ形 |

SQLite と LanceDB の更新が不一致になった場合は `409` とし、再構築の対象にする。

### `DELETE /summaries/{summary_id}`

| 区分 | フィールド | 型 | 内容 |
| :--- | :--- | :--- | :--- |
| パス | `summary_id` | `string (uuid)` | 削除対象 |
| レスポンス `204` | 本文なし | `null` | 正常終了 |

SQLite と検索用データを削除する。

### `PUT /summaries/{summary_id}/tags`

| 区分 | フィールド | 型 | 内容 |
| :--- | :--- | :--- | :--- |
| パス | `summary_id` | `string (uuid)` | 更新対象 |
| リクエスト JSON | `tag_ids` | `array<string (uuid)>` | 置き換え後のタグ ID |
| レスポンス `200` | `tag_ids` | `array<string (uuid)>` | 保存後の一覧 |

### `PUT /summaries/{summary_id}/bookmark`

| 区分 | フィールド | 型 | 内容 |
| :--- | :--- | :--- | :--- |
| パス | `summary_id` | `string (uuid)` | 更新対象 |
| リクエスト JSON | `is_bookmarked` | `boolean` | 希望状態 |
| レスポンス `200` | `is_bookmarked` | `boolean` | 保存後の状態 |

## 検索

### `GET /summaries/search`

意味検索を行い、SQLite の要約本文を返す。

| リクエスト | 型 | 場所・内容 |
| :--- | :--- | :--- |
| `query` | `string` | クエリ。空文字は不可 |
| `limit` | `integer` | クエリ。上限は未決定 |

| レスポンス（`200`） | 型 | 内容 |
| :--- | :--- | :--- |
| `items` | `array<object>` | 検索結果 |
| `items[].summary_id` | `string (uuid)` | 要約 ID |
| `items[].body` | `string` | 要約本文 |
| `items[].rank` | `integer` | 1 から始まる順位 |
| `items[].score` | `number` | 類似スコア |

モデル未準備または検索用データ未構築は `409`。スコアの尺度はモデル決定後に定義する。

## 設定

### `GET /settings`

| 区分 | フィールド | 型 | 内容 |
| :--- | :--- | :--- | :--- |
| リクエスト | 本文なし | `null` | 入力なし |
| レスポンス `200` | `destination` | `string` | Codex の送信先 |
| レスポンス `200` | `has_credentials` | `boolean` | 認証情報の登録状態 |
| レスポンス `200` | `data_directory` | `string` | 保存先の絶対パス |
| レスポンス `200` | `embedding_model` | `string \| null` | 未決定・未設定なら `null` |

認証情報の中身は返さない。

### `PATCH /settings`

| 区分 | フィールド | 型 | 内容 |
| :--- | :--- | :--- | :--- |
| リクエスト JSON | `settings` | `object<string, string>` | 秘密情報を含まない設定名と値 |
| レスポンス `200` | 設定 | `object` | `GET /settings` と同じ形 |

許可する設定名と値の規則、および認証情報の登録方法は未決定。

## 実装前に決めること

ローカル API の認証と呼び出し元制限、ポート、ライブラリ、各操作の進捗・キャンセル、Codex の接続方式、要約単位、検索件数上限。エンドポイント・フィールド・ステータスは実装開始時に画面仕様と照合する。

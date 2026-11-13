# ローカル Embedding モデル選定

## 目的と結論

LINE トークから作成した日本語の要約を、利用者の短い検索文から意味検索する。Windows の portable 配布物にモデルを同梱し、文章のベクトル化を利用者の PC 内で行う。

**初期採用候補は [`intfloat/multilingual-e5-small`](https://huggingface.co/intfloat/multilingual-e5-small) とする。** 多言語検索向けのモデルで、384 次元、最大 512 トークン。MIT ライセンス。大きいモデルより配布・実行の負担を抑えやすいと判断した。日本語の技術相談データでの検索精度と Windows 配布物の動作は未検証のため、実装前に評価する。

## 候補比較

| 採否 | モデル | ベクトル次元 | 入力長 | ライセンス | 判断 |
| :--- | :--- | ---: | :--- | :--- | :--- |
| 初期採用候補 | [`multilingual-e5-small`](https://huggingface.co/intfloat/multilingual-e5-small) | 384 | 最大 512 トークン | MIT | 多言語の検索用モデル。小型で初期配布に向く。長い要約は分割が必要。 |
| 比較候補 | [`multilingual-e5-base`](https://huggingface.co/intfloat/multilingual-e5-base) | 768 | 最大 512 トークン | MIT | 同系列の大型モデル。精度が不足した場合に比較する。 |
| 比較候補 | [`paraphrase-multilingual-MiniLM-L12-v2`](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2) | 384 | 最大 128 トークン | Apache-2.0 | 多言語対応で扱いやすいが、要約の検索では入力長が短い。 |
| 比較候補 | [`BAAI/bge-m3`](https://huggingface.co/BAAI/bge-m3) | 1024 | 最大 8192 トークン | MIT | 長文に対応し検索方式も豊富。ただし初期の portable 配布にはモデルと実行環境の負担が大きい。 |

入力長・次元・ライセンスは各モデルカードの記載に基づく。配布サイズや CPU 上の速度は未測定のため、比較表に推測値を置かない。

## 利用方法

- 要約文に `passage: `、検索文に `query: ` を付けて、**同じモデル**でベクトル化する。これは E5 のモデルカードが指定する検索時の形式である。
- 要約ベクトルと要約 ID を LanceDB に保存する。トーク・要約本文・タグは SQLite に保存する。
- モデルのファイルを配布物に同梱し、実行時にモデルを自動ダウンロードしない。ベクトル化時に外部 Embedding API へ文章を送信しない。
- モデルの識別子と版、次元数を記録する。モデルを変更したときは、保存済み要約を新モデルで再ベクトル化する。
- 512 トークンを超える要約を単純に切り捨てない。分割方法と複数ベクトルの扱いを実装時に決める。

## 採用を確定するための確認

1. 実際の日本語の技術相談・要約を使い、短い検索文に対する上位検索結果を他候補と比較する。
2. 対象 Windows 環境の CPU で、初回起動時間・検索時の変換時間・メモリ使用量・配布物サイズを測る。
3. PyInstaller でモデルと必要な実行ライブラリを同梱し、ネットワーク接続なしで起動・検索できることを確認する。
4. 同梱するモデルと依存ライブラリのライセンス表記を配布物に含める。

## 参考資料

- [Multilingual E5 small モデルカード](https://huggingface.co/intfloat/multilingual-e5-small)
- [Multilingual E5 base モデルカード](https://huggingface.co/intfloat/multilingual-e5-base)
- [Multilingual MiniLM モデルカード](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)
- [BGE-M3 モデルカード](https://huggingface.co/BAAI/bge-m3)
- [Sentence Transformers の検索ガイド](https://www.sbert.net/examples/sentence_transformer/applications/semantic-search/README.html)

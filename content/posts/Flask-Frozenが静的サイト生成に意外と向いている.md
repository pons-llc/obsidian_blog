---
title: Flask-Frozenが静的サイト生成に意外と向いている
slug: frozen-flask-static-generation
date: 2026-05-13
tags:
  - Flask
  - 技術
summary: Frozen-Flaskはフラスコアプリを丸ごと静的HTMLに変換する。Pythonで自由にロジックを書けるのが地味に強い。
draft: false
---

静的サイトジェネレーターといえば Hugo、Jekyll、Eleventy あたりが有名だ。でも Python を普段使いしているなら Frozen-Flask は意外な選択肢になる。[[ObsidianとFlask-Frozenでブログを作った理由|なぜこの構成を選んだか]]も参照。

## 仕組みはシンプル

Frozen-Flask（`flask-frozen`）は Flask アプリの全URLをクロールして、レスポンスをそのままHTMLファイルとして保存する。

```python
from flask_frozen import Freezer
freezer = Freezer(app)
freezer.freeze()  # これだけ
```

`python freeze.py` を実行すると `build/` ディレクトリに静的HTMLが生成される。あとはそれをサーバーに置くだけ。

## ロジックをPythonで書ける

Hugo や Jekyll では独自のテンプレート構文やショートコードを覚える必要がある。Flask なら Python のコードがそのまま動く。

たとえばタグ別の記事一覧、関連記事の表示、記事数によるソート順の切り替え——これらを普通の Python 関数として書ける。フレームワーク固有の書き方を調べる時間がかからない。

## 開発サーバーでリアルタイムプレビュー

`python app.py` で起動したローカルサーバーは通常の Flask アプリとして動く。ファイルを変更すると自動でリロードされる。書きながらブラウザで確認するサイクルが速い。

本番用のビルドと開発用のプレビューが同じコードベースなので、「ローカルでは動いたのに本番で崩れた」が起きにくい。

## 向いているもの・向いていないもの

静的サイトなので、コメントやリアルタイム更新には向かない。でもブログはそもそも静的でいい。読まれるだけのコンテンツに動的な仕組みは不要だ。

ページ数が数万を超えるようなサイトではビルド時間が問題になるかもしれないが、個人ブログのスケールなら気にならない。生成した静的ファイルは[[GitHub + Cloudflare Pagesで無料ホスティング|Cloudflare Pagesで無料でホストできる]]。

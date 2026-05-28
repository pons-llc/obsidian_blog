# blogtemplate

ObsidianのMarkdownファイルをFlask-Frozenで静的HTMLに変換するブログシステム。

## スキル

`/blog` スキルで以下の操作が案内できる：

- 新規投稿の作成（フロントマター付きMarkdownを自動生成）
- ローカルプレビューの起動
- 静的ファイルのビルド
- 投稿一覧の確認・下書き管理

`/design` スキルでブログのデザインをインタラクティブにカスタマイズできる：

- 好みのヒアリング（用途・雰囲気・カラー・フォント）
- `static/css/style.css` を CSS変数ベースで書き換え
- Google Fonts 導入時は `templates/base.html` も更新
- プレビューしながら反復修正

## よく使うコマンド

```bash
# 依存インストール（初回のみ）
uv pip install -r requirements.txt

# ローカルプレビュー（http://localhost:5000）+ OGP画像生成
uv run python app.py

# 静的ファイル生成（build/ に出力）+ OGP画像生成
SITE_URL=https://yourblog.pages.dev uv run python freeze.py

# サイト名も変更する場合
SITE_NAME="ブログ名" SITE_URL=https://yourblog.pages.dev uv run python freeze.py
```

## ファイル構成

| パス | 役割 |
|------|------|
| `content/posts/*.md` | ブログ記事（Obsidianで編集） |
| `content/templates/` | Obsidianのノートテンプレート |
| `content/assets/` | 画像などの添付ファイル |
| `app.py` | Flaskアプリ（`load_post()`, `get_posts()`, ルート定義） |
| `freeze.py` | Frozen-Flask ビルドスクリプト |
| `ogp.py` | OGP画像生成（`make_ogp()`, `generate_for_posts()`） |
| `templates/*.html` | Jinja2 HTMLテンプレート（base/index/post/tag/search） |
| `static/css/style.css` | スタイルシート |
| `static/js/search.js` | 検索UI（インデックスのlazy fetch・絞り込み・結果描画） |
| `static/ogp/<slug>.png` | 生成されたOGP画像（1200×630px） |
| `build/` | 生成済み静的HTML（gitignore済み、直接編集しない） |

## 投稿のフロントマター仕様

```yaml
title: string       # タイトル（必須）、OGP画像のメインテキストにも使用
date: YYYY-MM-DD    # 公開日（必須、クォートなし）
tags: list          # タグ一覧（任意）
summary: string     # 概要（一覧ページ・OGP画像・meta descriptionに使用、任意）
draft: bool         # true で非公開（デフォルト: false）
```

## 環境変数

| 変数 | 説明 | デフォルト |
|------|------|-----------|
| `SITE_URL` | サイトのURL（OGPのog:image等の絶対URL生成に必要） | 空（OGP URLなし） |
| `SITE_NAME` | サイト名（ヘッダー・OGP画像・og:site_nameに使用） | `My Blog` |

Cloudflare Pagesのビルド設定でこれらを環境変数として設定すること。

## デプロイ（GitHub + Cloudflare Pages・無料）

Cloudflare Pagesのビルド設定：

- Build command: `pip install -r requirements.txt && python freeze.py`
- Build output directory: `build`
- 環境変数 `SITE_URL`: `https://<project>.pages.dev`

mainブランチへのpushで自動デプロイ。

## 注意事項

- `build/` は生成物のため直接編集しない
- `static/ogp/` も生成物だが、ローカル確認用にcommitしてもよい
- Obsidianのwikilink（`[[slug|テキスト]]`）は `convert_wikilinks()` で `/posts/slug/` へ自動変換される
- `date` フィールドはYAML日付形式（クォートなし: `2026-01-01`）で記述すること
- 新しいルートを追加した場合は `freeze.py` にジェネレーターも追加すること

## 検索

`/search/` ページでサイト内検索できる。インデックス（`/search-index.json`）は検索ボタンを押したときに初めてfetchされる（ページ読み込み時は取得しない）。検索対象はタイトル・summary・タグ（部分一致）。`/search/` と `/search-index.json` はパラメータなしのルートなので Frozen-Flask が自動で静的ファイルを生成する。

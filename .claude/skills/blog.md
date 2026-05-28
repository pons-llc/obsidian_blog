---
name: blog
description: ObsidianとFlask-Frozenを使ったブログの執筆・管理・ビルドワークフロー。新規投稿作成、ローカルプレビュー、静的ファイル生成（OGP画像含む）を案内する。
---

ユーザーがブログの投稿作成・編集・ビルド・プレビューを行いたいと言ったら、以下のワークフローに従え。

# ブログワークフロー

プロジェクトルート: `/Users/tatsurohatori/Documents/blogtemplate/`

## 操作別手順

### 新規投稿の作成

1. タイトルを確認（未指定なら聞く）
2. スラッグ（ファイル名）を生成: 英小文字とハイフンに変換 or 日付ベース（`2026-05-28-topic`）
3. `content/posts/<slug>.md` を以下のフォーマットで作成:

```yaml
---
title: <タイトル>
date: <今日の日付 YYYY-MM-DD>
tags:
  - <関連タグ>
summary: <1〜2文の概要（OGP画像とmeta descriptionにも使われる）>
draft: false
---

<内容をここに記述>
```

4. 作成後、Obsidianで開く場合は `content/` フォルダをvaultとして開くよう案内する

### ローカルプレビュー

```bash
uv run python app.py
```

→ `http://localhost:5000` でプレビュー確認。起動時にOGP画像も自動生成される。

### 静的ファイルのビルド（OGP画像含む）

```bash
SITE_URL=https://yourblog.pages.dev uv run python freeze.py
```

→ `build/` に静的HTMLを生成。`static/ogp/<slug>.png` にOGP画像を生成。

### 投稿一覧の確認

`content/posts/` 内の `.md` ファイルを一覧表示し、タイトル・日付・タグ・下書き状態を整理して表示する。

### 既存投稿の編集

1. スラッグまたはタイトルで対象ファイルを特定
2. フロントマターと本文を確認してから編集
3. `draft: true` にすると非公開（ビルド対象外）

## フロントマター仕様

| フィールド | 型           | 説明                                    |
|-----------|-------------|---------------------------------------|
| title     | string      | タイトル（必須）、OGP画像のメインテキストにも使用 |
| date      | YYYY-MM-DD  | 公開日（必須、クォートなし）                  |
| tags      | list        | タグ一覧（任意）                            |
| summary   | string      | 概要（一覧・OGP・meta description用、任意）  |
| draft     | bool        | true で非公開（デフォルト: false）           |

## 環境変数

| 変数 | 説明 |
|------|------|
| `SITE_URL` | サイトURL（例: `https://yourblog.pages.dev`）。OGPのog:imageに絶対URLが入る。 |
| `SITE_NAME` | サイト名（デフォルト: `My Blog`）。ヘッダーとOGP画像に表示される。 |

## ファイル構成

```
content/posts/       ← Obsidianで編集するMarkdownファイル
content/templates/   ← Obsidianの新規投稿テンプレート
templates/           ← Jinja2 HTMLテンプレート（base/index/post/tag）
static/css/          ← スタイルシート
static/ogp/          ← 生成されたOGP画像（1200×630px、自動生成）
ogp.py               ← OGP画像生成モジュール（Pillow使用、日本語フォント対応）
app.py               ← Flaskアプリ（ローカルプレビュー用）
freeze.py            ← 静的ファイル生成スクリプト
build/               ← 生成された静的HTML（デプロイ対象、gitignore済み）
```

## デプロイ（GitHub + Cloudflare Pages・無料）

Cloudflare Pagesのビルド設定：
- Build command: `pip install -r requirements.txt && python freeze.py`
- Build output directory: `build`
- 環境変数 `SITE_URL`: `https://<project>.pages.dev`

mainブランチへのpushで自動デプロイ。

## よくある問題

- **OGP画像が生成されない**: Pillowが未インストール → `uv pip install Pillow`
- **OGP画像のURLが空**: `SITE_URL` 環境変数が未設定 → ビルド時に指定する
- **ビルド後にリンク切れ**: `freeze.py` の `FREEZER_RELATIVE_URLS = True` を確認
- **日付が表示されない**: フロントマターの日付はクォートなしのYAML日付形式（`2026-01-01`）で記述
- **Obsidianのwikilink (`[[link]]`) が機能しない**: `[text](url)` 形式を使う
- **新しい投稿がビルドされない**: `draft: false` になっているか確認


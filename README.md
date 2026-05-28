# blogtemplate

ObsidianとFlask-Frozenを組み合わせた静的ブログ。
Claude Codeのスキルで投稿作成やデザイン変更もできる。

---

## Obsidianで書くメリット

ブログ記事はすべて `content/posts/` のMarkdownファイル。
`content/` フォルダをObsidianのvaultとして開くだけで、そのまま執筆環境になる。

- **プロパティパネル** — タグ・日付・下書き状態をGUI操作できる
- **テンプレート** — 「テンプレートの挿入」コマンドで `新規投稿.md` を呼び出すとフロントマターを自動入力
- **タグ・バックリンク** — 記事間の関連をObsidian上で管理できる
- **ローカル完結** — クラウド不要、ファイルはすべて手元に残る
- **プレビュー** — Obsidianのプレビューモードで見た目を確認しながら書ける

---

## Claude Code スキルの使い方

このプロジェクトには2つのスキルが含まれている。
Claude Codeをプロジェクトルートで開いて呼び出す。

### `/blog` — 投稿管理

新規投稿・ビルド・プレビューをサポート。

```
/blog 新しい記事を書きたい
/blog 下書き一覧を見せて
/blog ビルドして
```

### `/design` — デザインカスタマイズ

好みを聞きながら `style.css` をカスタマイズ。
ミニマル・テックダーク・温かみのある雰囲気など、インタラクティブに仕上げていける。

```
/design
```

---

## サイト内検索

ヘッダーの「検索」リンクからサイト内検索ができる。
検索インデックスはボタンを押したときに初めて読み込まれるので、他のページの表示速度に影響しない。タイトル・概要・タグを対象に部分一致で絞り込む。

---

## セットアップ

```bash
# 依存インストール
uv pip install -r requirements.txt

# ローカルプレビュー（http://localhost:5000）
uv run python app.py

# 静的ファイル生成
SITE_URL=https://yourblog.pages.dev uv run python freeze.py
```

---

## デプロイ（GitHub + Cloudflare Pages・無料）

1. GitHubにpush
2. Cloudflare Pagesで「Connect to Git」
3. ビルド設定を入力：

| 項目 | 値 |
|------|----|
| Build command | `pip install -r requirements.txt && python freeze.py` |
| Build output directory | `build` |
| 環境変数 `SITE_URL` | `https://<project>.pages.dev` |
| 環境変数 `SITE_NAME` | ブログ名（任意） |

mainへのpushで自動デプロイ。カスタムドメインも無料で追加できる。

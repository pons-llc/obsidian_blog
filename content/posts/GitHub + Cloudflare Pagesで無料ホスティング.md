---
order: 5
title: GitHub + Cloudflare Pagesで無料ホスティング
slug: free-hosting-cloudflare-pages
date: 2026-05-24
tags:
  - デプロイ
  - Cloudflare
summary: GitHubにpushするだけで自動ビルド・デプロイ。Cloudflare Pagesなら帯域無制限・無料で運用できる。
draft: false
---

静的サイトのホスティングには Cloudflare Pages を使っている。無料で使えて、速くて、設定が少ない。[[Flask-Frozenが静的サイト生成に意外と向いている|Flask-Frozenで生成した]]静的ファイルをそのままデプロイできる。

## 設定は3ステップ

1. GitHub にリポジトリを作って push する
2. Cloudflare Pages で「Connect to Git」でリポジトリを選ぶ
3. ビルド設定を入力する：

| 項目 | 値 |
|------|-----|
| Build command | `pip install -r requirements.txt && python freeze.py` |
| Output directory | `build` |
| 環境変数 `SITE_URL` | `https://<project>.pages.dev` |

以上。`main` ブランチへの push が自動でビルドとデプロイをトリガーする。

## 無料でここまでできる

- **帯域無制限**（Netlify は月100GBまで）
- **毎月500ビルド**（個人ブログには十分すぎる）
- **カスタムドメイン**（SSL証明書も自動）
- **Cloudflare のCDN**（世界中のエッジから配信）

個人ブログを運用するのにお金がかからない。この構成でコストがかかるのはドメイン代だけだ。

## OGP画像もビルド時に自動生成される

`python freeze.py` を実行すると、記事のタイトルと概要から OGP 画像（1200×630px）が自動生成される。SNS でシェアされたときに記事ごとのサムネイルが表示される。

Cloudflare Pages のビルドで `SITE_URL` を環境変数に設定しておけば、OGP タグに絶対 URL が埋め込まれてシェア時に正しく機能する。

## Obsidian → GitHub → Cloudflare の流れ

1. Obsidian で記事を書く
2. `git commit && git push`
3. Cloudflare Pages が自動でビルド・デプロイ

記事の公開にかかる手動作業は git push だけ。記事の作成は[[ObsidianをCMSとして使う|Obsidian]]で、[[Claude CodeのスキルでブログをAIアシスタントと一緒に管理する|Claude Codeのスキル]]でサポートしてもらっている。

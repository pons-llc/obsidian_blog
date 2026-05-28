---
order: 6
title: Cloudflareでカスタムドメインを設定する
slug: custom-domain-cloudflare
date: 2026-05-25
tags:
  - デプロイ
  - Cloudflare
summary: Cloudflare Pagesに独自ドメインを設定する手順。DNS設定からSSL証明書の自動発行まで無料でできる。
draft: false
---

[[GitHub + Cloudflare Pagesで無料ホスティング|Cloudflare Pagesでブログを公開]]したら、次は独自ドメインを設定したい。手順は少なく、SSL証明書も自動で発行される。

## 必要なもの

- 取得済みのドメイン（お名前.com、Cloudflare Registrar、Namecheapなど）
- Cloudflare Pagesにデプロイ済みのブログ

## 手順

### 1. Cloudflare Pagesの管理画面を開く

対象のプロジェクトを選び、「Custom domains」タブを開く。
「Set up a custom domain」をクリックしてドメインを入力する。

### 2. DNSを設定する

ドメインをどこで管理しているかによって設定方法が変わる。

**Cloudflareでドメインを管理している場合（推奨）**

Cloudflareが自動的にDNSレコードを追加してくれる。確認して有効化するだけ。

**他のレジストラでドメインを管理している場合**

CNAMEレコードを追加する：

| 種別 | 名前 | 値 |
|------|------|----|
| CNAME | `@` または `www` | `<project>.pages.dev` |

ルートドメイン（`example.com`）にCNAMEが設定できないレジストラの場合は、ネームサーバーをCloudflareに移管するのが最もスムーズ。

### 3. SSL証明書の発行を待つ

DNS設定が反映されると（数分〜24時間）、Cloudflareが自動的にSSL証明書を発行する。
ステータスが「Active」になれば完了。

## SITE_URLを更新する

カスタムドメインが有効になったら、Cloudflare Pagesのビルド設定で環境変数を更新する。

```
SITE_URL = https://yourdomain.com
```

次のビルド時から、OGP画像のURLやsitemapに正しいドメインが反映される。

## www ありとなし

`www.yourdomain.com` と `yourdomain.com` の両方を設定できる。どちらをメインにするかを決めて、もう一方はリダイレクトに設定すると良い。Cloudflare Pagesは両方設定しておけば自動でどちらも処理してくれる。

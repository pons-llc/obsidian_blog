---
order: 8
title: Google AdSenseに申請する方法
slug: google-adsense-application
date: 2026-05-27
tags:
  - 運営
  - 収益化
summary: 静的ブログでのAdSense申請手順。ads.txtの設置方法と審査を通過するためのポイント。
draft: false
---

ブログをある程度書いたら収益化を考えたい。Google AdSenseは審査制だが、静的ブログでも問題なく申請できる。

## 申請前に確認すること

審査を通過しやすくするための前提条件：

- **記事数**: 最低10〜20記事程度が目安
- **オリジナルコンテンツ**: コピーコンテンツは不可
- **プライバシーポリシー**: [[プライバシーポリシーの作り方と設置方法|設置が必須]]
- **お問い合わせページ**: あるとベター
- **独自ドメイン**: [[Cloudflareでカスタムドメインを設定する|カスタムドメイン]]があると審査が通りやすい

## 申請手順

1. [Google AdSense](https://www.google.com/adsense/) にアクセスしてアカウントを作成
2. サイトのURLを入力（`https://yourdomain.com`）
3. AdSenseコードを `<head>` に貼り付ける
4. 審査完了を待つ（数日〜数週間）

## AdSenseコードの設置

`templates/base.html` の `<head>` 内に貼り付ける：

```html
<!-- Google AdSense -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXX"
     crossorigin="anonymous"></script>
```

`XXXXXXXXXX` の部分はAdSenseの管理画面で発行されたパブリッシャーIDに置き換える。

## ads.txtの設置

AdSenseは `ads.txt` ファイルをサイトのルートに設置することを要求する。
`https://yourdomain.com/ads.txt` にアクセスできる必要がある。

`static/ads.txt` を作成し、AdSenseの管理画面に表示される内容を貼り付ける：

```
google.com, pub-XXXXXXXXXX, DIRECT, f08c47fec0942fa0
```

Frozen-Flask は `static/` 内のファイルをそのまま `build/` にコピーするので、`static/ads.txt` に置けば `https://yourdomain.com/ads.txt` として公開される。

## 審査中・審査後

審査中はAdSenseコードを貼っていても広告は表示されない。審査通過後に広告の種類と配置を設定できる。

静的サイトなので自動広告（Auto Ads）が最もシンプル。コード1行で最適な場所に自動配置してくれる。

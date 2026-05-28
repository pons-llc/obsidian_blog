---
order: 1
title: ObsidianとFlask-Frozenでブログを作った理由
slug: why-obsidian-flask-blog
date: 2026-05-01
tags:
  - ブログ
  - 構成
summary: WordPressでも静的サイトジェネレーターでもなく、ObsidianとFlask-Frozenの組み合わせを選んだ理由を整理した。
draft: false
---

ブログを始めようと思ったとき、選択肢はたくさんある。WordPressのような動的CMS、HugoやJekyllのような静的サイトジェネレーター、あるいはNotionやSubstackのようなサービス。

なぜこの構成にしたかを一言で言うと、**書くこととデプロイすることを完全に分離したかった**から。

## 書く環境にこだわりたかった

Obsidianは現在もっとも使い込んでいるツールだ。日々のメモ、アイデアの整理、読書ノート。ノートを書く環境としてはすでに最高の状態になっている。

ブログもそこで書けるなら、新しいエディタに慣れる必要がない。記事のアイデアが日常のメモから自然に育っていく。[[ObsidianをCMSとして使う|ObsidianをCMSとして使う方法]]はまた別に書いた。

## Markdownファイルがそのまま資産になる

WordPressはデータベースにコンテンツが閉じ込められる。サービス依存のブログはプラットフォームが変わると消える。

このブログの記事は全部 `content/posts/` の `.md` ファイルだ。Git管理できるし、エディタを変えてもそのまま使える。10年後もファイルとして手元に残る。

## Flask-Frozenで「普通のPythonコード」として扱える

HugoやJekyllは独自のテンプレートエンジンや設定ファイルを覚える必要がある。Flask-Frozenはただのフラスコアプリをフリーズするだけ。Pythonを知っていれば、ロジックを自由に書ける。

タグ一覧のソート順を変えたい、特定のカテゴリだけRSSを出したい。そういうカスタマイズがPythonのコードとして書けるのは大きい。[[Flask-Frozenが静的サイト生成に意外と向いている|Flask-Frozenの詳細]]はこちら。

---

完璧な構成ではないかもしれないが、自分の使い方に素直に合わせた結果がこれだ。ホスティングは[[GitHub + Cloudflare Pagesで無料ホスティング|GitHub + Cloudflare Pages]]で無料で運用している。記事の作成やデザイン変更は[[Claude CodeのスキルでブログをAIアシスタントと一緒に管理する|Claude Codeのスキル]]で行っている。

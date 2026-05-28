---
name: design
description: ブログのデザインをインタラクティブにカスタマイズする。好みを聞いてCSS・テンプレートを変更し、プレビューしながら仕上げる。
---

ユーザーがブログのデザインを変えたい・カスタマイズしたいと言ったら、以下のワークフローを実行せよ。

# デザインカスタマイズワークフロー

## STEP 1: ヒアリング

以下の質問を**AskUserQuestion ツールで一度に聞く**（最大4問）。
すでに明らかな情報はスキップしてよい。

### 聞くこと

1. **ブログの用途・テーマ**（ブログの性格を掴む）
   - 技術ブログ（コード多め）
   - 日記・エッセイ（読み物中心）
   - 写真・ビジュアル重視
   - ニュース・マガジン風

2. **全体の雰囲気**
   - ミニマル（余白多め、装飾なし）
   - エレガント（細いフォント、洗練）
   - テック・ハッカー（ダーク背景、コード映え）
   - 温かみ（セリフ体、ベージュ・クリーム系）
   - カラフル・ポップ

3. **カラースキーム**
   - ライト固定 / ダーク固定 / OS設定に合わせる（auto）

4. **フォント方針**
   - システムフォントのみ（軽量・高速）
   - Google Fontsを使う（Noto Sans JP 等）
   - セリフ体（読み物向け）

---

## STEP 2: デザイン案の提示

ヒアリング結果から具体的な設計を提案する。変更前に必ず以下を説明する：

- 背景色 / テキスト色 / アクセントカラー（カラーコード）
- フォント名
- レイアウト幅
- 追加する特徴（カード、ボーダー、影など）

「このデザインで適用しますか？」と確認してから実行する。

---

## STEP 3: CSS の適用

`static/css/style.css` を**CSS変数ベースで書き直す**。

### 必須の CSS 変数定義（`:root` に）

```css
:root {
  --bg:        /* 背景色 */;
  --bg-sub:    /* カード・コードブロック背景 */;
  --text:      /* 本文色 */;
  --muted:     /* 補助テキスト（日付・タグ等） */;
  --accent:    /* リンク・アクセント色 */;
  --border:    /* 区切り線 */;
  --max-w:     /* コンテンツ最大幅 */;
  --font:      /* 本文フォント */;
  --font-mono: /* コードフォント */;
  --base-size: /* 基本フォントサイズ */;
  --line-h:    /* 行間 */;
  --radius:    /* カード角丸 */;
}
```

### Google Fonts を使う場合

`templates/base.html` の `<head>` に `<link>` タグを追加する。

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap" rel="stylesheet">
```

### ダークモード（auto）の場合

```css
@media (prefers-color-scheme: dark) {
  :root {
    --bg: /* ダーク背景 */;
    /* ... */
  }
}
```

### OGP画像の色も合わせる場合

`ogp.py` の `BG` と `ACCENT` 定数を更新する。

---

## STEP 4: プレビュー

変更後に以下を実行してプレビューを促す：

```bash
uv run python app.py
```

→ `http://localhost:5000` を開いて確認してもらう。

---

## STEP 5: 反復修正

「もっと余白を広く」「色をもう少し明るく」「フォントサイズを大きく」などの追加要望に対して
**CSS変数の値だけ変えれば済む変更は変数のみ修正**し、構造的な変更が必要な場合はセクションを書き換える。

---

# デザインパターン集（参考）

## ミニマルライト（デフォルト的な清潔感）

```css
:root {
  --bg: #ffffff;
  --bg-sub: #f8f9fa;
  --text: #1a1a1a;
  --muted: #6b7280;
  --accent: #2563eb;
  --border: #e5e7eb;
  --max-w: 700px;
  --font: -apple-system, BlinkMacSystemFont, 'Noto Sans JP', sans-serif;
  --font-mono: 'SF Mono', Consolas, monospace;
  --base-size: 17px;
  --line-h: 1.85;
  --radius: 6px;
}
```

## テックダーク（GitHub風、コード多めのブログ向け）

```css
:root {
  --bg: #0d1117;
  --bg-sub: #161b22;
  --text: #e6edf3;
  --muted: #8b949e;
  --accent: #58a6ff;
  --border: #30363d;
  --max-w: 820px;
  --font: -apple-system, BlinkMacSystemFont, 'Noto Sans JP', sans-serif;
  --font-mono: 'SF Mono', ui-monospace, 'Cascadia Code', monospace;
  --base-size: 16px;
  --line-h: 1.75;
  --radius: 6px;
}
```

## 温かみ・エッセイ（日記・読み物向け）

```css
:root {
  --bg: #fdf8f0;
  --bg-sub: #f3ede0;
  --text: #3c3836;
  --muted: #928374;
  --accent: #c77b3f;
  --border: #e8dece;
  --max-w: 680px;
  --font: 'Georgia', 'Noto Serif JP', 'YuMincho', serif;
  --font-mono: 'SF Mono', Consolas, monospace;
  --base-size: 18px;
  --line-h: 1.9;
  --radius: 4px;
}
```

## エレガントダーク（ポートフォリオ・洗練）

```css
:root {
  --bg: #111111;
  --bg-sub: #1a1a1a;
  --text: #f0f0f0;
  --muted: #888888;
  --accent: #d4a853;
  --border: #2a2a2a;
  --max-w: 760px;
  --font: 'Helvetica Neue', 'Noto Sans JP', sans-serif;
  --font-mono: 'Courier New', monospace;
  --base-size: 16px;
  --line-h: 1.8;
  --radius: 2px;
}
```

---

# 注意事項

- 既存の `style.css` 全体を書き換える場合も、CSS変数は必ず最初に定義する
- フォントサイズや行間は日本語読みやすさを優先（最低16px、行間1.7以上）
- アクセントカラーはリンク・タグ・ボーダーに一貫して使う
- コントラスト比は 4.5:1 以上を維持する（WCAG AA 基準）


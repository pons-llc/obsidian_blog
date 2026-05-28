import glob
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
ACCENT = (99, 102, 241)
BG = (22, 27, 46)


def _find_font(size):
    candidates = (
        glob.glob("/System/Library/Fonts/ヒラギノ角ゴシック W*.ttc")
        + glob.glob("/System/Library/Fonts/Hiragino*.ttc")
        + [
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        ]
    )
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _wrap(draw, text, font, max_w):
    lines, cur = [], ""
    for ch in text:
        test = cur + ch
        if draw.textbbox((0, 0), test, font=font)[2] > max_w and cur:
            lines.append(cur)
            cur = ch
        else:
            cur = test
    if cur:
        lines.append(cur)
    return lines


def make_ogp(title, summary="", site_name="My Blog"):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, W, 6], fill=ACCENT)

    f_sm = _find_font(26)
    d.text((80, 56), site_name, font=f_sm, fill=(160, 160, 200))

    f_lg = _find_font(62)
    y = 160
    for line in _wrap(d, title, f_lg, 1040)[:3]:
        d.text((80, y), line, font=f_lg, fill=(255, 255, 255))
        y += 84

    if summary:
        f_md = _find_font(30)
        y = max(y + 30, 480)
        for line in _wrap(d, summary, f_md, 1040)[:2]:
            d.text((80, y), line, font=f_md, fill=(160, 160, 190))
            y += 42

    d.rectangle([0, H - 4, W, H], fill=ACCENT)
    return img


def generate_for_posts(posts, output_dir, site_name="My Blog"):
    os.makedirs(output_dir, exist_ok=True)
    for post in posts:
        img = make_ogp(post["title"], post.get("summary", ""), site_name)
        img.save(os.path.join(output_dir, f"{post['slug']}.png"), "PNG", optimize=True)
    print(f"OGP images generated: {len(posts)} files → {output_dir}/")

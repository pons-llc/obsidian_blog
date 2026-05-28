import glob
import os
import re
from datetime import date

import frontmatter
import markdown as md
from flask import Flask, Response, jsonify, render_template, send_from_directory
from markupsafe import Markup

app = Flask(__name__)
app.config['SITE_NAME'] = os.environ.get('SITE_NAME', 'My Blog')
app.config['SITE_URL'] = os.environ.get('SITE_URL', '')

POSTS_DIR = os.path.join(os.path.dirname(__file__), 'content', 'posts')


def _get_slug_map():
    result = {}
    for fp in glob.glob(os.path.join(POSTS_DIR, '*.md')):
        p = frontmatter.load(fp)
        fn = os.path.splitext(os.path.basename(fp))[0]
        result[fn] = p.get('slug', fn)
    return result


def convert_wikilinks(text, slug_map):
    def repl_piped(m):
        slug = slug_map.get(m.group(1).strip(), m.group(1).strip())
        return f'[{m.group(2).strip()}](/posts/{slug}/)'

    def repl_plain(m):
        ref = m.group(1).strip()
        slug = slug_map.get(ref, ref)
        return f'[{ref}](/posts/{slug}/)'

    text = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', repl_piped, text)
    text = re.sub(r'\[\[([^\]|]+)\]\]', repl_plain, text)
    return text


def load_post(filepath):
    post = frontmatter.load(filepath)
    filename = os.path.splitext(os.path.basename(filepath))[0]
    slug = post.get('slug') or filename
    post_date = post.get('date', None)
    if isinstance(post_date, str):
        try:
            post_date = date.fromisoformat(post_date)
        except ValueError:
            post_date = None
    return {
        'slug': slug,
        'title': post.get('title', slug),
        'date': post_date,
        'tags': post.get('tags', []),
        'summary': post.get('summary', ''),
        'draft': post.get('draft', False),
        'order': post.get('order', None),
        'content': Markup(md.markdown(convert_wikilinks(post.content, _get_slug_map()), extensions=['fenced_code', 'tables', 'toc']))
    }


def get_posts(include_drafts=False):
    posts = []
    for filepath in glob.glob(os.path.join(POSTS_DIR, '*.md')):
        p = load_post(filepath)
        if not p['draft'] or include_drafts:
            posts.append(p)
    return sorted(posts, key=lambda p: (
        p['order'] if p['order'] is not None else 9999,
        -(p['date'].toordinal() if p['date'] else 0)
    ))


@app.route('/')
def index():
    return render_template('index.html', posts=get_posts())


def find_post_filepath(slug):
    for fp in glob.glob(os.path.join(POSTS_DIR, '*.md')):
        p = frontmatter.load(fp)
        fn = os.path.splitext(os.path.basename(fp))[0]
        if p.get('slug', fn) == slug:
            return fp
    return None


@app.route('/posts/<slug>/')
def post(slug):
    filepath = find_post_filepath(slug)
    if filepath is None:
        return 'Not found', 404
    return render_template('post.html', post=load_post(filepath))


@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'content', 'assets'), filename)


@app.route('/sitemap.xml')
def sitemap():
    posts = get_posts()
    tags = sorted({t for p in posts for t in p.get('tags', [])})
    base = app.config.get('SITE_URL', '').rstrip('/')
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        f'  <url><loc>{base}/</loc></url>',
    ]
    for p in posts:
        lm = f'<lastmod>{p["date"]}</lastmod>' if p['date'] else ''
        lines.append(f'  <url><loc>{base}/posts/{p["slug"]}/</loc>{lm}</url>')
    for t in tags:
        lines.append(f'  <url><loc>{base}/tags/{t}/</loc></url>')
    lines.append(f'  <url><loc>{base}/search/</loc></url>')
    lines.append('</urlset>')
    return Response('\n'.join(lines), mimetype='application/xml')


@app.route('/search/')
def search():
    return render_template('search.html')


@app.route('/search-index.json')
def search_index():
    return jsonify([{
        'slug': p['slug'],
        'title': p['title'],
        'date': p['date'].isoformat() if p['date'] else '',
        'tags': p['tags'],
        'summary': p['summary'],
    } for p in get_posts()])


@app.route('/tags/<tag>/')
def tag(tag):
    posts = [p for p in get_posts() if tag in p.get('tags', [])]
    return render_template('tag.html', tag=tag, posts=posts)


if __name__ == '__main__':
    try:
        import ogp
        ogp.generate_for_posts(
            get_posts(),
            os.path.join(os.path.dirname(__file__), 'static', 'ogp'),
            site_name=app.config['SITE_NAME'],
        )
    except ImportError:
        print('Pillow not installed, skipping OGP images. Run: pip install Pillow')
    app.run(debug=True)

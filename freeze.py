import glob
import os

from flask_frozen import Freezer

from app import app, get_posts

app.config['FREEZER_DESTINATION'] = 'build'
app.config['FREEZER_RELATIVE_URLS'] = True
app.config['SITE_URL'] = os.environ.get('SITE_URL', '')
app.config['SITE_NAME'] = os.environ.get('SITE_NAME', 'My Blog')

freezer = Freezer(app)


@freezer.register_generator
def post():
    for p in get_posts():
        yield {'slug': p['slug']}


@freezer.register_generator
def assets():
    assets_dir = os.path.join('content', 'assets')
    if os.path.isdir(assets_dir):
        for fp in glob.glob(os.path.join(assets_dir, '**', '*'), recursive=True):
            if os.path.isfile(fp):
                yield {'filename': os.path.relpath(fp, assets_dir)}


@freezer.register_generator
def tag():
    tags = set()
    for p in get_posts():
        tags.update(p.get('tags', []))
    for t in tags:
        yield {'tag': t}


if __name__ == '__main__':
    try:
        import ogp
        ogp.generate_for_posts(
            get_posts(),
            os.path.join('static', 'ogp'),
            site_name=app.config['SITE_NAME'],
        )
    except ImportError:
        print('Pillow not installed, skipping OGP images. Run: pip install Pillow')

    freezer.freeze()
    print('Build complete! Static files in ./build/')

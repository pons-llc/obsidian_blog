(function () {
  const app     = document.getElementById('search-app');
  const input   = document.getElementById('search-input');
  const button  = document.getElementById('search-button');
  const status  = document.getElementById('search-status');
  const results = document.getElementById('search-results');
  const INDEX_URL = app.dataset.indexUrl;

  let index = null;

  async function loadIndex() {
    if (index) return true;
    status.textContent = '読み込み中...';
    button.disabled = true;
    try {
      const res = await fetch(INDEX_URL);
      if (!res.ok) throw new Error(res.status);
      index = await res.json();
      status.textContent = '';
      return true;
    } catch {
      status.textContent = '検索インデックスの読み込みに失敗しました。';
      return false;
    } finally {
      button.disabled = false;
    }
  }

  function doSearch(query) {
    const q = query.toLowerCase();
    return index.filter(p =>
      p.title.toLowerCase().includes(q) ||
      p.summary.toLowerCase().includes(q) ||
      p.tags.some(t => t.toLowerCase().includes(q))
    );
  }

  function esc(str) {
    return String(str)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function render(hits, query) {
    if (!hits.length) {
      results.innerHTML = `<p class="search-empty">「${esc(query)}」に一致する記事が見つかりませんでした。</p>`;
      return;
    }
    const items = hits.map(p => {
      const tags = p.tags.length
        ? `<span class="tags">${p.tags.map(t => `<a href="../tags/${esc(t)}/" class="tag">${esc(t)}</a>`).join('')}</span>`
        : '';
      return `<li class="post-item">
        <a href="../posts/${esc(p.slug)}/">${esc(p.title)}</a>
        ${p.date ? `<time>${esc(p.date)}</time>` : ''}
        ${tags}
        ${p.summary ? `<p class="summary">${esc(p.summary)}</p>` : ''}
      </li>`;
    }).join('');
    results.innerHTML = `<p class="search-count">${hits.length}件見つかりました</p><ul class="post-list">${items}</ul>`;
  }

  async function run() {
    const query = input.value.trim();
    if (!query) return;
    const ok = await loadIndex();
    if (ok) render(doSearch(query), query);
  }

  button.addEventListener('click', run);
  input.addEventListener('keydown', e => { if (e.key === 'Enter') run(); });
})();

(async function () {
  const res = await fetch('../data/wine-academy.json');
  const data = await res.json();
  const grid = document.getElementById('styleGrid');
  const filtersEl = document.getElementById('filters');
  const search = document.getElementById('styleSearch');
  const shown = document.getElementById('shownCount');
  document.getElementById('styleCount').textContent = data.styleCount.toLocaleString();
  document.getElementById('subCount').textContent = data.subgenreCount;

  let active = 'All';
  const filters = ['All', ...data.subgenres];
  filters.forEach((name) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'filter-btn';
    b.textContent = name;
    b.setAttribute('aria-pressed', name === 'All' ? 'true' : 'false');
    b.addEventListener('click', () => {
      active = name;
      filtersEl.querySelectorAll('.filter-btn').forEach((x) =>
        x.setAttribute('aria-pressed', x.textContent === active ? 'true' : 'false')
      );
      render();
    });
    filtersEl.appendChild(b);
  });

  function render() {
    const q = (search.value || '').trim().toLowerCase();
    const list = data.styles.filter((s) => {
      if (active !== 'All' && s.subgenre !== active) return false;
      if (!q) return true;
      return (
        s.name.toLowerCase().includes(q) ||
        s.subgenre.toLowerCase().includes(q) ||
        (s.parent || '').toLowerCase().includes(q)
      );
    });
    shown.textContent = `Showing ${list.length.toLocaleString()} of ${data.styleCount.toLocaleString()} styles`;
    grid.innerHTML = '';
    const frag = document.createDocumentFragment();
    // Cap DOM for very large filtered "All" with no search: still show all 392 — fine for preview
    list.forEach((s) => {
      const el = s.slug ? document.createElement('a') : document.createElement('div');
      el.className = 'style-card' + (s.slug ? ' is-link' : '');
      if (s.slug) el.href = '../encyclopedia/' + s.slug + '.html';
      el.innerHTML =
        '<div class="sg">' +
        escapeHtml(s.subgenre) +
        '</div><h3>' +
        escapeHtml(s.name) +
        '</h3>' +
        (s.definition
          ? '<p>' + escapeHtml(s.definition) + '</p>'
          : '');
      frag.appendChild(el);
    });
    grid.appendChild(frag);
  }

  function escapeHtml(t) {
    return String(t)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  search.addEventListener('input', render);
  render();
})();

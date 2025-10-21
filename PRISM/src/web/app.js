./src/web/app.js - v1.0.0

const API = (window.API_BASE_URL || 'http://localhost:8000');

document.getElementById('query-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const q = document.getElementById('q').value;
  const type = document.getElementById('type').value;
  const tag = document.getElementById('tag').value;
  const params = new URLSearchParams();
  if (q) params.set('q', q);
  if (type) params.set('type', type);
  if (tag) params.set('tag', tag);
  const res = await fetch(`${API}/query?${params.toString()}`);
  const data = await res.json();
  document.getElementById('results').textContent = JSON.stringify(data, null, 2);
});

document.getElementById('classify-btn').addEventListener('click', async () => {
  const title = document.getElementById('title').value;
  const body = document.getElementById('body').value;
  const payload = { items: [{ title, body }] };
  const res = await fetch(`${API}/classify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  document.getElementById('classify-out').textContent = JSON.stringify(data, null, 2);
});

EOF ./src/web/app.js - v1.0.0
# 修正履歴:
# - 2025-10-20 v1.0.0: Web から API を叩く最小スクリプト


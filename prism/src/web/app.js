// ./src/web/app.js - v1.0.0
(function () {
  const $ = (id) => document.getElementById(id);

  async function query() {
    const apiBase = $("apiBase").value || "http://localhost:8000";
    const apiKey = $("apiKey").value || "dev-key-change-me";
    const type = $("qType").value.trim();
    const tag = $("qTag").value.trim();
    const start = $("qStart").value.trim();
    const end = $("qEnd").value.trim();
    const params = new URLSearchParams();
    if (type) params.set("type", type);
    if (tag) params.set("tag", tag);
    if (start) params.set("start", start);
    if (end) params.set("end", end);

    const res = await fetch(`${apiBase}/query?${params.toString()}`, {
      headers: { "x-api-key": apiKey },
    });
    const data = await res.json();
    const list = $("results");
    list.innerHTML = "";
    (data.results || []).forEach((r) => {
      const li = document.createElement("li");
      li.textContent = `${r.type} | ${r.title || ""} | [${(r.tags || []).join(", ")}]`;
      list.appendChild(li);
    });
  }

  async function classify() {
    const apiBase = $("apiBase").value || "http://localhost:8000";
    const apiKey = $("apiKey").value || "dev-key-change-me";
    const text = $("note").value;
    const payload = { items: [{ title: text.split("\n")[0], body: text }] };
    const res = await fetch(`${apiBase}/classify`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "x-api-key": apiKey },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    $("classifyResult").textContent = JSON.stringify(data, null, 2);
  }

  $("btnQuery").addEventListener("click", query);
  $("btnClassify").addEventListener("click", classify);
})();
// EOF ./src/web/app.js - v1.0.0
// 修正履歴:
// - 2025-10-20 v1.0.0: 初版作成
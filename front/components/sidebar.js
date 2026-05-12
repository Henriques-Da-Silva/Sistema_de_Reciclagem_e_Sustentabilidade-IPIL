(function () {
  const pagina = window.location.pathname.split("/").pop() || "../pages/dashboard.html";

  const itens = [
    { href: "../pages/dashboard.html",      icone: "ti-home",        label: "Página Inicial" },
    { href: "../pages/nova_coleta.html",    icone: "ti-plus",        label: "Nova coleta" },
    { href: "../pages/history.html",        icone: "ti-history",     label: "Histórico" },
    { href: "../pages/locais_coleta.html",  icone: "ti-map-pin",     label: "Locais de coleta" },
    { href: "../pages/ranking.html",        icone: "ti-trophy",      label: "Ranking" },
    { href: "../pages/perfil.html",         icone: "ti-user",        label: "Perfil" },
  ];

  const comunidadeIdx = 4; // índice onde começa a seção "Comunidade"

  const navHTML = itens.map((item, i) => {
    const secao = i === comunidadeIdx
      ? `<div class="sidebar-section">Comunidade</div>`
      : i === 0 ? `<div class="sidebar-section">Menu</div>` : "";
    const ativo = pagina === item.href ? "active" : "";
    return `
      ${secao}
      <a href="${item.href}" class="nav-item ${ativo}">
        <i class="ti ${item.icone}" aria-hidden="true"></i>
        ${item.label}
      </a>
    `;
  }).join("");

  const html = `<aside id="app-sidebar">${navHTML}</aside>`;

  const style = `
    <style>
      body {
        display: flex;
        flex-direction: column;
        min-height: 100vh;
        margin: 0;
        font-family: 'Segoe UI', sans-serif;
        background: #F9FAFB;
        color: #212529;
      }
      #app-layout {
        display: flex;
        flex: 1;
      }
      #app-sidebar {
        width: 200px;
        background: #fff;
        border-right: 1px solid #e5e7eb;
        padding: 12px 0;
        flex-shrink: 0;
        min-height: calc(100vh - 4rem);
      }
      .sidebar-section {
        font-size: 10px;
        font-weight: 600;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        padding: 12px 16px 4px;
      }
      .nav-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 16px;
        font-size: 14px;
        color: #374151;
        text-decoration: none;
        border-left: 3px solid transparent;
        transition: background 0.15s;
      }
      .nav-item:hover {
        background: #D8F3DC;
      }
      .nav-item.active {
        background: #D8F3DC;
        color: #1B4332;
        border-left-color: #1B4332;
        font-weight: 500;
      }
      .nav-item i {
        font-size: 18px;
        opacity: 0.7;
      }
      .nav-item.active i {
        opacity: 1;
      }
      main {
        flex: 1;
        padding: 28px 32px;
      }
    </style>
  `;

  const layout = document.createElement("div");
  layout.id = "app-layout";
  while (document.body.firstChild && document.body.firstChild.id !== "app-header") {
    if (document.body.firstChild.id === "app-header") break;
    layout.appendChild(document.body.firstChild);
  }

  document.head.insertAdjacentHTML("beforeend", style);
  document.body.insertAdjacentHTML("beforeend", html);

  const main = document.querySelector("main");
  if (main) {
    const appLayout = document.getElementById("app-layout") || document.createElement("div");
    appLayout.id = "app-layout";
    document.body.appendChild(appLayout);
    appLayout.appendChild(document.getElementById("app-sidebar"));
    appLayout.appendChild(main);
  }
})();
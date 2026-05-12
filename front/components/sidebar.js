(function () {
  const pagina = window.location.pathname.split("/").pop() || "dashboard.html";

  const itens = [
    { href: "../pages/dashboard.html",     icone: "ti-home",    label: "Página Inicial" },
    { href: "../pages/nova_coleta.html",   icone: "ti-plus",    label: "Nova coleta" },
    { href: "../pages/history.html",       icone: "ti-history", label: "Histórico" },
    { href: "../pages/locais_coleta.html", icone: "ti-map-pin", label: "Locais de coleta" },
    { href: "../pages/ranking.html",       icone: "ti-trophy",  label: "Ranking" },
    { href: "../pages/perfil.html",        icone: "ti-user",    label: "Perfil" },
  ];

  const comunidadeIdx = 4;

  const navHTML = itens.map((item, i) => {
    const secao = i === comunidadeIdx
      ? `<div class="sidebar-section">Comunidade</div>`
      : i === 0 ? `<div class="sidebar-section">Menu</div>` : "";
    const ativo = pagina === item.href ? "active" : "";
    return `
      ${secao}
      <a href="${item.href}" class="nav-item ${ativo}">
        <i class="ti ${item.icone}" aria-hidden="true"></i>
        <span class="nav-label">${item.label}</span>
      </a>
    `;
  }).join("");

  const html = `
    <div id="sidebar-overlay"></div>
    <aside id="app-sidebar">
      <button id="sidebar-close" aria-label="Fechar menu">
        <i class="ti ti-x" aria-hidden="true"></i>
      </button>
      ${navHTML}
    </aside>
  `;

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

      /* ── Desktop ── */
      #app-sidebar {
        position: sticky;
        top: 4rem;
        height: calc(100vh - 4rem);
        width: 13rem;
        background: #fff;
        border-right: 0.0625rem solid #e5e7eb;
        padding: 0.75rem 0;
        flex-shrink: 0;
        overflow-y: auto;
        transition: width 0.25s ease;
      }

      #sidebar-close {
        display: none;
      }

      #sidebar-overlay {
        display: none;
      }

      .sidebar-section {
        font-size: 0.625rem;
        font-weight: 600;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        padding: 0.75rem 1rem 0.25rem;
        white-space: nowrap;
      }

      .nav-item {
        display: flex;
        align-items: center;
        gap: 0.625rem;
        padding: 0.625rem 1rem;
        font-size: 0.875rem;
        color: #374151;
        text-decoration: none;
        border-left: 0.1875rem solid transparent;
        white-space: nowrap;
        transition: background 0.15s;
      }

      .nav-item:hover { background: #D8F3DC; }

      .nav-item.active {
        background: #D8F3DC;
        color: #1B4332;
        border-left-color: #1B4332;
        font-weight: 500;
      }

      .nav-item i {
        font-size: 1.125rem;
        opacity: 0.7;
        flex-shrink: 0;
      }

      .nav-item.active i { opacity: 1; }

      main {
        flex: 1;
        padding: 1.75rem 2rem;
      }

      /* ── Mobile ── */
      @media (max-width: 48rem) {

        #app-sidebar {
          position: fixed;
          top: 3rem;
          left: 0;
          height: calc(100vh - 3rem);
          width: 16rem;
          z-index: 200;
          transform: translateX(-100%);
          transition: transform 0.25s ease;
          box-shadow: 0.125rem 0 1rem rgba(0,0,0,0.1);
          padding-top: 0.5rem;
          overflow-y: auto;
        }

        #app-sidebar.open {
          transform: translateX(0);
        }

        #sidebar-close {
          display: flex;
          align-items: center;
          justify-content: flex-end;
          padding: 0 1rem 0.5rem;
          background: none;
          border: none;
          cursor: pointer;
          font-size: 1.25rem;
          color: #374151;
          width: 100%;
        }

        #sidebar-overlay {
          display: block;
          position: fixed;
          inset: 0;
          background: rgba(0,0,0,0);
          z-index: 199;
          pointer-events: none;
          transition: background 0.25s;
        }

        #sidebar-overlay.active {
          background: rgba(0,0,0,0.4);
          pointer-events: all;
        }

        main {
          padding: 1.25rem 1rem;
        }
      }
    </style>
  `;

  document.head.insertAdjacentHTML("beforeend", style);
  document.body.insertAdjacentHTML("beforeend", html);

  const main = document.querySelector("main");
  if (main) {
    const appLayout = document.createElement("div");
    appLayout.id = "app-layout";
    document.body.appendChild(appLayout);
    appLayout.appendChild(document.getElementById("app-sidebar"));
    appLayout.appendChild(main);
  }

  // ── Lógica ──
  const sidebar  = document.getElementById("app-sidebar");
  const overlay  = document.getElementById("sidebar-overlay");
  const btnClose = document.getElementById("sidebar-close");

  function abrirSidebar() {
    sidebar.classList.add("open");
    overlay.classList.add("active");
  }

  function fecharSidebar() {
    sidebar.classList.remove("open");
    overlay.classList.remove("active");
  }

  btnClose.addEventListener("click", fecharSidebar);
  overlay.addEventListener("click", fecharSidebar);

  window.abrirSidebar = abrirSidebar;

})();
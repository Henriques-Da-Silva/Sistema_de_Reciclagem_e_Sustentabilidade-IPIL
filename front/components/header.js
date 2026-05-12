(function () {
  const usuario = JSON.parse(localStorage.getItem("usuario") || '{"nome":"Usuário"}');
  const iniciais = usuario.nome.split(" ").map(p => p[0]).join("").slice(0, 2).toUpperCase();

  const html = `
    <header id="app-header">
      <div class="header-left">

        <!-- só aparece no mobile -->
        <button id="btn-hamburger" aria-label="Abrir menu" onclick="window.abrirSidebar()">
          <i class="ti ti-menu-2" aria-hidden="true"></i>
        </button>

        <div class="header-logo">
          <img src="../img/logo3.png" alt="Reciclagem Sustentável IPIL" class="header-logo-img" />
        </div>
      </div>

      <div class="header-right">
        <span class="header-username">${usuario.nome}</span>
        <div class="header-avatar">${iniciais}</div>
      </div>
    </header>
  `;

  const style = `
    <style>
      #app-header {
        background: #1B4332;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 1.5rem;
        height: 4rem;
        position: sticky;
        top: 0;
        z-index: 100;
      }

      .header-left {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        height: 100%;
      }

      .header-logo {
        display: flex;
        align-items: center;
        height: 100%;
      }

      .header-logo-img {
        height: 100%;
        width: auto;
      }

      .header-right {
        display: flex;
        align-items: center;
        gap: 0.625rem;
      }

      .header-username {
        color: #9FE1CB;
        font-size: 0.8125rem;
      }

      .header-avatar {
        width: 2rem;
        height: 2rem;
        border-radius: 50%;
        background: #2D6A4F;
        color: #D8F3DC;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: 600;
        cursor: pointer;
      }

      /* hambúrguer — escondido no desktop */
      #btn-hamburger {
        display: none;
        background: none;
        border: none;
        color: #D8F3DC;
        font-size: 1.375rem;
        cursor: pointer;
        padding: 0.25rem;
        line-height: 1;
      }

      /* mobile */
      @media (max-width: 48rem) {
        #app-header {
          padding: 0 1rem;
          height: 3rem;
        }

        .header-logo-img {
          height: 100%;
        }

        .header-username {
          display: none;
        }

        #btn-hamburger {
          display: flex;
          align-items: center;
          justify-content: center;
        }
      }
    </style>
  `;

  document.head.insertAdjacentHTML("beforeend", style);
  document.body.insertAdjacentHTML("afterbegin", html);
})();
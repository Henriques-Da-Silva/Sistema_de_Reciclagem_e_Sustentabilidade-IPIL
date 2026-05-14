(function () {
	const API = "http://127.0.0.1:8000/usuarios/users"

	function formatPoints(p) {
		try {
			return new Intl.NumberFormat('pt-BR').format(p) + ' pts'
		} catch (e) {
			return p + ' pts'
		}
	}

	function getNivel(pontos) {
		// Regras simples de nível — ajuste conforme necessário
		if (pontos >= 4500) return 'Reciclador Lendário'
		if (pontos >= 4000) return 'Reciclador Prata'
		if (pontos >= 3500) return 'Reciclador Bronze'
		if (pontos >= 2000) return 'Reciclador Verde'
		return 'Reciclador Iniciante'
	}

	function createItem(user, index) {
		const item = document.createElement('div')
		item.classList.add('item')
		if (index === 0) item.classList.add('top1')
		if (index === 1) item.classList.add('top2')
		if (index === 2) item.classList.add('top3')

		const left = document.createElement('div')
		left.classList.add('left')

		const pos = document.createElement('div')
		pos.classList.add('posicao')
		pos.textContent = String(index + 1)

		const infoWrap = document.createElement('div')
		const nome = document.createElement('div')
		nome.classList.add('nome')
		nome.textContent = user.nome || user.email || 'Usuário'

		const nivel = document.createElement('div')
		nivel.classList.add('nivel')
		nivel.textContent = getNivel(user.pontuacao || 0)

		infoWrap.appendChild(nome)
		infoWrap.appendChild(nivel)

		left.appendChild(pos)
		left.appendChild(infoWrap)

		const pontosDiv = document.createElement('div')
		pontosDiv.classList.add('pontos')
		pontosDiv.textContent = formatPoints(user.pontuacao || 0)

		item.appendChild(left)
		item.appendChild(pontosDiv)

		return item
	}

	async function loadRanking() {
		const rankingBox = document.querySelector('.ranking-box')
		if (!rankingBox) return

		rankingBox.innerHTML = '<div class="loading">Carregando ranking...</div>'

		try {
			const res = await fetch(API)
			if (!res.ok) {
				const txt = await res.text()
				throw new Error(`${res.status} - ${txt}`)
			}

			const users = await res.json()

			if (!Array.isArray(users) || users.length === 0) {
				rankingBox.innerHTML = '<div class="empty">Nenhum usuário encontrado.</div>'
				return
			}

			// Ordena por pontuação decrescente
			users.sort((a, b) => (b.pontuacao || 0) - (a.pontuacao || 0))

			// Limpa e monta os itens
			rankingBox.innerHTML = ''
			users.forEach((u, i) => {
				const el = createItem(u, i)
				rankingBox.appendChild(el)
			})

		} catch (err) {
			console.error('Erro ao carregar ranking:', err)
			rankingBox.innerHTML = `<div class="error">Erro ao carregar ranking: ${err.message}</div>`
		}
	}

	// Inicializa quando a DOM estiver pronta
	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', loadRanking)
	} else {
		loadRanking()
	}

})();


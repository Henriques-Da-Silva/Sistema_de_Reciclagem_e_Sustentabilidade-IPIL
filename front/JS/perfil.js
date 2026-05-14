btn = document.getElementById("logout_btn");

btn.addEventListener("click", function() {
    localStorage.removeItem("usuario");
    window.location.href = "../pages/login.html";
} )

async function Carregar_Perfil() {
    const usuario = localStorage.getItem("usuario");
    
    if(!usuario){
        window.location.href = "../pages/login.html";
        return;
    }

    try {

        const user_data = JSON.parse(usuario)
        const resposta = await fetch(`http://127.0.0.1:8000/usuarios/${user_data.id}`)
    
        if (!resposta.ok){
            console.error("Erro ao carregar dados do usuário:", resposta.status);
            localStorage.removeItem("usuario");
            window.location.href = "../pages/login.html";
            return;
        }
    
        const user_info = await resposta.json();

        const iniciais = user_info.nome.split(" ").map(p => p[0]).join("").slice(0, 2).toUpperCase();

        document.getElementById("avatar").innerText = "";
        document.getElementById("avatar").innerText = iniciais;

        document.getElementById("user_name").innerText = "";
        document.getElementById("user_name").innerText = user_info.nome;

        document.getElementById("user_email").innerText = "";
        document.getElementById("user_email").innerText = user_info.email;

        function getNivel(pontos) {
            // Regras simples de nível — ajuste conforme necessário
            if (pontos >= 4500) return 'Reciclador Lendário'
            if (pontos >= 4000) return 'Reciclador Prata'
            if (pontos >= 3500) return 'Reciclador Bronze'
            if (pontos >= 2000) return 'Reciclador Verde'
            return 'Reciclador Iniciante'
	    }

        document.getElementById("user_level").innerText = "";
        document.getElementById("user_level").innerText = getNivel(user_info.pontos);

        document.getElementById("pontos").innerText = "";
        document.getElementById("pontos").innerText = user_info.pontuacao.toLocaleString();
        
        document.getElementById("total_reciclado").innerText = "";
        document.getElementById("total_reciclado").innerText = user_info.total_reciclado.toLocaleString() + " Kg";

        user_id = JSON.parse(localStorage.getItem("usuario")).id

        const coletas = await fetch(`http://127.0.0.1:8000/coletas/${user_info.id}`)
        if (!coletas.ok) throw new Error("Erro ao listar as coletas do usuario");
        const list_coletas = await coletas.json();
        const ultimas4 = list_coletas.slice(0, 4);

        document.getElementById("coletas_realizadas").innerText = list_coletas.length;
        document.getElementById("ranking").innerText = "view at ranking";

        document.getElementById("atividades").innerHTML = `<h2>Últimas Atividades</h2>`;
        for (const coleta of ultimas4) {
            material = await fetch(`http://127.0.0.1:8000/materiais/${coleta.idMaterial}`);

            if (!material.ok) {
                console.error("Erro ao carregar material:", material.status);
                return;
            }

            const material_info = await material.json();

            const div = document.createElement("div");
            div.className = "item"
            div.innerHTML = `<div class="material">
                                ${material_info.nome}
                            </div>
                            <div class="data">
                                ${coleta.quantidadeKilo} Kg • ${new Date(coleta.dataCadastro).toLocaleDateString()}
                            </div>`;
            document.getElementById("atividades").appendChild(div);
        }

    } catch (err) {
        console.log("Erro:", err)
        window.location.href = "../pages/login.html";
    }
}

Carregar_Perfil();
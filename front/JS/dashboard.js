async function CarregarUsuario() {
    const usuario = localStorage.getItem("usuario");
    
    if(!usuario){
        window.location.href = "../pages/login.html";
        return;
    }

    try {
        const user_data = JSON.parse(usuario)
        const resposta = await fetch(`${API_URL}/usuarios/${user_data.id}`)
    
        if (!resposta.ok){
            console.error("Erro ao carregar dados do usuário:", resposta.status);
            localStorage.removeItem("usuario");
            window.location.href = "../pages/login.html";
            return;
        }
    
        const user_info = await resposta.json();
    
        document.getElementById("usuario_nome").innerText = user_info.nome;
        document.getElementById("pontos").innerText = user_info.pontuacao;
        document.getElementById("total_reciclado").innerText = user_info.total_reciclado;

        const coletas_user = await fetch(`${API_URL}/coletas/${user_data.id}`)

        if (!coletas_user.ok) {
            console.error("Erro ao carregar coletas do usuário:", coletas_user.status);
            return;
        }

        const coletas_info = await coletas_user.json();
        const ultimas4 = coletas_info.slice(0, 4);
        const coletas_ul = document.getElementById("coletas");

        if (!Array.isArray(ultimas4) || ultimas4.length === 0) {
            coletas_ul.innerHTML = `<li class="flex justify-between items-center bg-gray-100 p-4 rounded-lg">Nenhuma coleta encontrada.</li>`;
            return;
        }

        for (const coleta of ultimas4) {

            material = await fetch(`${API_URL}/materiais/${coleta.idMaterial}`);

            if (!material.ok) {
                console.error("Erro ao carregar material:", material.status);
                return;
            }

            const material_info = await material.json();

            const li = document.createElement("li");
            li.className = "flex justify-between items-center bg-gray-100 p-4 rounded-lg";
            li.innerHTML = `<span class="font-medium">${material_info.nome}</span>
                           <span class="text-green-600 font-semibold">+${coleta.pontos_ganhos} pts</span>`;
            coletas_ul.appendChild(li);
        }


    } catch (err) {
        console.log("Erro:", err)
            window.location.href = "../pages/login.html";
    }
}

CarregarUsuario();
async function Historico_coletas() {
    user_id = JSON.parse(localStorage.getItem("usuario")).id

    const coletas = await fetch(`${API_URL}/coletas/${user_id}`)
    if (!coletas.ok) throw new Error("Erro ao listar as coletas do usuario");

    const list_coletas = await coletas.json();

    for (const coleta of list_coletas) {

        material = await fetch(`${API_URL}/materiais/${coleta.idMaterial}`);

        if (!material.ok) {
            console.error("Erro ao carregar material:", material.status);
            return;
        }

        const material_info = await material.json();

        const data = coleta.dataCadastro.split("T")

        const tr = document.createElement("tr")
        tr.innerHTML = `<td>${data[0]}</td>
                        <td>${material_info.nome}</td>
                        <td>${coleta.quantidadeKilo} Kg</td>
                        <td class="pontos">+${coleta.pontos_ganhos} pts</td>`
        document.getElementById("table_body").appendChild(tr);
    }
}

Historico_coletas();
async function Listar_Locais_de_Coleta() {
    const resposta = await fetch(`${API_URL}/locais-coleta/`)
    if (!resposta.ok) throw new Error("Erro ao listar pontos de coleta.");

    const locais = await resposta.json();

    for (const local of locais) {
        const card = document.createElement("div");
        card.className = "card";
        card.innerHTML = ` <h2>${local.nome}</h2>
                            <div class="info">
                                <p class="p-2 bg-green-100 rounded mb-4"> ${local.descricao} </p>
                                <p class="text-gray-600"> 
                                    <span class="text-green-700 font-semibold">Endereço: </span>
                                    ${local.endereco} 
                                </p>
                            </div>
                            <div class="materiais">
                                <h3 class="text-green-700 font-semibold">Materiais aceites: </h3>
                                <ul>
                                    <li>Papel</li>
                                    <li>Vidro</li>
                                    <li>Plástico</li>
                                </ul>
                            </div> `

        document.getElementById("locais_coleta").appendChild(card);
    }
}

Listar_Locais_de_Coleta();
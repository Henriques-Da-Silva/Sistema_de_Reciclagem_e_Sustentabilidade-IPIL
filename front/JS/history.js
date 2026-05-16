async function Historico_coletas() {
    
    try {    
        const user = JSON.parse(localStorage.getItem("usuario"));
        if (!user) return alert("Usuário não logado");
        const user_id = user.id;
    
        const coletas = await fetch(`${API_URL}/coletas/${user_id}`)
        if (!coletas.ok) throw new Error("Erro ao listar as coletas do usuario");
    
        const list_coletas = await coletas.json();

        if (!Array.isArray(list_coletas) || list_coletas.length === 0) {
            document.getElementById("table_body").innerHTML = "<tr><td colspan='4'>Nenhuma coleta encontrada.</td></tr>";
            return;
        }
    
        for (const coleta of list_coletas) {
    
            const material = await fetch(`${API_URL}/materiais/${coleta.idMaterial}`);
    
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
    } catch (erro) {
        console.error(erro);
        alert("Erro ao carregar histórico. Tenta novamente.");
    }
}

btn = document.getElementById("export_historic")

btn.addEventListener("click", () => {
    const linhas = document.querySelectorAll("table tr");

    let csv = [];

    linhas.forEach(linha => {
        let cols = linha.querySelectorAll("th, td");
        let dados = [];

        cols.forEach(col => {
            let texto = col.innerText.replace(/,/g, "");
            dados.push(texto);
        });

        csv.push(dados.join(","));
    });

    const csvString = csv.join("\n");

    const blob = new Blob([csvString], { type: "text/csv" });

    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "historico_coletas.csv";

    link.click();
});

Historico_coletas();
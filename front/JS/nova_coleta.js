form = document.getElementById("nova_coleta_form");

async function listar_materiais() {
    try {
        const response = await fetch(`${API_URL}/materiais/`);
        if (!response.ok) { throw new Error("Erro ao listar materiais"); }

        const materiais = await response.json();
        const select = document.getElementById("materiais_select");
        select.innerHTML = '<option value="">Selecione um material</option>';

        for (const material of materiais) {
            const option = document.createElement("option");
            option.value = material.id;
            option.textContent = material.nome;
            select.appendChild(option);
        }

    } catch (error) {
        console.error("Erro:", error);
    }
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const quantidade = parseFloat(document.getElementById("quantidade").value);
    const material = parseInt(document.getElementById("materiais_select").value);

    if(!material) {
        alert("Por favor, selecione um material.");
        return;
    }
    const data = {
        idUsuario: JSON.parse(localStorage.getItem("usuario")).id,
        idMaterial: material,
        quantidadeKilo: quantidade
    };

    try {
        const response = await fetch(`${API_URL}/coletas/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) { throw new Error("Erro ao registrar coleta"); }

        const result = await response.json();
        console.log("Coleta registrada com sucesso:", result);
        form.reset();
        window.location.href = "../pages/dashboard.html";

    } catch (error) {
        console.error("Erro:", error);
        alert("Erro ao registrar coleta: " + error.message);
    }
});

listar_materiais();
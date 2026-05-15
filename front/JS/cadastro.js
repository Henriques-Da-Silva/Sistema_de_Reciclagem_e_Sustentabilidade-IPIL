const form = document.getElementById("cadastro_form")

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const API_URL = "https://sistema-de-reciclagem-e-sustentabilidade.onrender.com"

    const nome = document.getElementById("nome").value.trim()
    const email = document.getElementById("email").value.trim()
    const senha = document.getElementById("senha").value
    const confirmarSenha = document.getElementById("confirmar_senha").value

    if (senha !== confirmarSenha) {
        alert("As senhas não coincidem.");
        return;
    }

    const data = {
        nome: nome,
        email: email,
        senha: senha,
    };

    try {
        const response = await fetch(`${API_URL}/usuarios/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            const result = await response.json();
            console.log("Usuário cadastrado:", result);
            alert("Cadastro realizado com sucesso!");

            localStorage.setItem("usuario", JSON.stringify(result));
            window.location.href = "../pages/dashboard.html";
        } else {
            const text = await response.text();
            console.error("Erro ao cadastrar usuário", response.status, text);
            alert(`Erro ao cadastrar usuário: ${response.status} - ${text}`);
        }
    } catch (err) {
        console.error("Fetch error:", err);
        alert("Erro de rede ao tentar cadastrar usuário.");
    }
});

form = document.getElementById("login_form");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value.trim();
    const senha = document.getElementById("senha").value;

    const data = {
        email: email,
        senha: senha
    };

    try {
        const response = await fetch("http://192.168.43.231:8000/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const result = await response.json();
            console.log("Login bem-sucedido:", result);
            alert("Login realizado com sucesso!");

            localStorage.setItem("usuario", JSON.stringify(result));
            window.location.href = "../pages/dashboard.html";
        } else {
            const text = await response.text();
            console.error("Erro ao fazer login", response.status, text);
            alert(`Erro ao fazer login: ${response.status} - ${text}`);
        }
    } catch (err) {
        console.error("Fetch error:", err);
        alert("Erro de rede ao tentar fazer login.");
    }
});

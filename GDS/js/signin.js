document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("signin");

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const cif = document.getElementById("cif").value.trim();
        const nombreAgencia = document.getElementById("nombreAgencia").value.trim();
        const email = document.getElementById("email").value.trim();
        const numTelefono = document.getElementById("numTelefono").value.trim();
        const url = document.getElementById("url").value.trim();
        const contrasena = document.getElementById("contrasena").value.trim()

        if (!cif || !nombreAgencia || !email || !numTelefono || !url || contrasena) {
            alert("Todos los campos son obligatorios");
            return;
        }

        const body = { cif, nombreAgencia, email, numTelefono, url, contrasena };

        try {
            const res = await fetch("http://localhost:3000/api/agencia/create", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(body)
            });

            const data = await res.json();

            if (data.error) {
                alert(data.message);
                return;
            }
            if (data.agenciaCIF) {
                localStorage.setItem("agenciaCIF", data.agenciaCIF.toString());
            }

            window.location.href = "main.html";

        } catch (err) {
            console.error("Error de conexión:", err);
            alert("No se pudo conectar con el servidor");
        }

    });

});
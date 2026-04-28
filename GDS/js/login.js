document.addEventListener("DOMContentLoaded", function () {

    document.getElementById("login").addEventListener("submit", async function(e){

        e.preventDefault();

        const cif = document.getElementById("cif").value.trim();
        const email = document.getElementById("email").value.trim();
        const contrasena = document.getElementById("contrasena").value.trim();

        if(!cif || !email || !contrasena){
            alert("Todos los campos son obligatorios");
            return;
        }

        const url = `http://localhost:3000/api/agencia/inicioSesion?email=${encodeURIComponent(email)}&contrasena=${encodeURIComponent(contrasena)}&cif=${encodeURIComponent(cif)}`;

        try{
            const res = await fetch(url);

            if (!res.ok) {
                throw new Error("Error en servidor");
            }

            const data = await res.json();

            if (data.error || !data.agencia || data.agencia.length === 0) {
                alert("Credenciales incorrectas");
                return;
            }

            const agencia = data.agencia[0].cif;
            localStorage.setItem("agenciaCIF", agencia);

            window.location.href = "main.html"; 

        }catch (err) {
            console.error("Error de conexión:", err);
            alert("No se pudo conectar con el servidor");
        }

    });

});
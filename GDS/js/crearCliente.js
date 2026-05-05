document.addEventListener("DOMContentLoaded", function(){
    document.getElementById("crearCliente").addEventListener("submit",async function(e){
        e.preventDefault();

        const nombre = document.getElementById("nombreCliente").value.trim();
        const email = document.getElementById("email").value.trim();
        const apellido = document.getElementById("apellido").value.trim();
        const dni = document.getElementById("dni").value.trim();
        const numTelefono = document.getElementById("telefono").value.trim();
        const cif = localStorage.getItem("agenciaCIF");
        const contrasena = `${nombre}${apellido.charAt(0) || ""}123`;//Tìpica constraseá creada predeterminada cuando se crea una cuenta para una cliente

        if(!nombre || !email || !apellido || !dni || !numTelefono){
            alert("Todos los campos son obligatorios");
            return;
        }
        const body = {nombre, apellido, email, cif,dni, contrasena, numTelefono}
        try{
            const res = await fetch("http://localhost:3000/api/clientes/create",{
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(body)
            })

            const data = await res.json();

            if(data.error){
                alert(data.message);
                return;
            }

            alert("Cliente creado correctamente");
            window.location.href = "clientes.html";


        }catch(err){
            console.error(err);
            alert("No se pudo conectar con el servidor");

        }

    })

})
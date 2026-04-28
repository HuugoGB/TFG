document.addEventListener("DOMContentLoaded", function(){
    const agenciaCIF = localStorage.getItem("agenciaCIF");

    const authButtons = document.getElementById("authButtons");
    const logoutButton = document.getElementById("logoutButton");

    const cardReservas = document.getElementById("cardReservas");
    const cardClientes = document.getElementById("cardClientes");

    if (agenciaCIF){
        authButtons.style.display = "none";
        logoutButton.style.display = "block";
    }else{
        logoutButton.style.display = "none";

        cardReservas.style.display = "none";
        cardClientes.style.display = "none";
    }

    logoutButton.addEventListener("click", function () {
        localStorage.removeItem("agenciaCIF");
        window.location.reload();
    });
})
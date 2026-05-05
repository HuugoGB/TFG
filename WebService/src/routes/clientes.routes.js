const express = require("express");
const { getAllClientes, createCliente, inicioSesionCliente,getCliente, deleteCliente, getReservasCliente, getReservasClienteEnVigor,updateCliente } = require("../controllers/clientes.controller");

const router = express.Router();

router.get("/",getAllClientes);
router.get("/inicioSesion",inicioSesionCliente);
router.post("/create", createCliente);
router.get("/buscar", getCliente);
router.delete("/delete/:idCliente", deleteCliente);
router.get("/reservasCliente/", getReservasCliente);
router.get("/reservasEnVigor/",getReservasClienteEnVigor)
router.put("/update/:idCliente", updateCliente);

module.exports = router;
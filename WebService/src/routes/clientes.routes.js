const express = require("express");
const { getAllClientes, createCliente, inicioSesionCliente,getCliente, deleteCliente, getReservasCliente, updateCliente } = require("../controllers/clientes.controller");

const router = express.Router();

router.get("/",getAllClientes);
router.get("/inicioSesion/",inicioSesionCliente);
router.post("/create", createCliente);
router.get("/buscar", getCliente);
router.delete("/delete/:idCliente", deleteCliente);
router.get("/reservasCliente/:idCliente", getReservasCliente);
router.put("/update/:idCliente", updateCliente);

module.exports = router;
const express = require("express");
const { createCliente, getCliente, deleteCliente, getReservasCliente, updateCliente } = require("../controllers/clientes.controller");

const router = express.Router();

router.post("/create", createCliente);
router.get("/read", getCliente);
router.delete("/delete/:idCliente", deleteCliente);
router.get("/reservas_cliente/:idCliente", getReservasCliente);
router.put("/update/:idCliente", updateCliente);

module.exports = router;
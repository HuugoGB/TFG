const express = require("express");
const {getAllServiciosReserva, createServicioReserva} = require("../controllers/serviciosreserva.controller");

const router = express.Router();
router.get("/",getAllServiciosReserva);
router.post("/create",createServicioReserva);

module.exports = router;
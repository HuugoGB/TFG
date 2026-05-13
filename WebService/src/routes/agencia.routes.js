const express = require("express");
const { getAllAgencias, getNombreAgencia, crearAgencia, inicioSesionAgencia, getReservasAgenciaEnFechas, createReserva } = require("../controllers/agencia.controller");

const router = express.Router();
router.get("/",getAllAgencias);
router.get("/",getNombreAgencia);
router.post("/create",crearAgencia);
router.get("/inicioSesion", inicioSesionAgencia);
router.get("/reservasFechas",getReservasAgenciaEnFechas);
router.post("/createReserva",createReserva);

module.exports = router;
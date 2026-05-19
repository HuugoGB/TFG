const express = require("express");
const { getAllAgencias, getNombreAgencia, crearAgencia, inicioSesionAgencia, getReservasAgenciaEnFechas, createReserva,infoReservasFecha } = require("../controllers/agencia.controller");

const router = express.Router();
router.get("/",getAllAgencias);
router.get("/",getNombreAgencia);
router.post("/create",crearAgencia);
router.get("/inicioSesion", inicioSesionAgencia);
router.get("/reservasFechas",getReservasAgenciaEnFechas);
router.post("/createReserva",createReserva);
router.get("/infoReservasFecha", infoReservasFecha)

module.exports = router;
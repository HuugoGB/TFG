const express = require("express");
const { getAllAgencias, getNombreAgencia, crearAgencia, inicioSesionAgencia } = require("../controllers/agencia.controller");

const router = express.Router();
router.get("/",getAllAgencias);
router.get("/",getNombreAgencia);
router.post("/create",crearAgencia);
router.get("/inicioSesion", inicioSesionAgencia);

module.exports = router;
const express = require("express");
const {getAllTipoHab, getTipoHabPorPax, createTipoHab, disponibilidadTipoHab} = require("../controllers/tipohab.controller")

const router = express.Router();

router.get("/",getAllTipoHab);
router.get("/porPax/:pax",getTipoHabPorPax);
router.post("/create", createTipoHab);
router.get("/disponibilidad", disponibilidadTipoHab);

module.exports = router;
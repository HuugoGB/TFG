const express = require("express");
const {getAllTipoHab, getTipoHabPorPax, createTipoHab, disponibilidadTipoHab, disponibilidadTodos} = require("../controllers/tipohab.controller")

const router = express.Router();

router.get("/",getAllTipoHab);
router.get("/porPax/:pax",getTipoHabPorPax);
router.post("/create", createTipoHab);
router.get("/disponibilidad", disponibilidadTipoHab);
router.get("/disponibilidad_todas",disponibilidadTodos)

module.exports = router;
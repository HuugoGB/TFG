const express = require("express");
const {getInfoHabs,createHabitaciones, disponibilidadHabitacion} = require("../controllers/habitacion.controller")

const router = express.Router();

router.get("/",getInfoHabs)
router.post("/create/:cantidad",createHabitaciones);
router.get("/disponibilidad", disponibilidadHabitacion);

module.exports = router;
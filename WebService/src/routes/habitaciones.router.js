const express = require("express");
const {createHabitaciones, disponibilidadHabitacion} = require("../controllers/habitacion.controller")

const router = express.Router();

router.post("/create/:cantidad",createHabitaciones);
router.get("/disponibilidad", disponibilidadHabitacion);

module.exports = router;
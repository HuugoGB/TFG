const express = require("express");
const { getAllReservas, getReservas, createReserva, getAllReservasEnFechas, deleteReserva, updateReserva, updateCampoReserva, asignarHabitacion, cambiarEstado} = require("../controllers/reservas.controller");

const router = express.Router();

router.get("/",getAllReservas);
router.get("/buscar", getReservas);
router.post("/create", createReserva);
router.get("/entre_fechas", getAllReservasEnFechas);
router.delete("/delete/:idReserva", deleteReserva);
router.put("/update/:idReserva", updateReserva);
router.patch("/updateCampo/:idReserva",updateCampoReserva);
router.patch("/asignarHabitacion/:idReserva", asignarHabitacion);
router.patch("/cambiarEstado/:idReserva", cambiarEstado);
module.exports = router;

const express = require("express");
const {getAllTipoHab, createTipoHab, disponibilidadTipoHab} = require("../controllers/tipohab.controller")

const router = express.Router();

router.get("/",getAllTipoHab);
router.post("/create", createTipoHab);
router.get("/disponibilidad", disponibilidadTipoHab);

module.exports = router;
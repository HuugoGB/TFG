const express = require("express");
const {getAllServiciosExtra, getPrecioServicioExtra} = require("../controllers/serviciosextra.controller")

const router = express.Router();

router.get("/",getAllServiciosExtra);
router.get("/precio",getPrecioServicioExtra);

module.exports = router;
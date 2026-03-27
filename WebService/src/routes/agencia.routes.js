const express = require("express");
const { getAllAgencias, getNombreAgencia } = require("../controllers/agencia.controller");

const router = express.Router();
router.get("/",getAllAgencias);
router.get("/:cif")

module.exports = router;
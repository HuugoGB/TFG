const express = require("express");
const { getAllAgencias } = require("../controllers/agencia.controller");

const router = express.Router();
router.get("/",getAllAgencias);

module.exports = router;
const express = require("express");
const {getAllRegimenes,getPrecioRegimen, createRegimen, updateRegimen, deleteRegimen} = require("../controllers/regimen.controller")

const router = express.Router();

router.get("/",getAllRegimenes);
router.get("/precio",getPrecioRegimen);
router.post("/create", createRegimen);
router.patch("/update/:tipoRegimen", updateRegimen);
router.delete("/:tipoRegimen", deleteRegimen);



module.exports = router;
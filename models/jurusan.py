from odoo import models, fields

class Kota(models.Model):
    _name = "siswa.jurusan"
    _description = "Kota"

    name = fields.Char(string="Jurusan", required=True)

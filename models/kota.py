from odoo import models, fields

class Kota(models.Model):
    _name = "siswa.kota"
    _description = "Kota"

    name = fields.Char(string="Nama Kota", required=True)

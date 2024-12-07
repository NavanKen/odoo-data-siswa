from datetime import date
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SiswaProperty(models.Model):
    _name = "siswa_property"
    _description = "Siswa Property"
    _order = "tanggal_lahir desc"

    name = fields.Char(string="Nama Siswa", required=True)
    nis = fields.Char(string="NIS Siswa", required=True)
    tanggal_lahir = fields.Date(string="Tanggal Lahir", required=True)
    age = fields.Integer(string="Umur", required=True)
    asal_sekolah = fields.Char(string="Asal Sekolah", required=True)
    gender = fields.Selection([
        ('male', 'Laki-laki'),
        ('female', 'Perempuan'),
    ], string="Jenis Kelamin", required=True)


    kota_id = fields.Many2one('siswa.kota', string="Kota Asal", required=True)
    jurusan_id = fields.Many2one('siswa.jurusan', string="Jurusan Anda", required=True)
    tahun_lahir = fields.Integer(string="Tahun Lahir", compute="_compute_tahun_lahir", store=True)


    @api.depends('tanggal_lahir')
    def _compute_tahun_lahir(self):
        for record in self:
            if record.tanggal_lahir:
                record.tahun_lahir = record.tanggal_lahir.year
            else:
                record.tahun_lahir = 0

            
    @api.onchange('tanggal_lahir')
    def _onchange_tanggal_lahir(self):
        for record in self:
            if record.tanggal_lahir:
                # Hitung umur otomatis berdasarkan tanggal lahir
                today = date.today()
                calculated_age = today.year - record.tanggal_lahir.year - (
                    (today.month, today.day) < (record.tanggal_lahir.month, record.tanggal_lahir.day)
                )
                record.age = calculated_age  # Update umur otomatis
                
                if record.age < 0:
                    raise ValidationError("Umur tidak boleh negatif.")
                if record.age != calculated_age:
                    raise ValidationError("Umur tidak sesuai dengan tanggal lahir. Silakan periksa kembali.")



    @api.constrains('nis')
    def _check_nis(self):
        for record in self:
            if not record.nis.isdigit():
                raise ValidationError("NIS harus berupa angka tanpa koma atau karakter lain.")


    @api.constrains('nis')
    def _check_unique_nis(self):
        for record in self:
            if self.search_count([('nis', '=', record.nis)]) > 1:
                raise ValidationError("Nis ini sudah digunakan")


    #Typo di @api.conrains('nis') bisa menyebabakan internal server error     
    # @api.conrains('nis')
    # def _check_unique_nis(self):
    #     for record in self:
    #         if self.search_count([('nis', '=', record.nis)]) > 1:
    #             raise ValidationError("Nis Sudah Ada")
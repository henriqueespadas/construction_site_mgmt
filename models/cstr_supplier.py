from odoo import models, fields


class ConstructionSupplier(models.Model):
    _name = "cstr.supplier"
    _ihnerits = {"res.partner": "partner_id"}
    _description = "Construction Supplier"

    partner_id = fields.Many2one("res.partner", string="Partner")
    materials_ids = fields.One2many("cstr.materials", "supplier_id", string="Materials")
    work_ids = fields.One2many("cstr.work", "supplier_id", string="Works")
    project_ids = fields.One2many("cstr.project", "supplier_id", string="Projects")

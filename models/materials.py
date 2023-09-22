from odoo import models, fields


class ConstructionMaterials(models.Model):
    _name = "cstr.materials"
    _description = "Construction Materials"

    name = fields.Char(string="Name")
    description = fields.Char(string="Description")
    quantity = fields.Integer(string="Quantity")
    unit_price = fields.Float(string="Unit Price")
    total_price = fields.Float(string="Total Price")
    work_id = fields.Many2one("cstr.work", string="Work")
    supplier_id = fields.Many2one("cstr.supplier", string="Supplier")

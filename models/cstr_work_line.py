from odoo import models, fields


class ConstructionWorkLine(models.Model):
    _name = "cstr.work.line"
    _description = "Construction Work Line Item"

    description = fields.Char("Description")
    amount = fields.Float("Amount")
    work_id = fields.Many2one("cstr.work", string="Work")

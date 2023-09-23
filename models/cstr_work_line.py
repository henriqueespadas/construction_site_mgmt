from odoo import models, fields


class ConstructionWorkLine(models.Model):
    _name = "cstr.work.line"
    _description = "Construction Work Line Item"

    description = fields.Char("Description")
    amount = fields.Float("Amount")
    work_id = fields.Many2one("cstr.work", string="Work")
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    unity = fields.Selection([
        ('sq_m', 'Square Meter'),
        ('sq_ft', 'Square Foot'),
        ('cubic_m', 'Cubic Meter'),
        ('cubic_ft', 'Cubic Foot'),
        ('linear_m', 'Linear Meter'),
        ('linear_ft', 'Linear Foot'),
        ('kg', 'Kilogram'),
        ('lb', 'Pound'),
        ('unit', 'Unit'),
        ('liter', 'Liter'),
        ('gallon', 'Gallon')
    ], string='Unit of Measure')

from odoo import models, fields, api

from odoo.exceptions import ValidationError


class ConstructionWorkLine(models.Model):
    _name = "cstr.work.line"
    _description = "Construction Work Line Item"

    work_id = fields.Many2one("cstr.work", string="Work")
    description = fields.Char("Description")
    amount = fields.Float("Amount")
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    work_line_progress_bar = fields.Float(string='Progresso', default=0.0)
    unity = fields.Selection(
        [
            ("sq_m", "Square Meter"),
            ("sq_ft", "Square Foot"),
            ("cubic_m", "Cubic Meter"),
            ("cubic_ft", "Cubic Foot"),
            ("linear_m", "Linear Meter"),
            ("linear_ft", "Linear Foot"),
            ("kg", "Kilogram"),
            ("lb", "Pound"),
            ("unit", "Unit"),
            ("liter", "Liter"),
            ("gallon", "Gallon"),
        ],
        string="Unit of Measure",    )


    @api.model
    def create(self, vals):
        if 'work_line_progress_bar' in vals:
            if not 0.0 <= vals['work_line_progress_bar'] <= 100.0:
                raise ValidationError("O valor do progresso deve estar entre 0.0 e 100.0")
        return super('cstr.work.line', self).create(vals)

    def write(self, vals):
        if 'work_line_progress_bar' in vals:
            if not 0.0 <= vals['work_line_progress_bar'] <= 100.0:
                raise ValidationError("O valor do progresso deve estar entre 0.0 e 100.0")
        return super('cstr.work.line', self).write(vals)


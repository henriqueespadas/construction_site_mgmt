from odoo import models, fields


class ConstructionProject(models.Model):
    _inherit = "project.project"

    budget = fields.Float(string="Budget")
    costs = fields.Float(string="Costs")

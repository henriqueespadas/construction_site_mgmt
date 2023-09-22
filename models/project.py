from odoo import models, fields


class ConstructionProject(models.Model):
    _name = "cstr.project"
    _inherits = {"project.project": "project_id"}
    # _inherit = "project.project"

    budget = fields.Float(string="Budget")
    costs = fields.Float(string="Costs")
    project_id = fields.Many2one("project.project", string="Project")
    supplier_id = fields.Many2one("cstr.supplier", string="Supplier")

from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    safety_training_completed = fields.Boolean(default=False)
    role_in_construction = fields.Selection(
        [
            ("engineer", "Engineer"),
            ("mason", "Mason"),
            ("electrician", "Electrician"),
            ("plumber", "Plumber"),
            ("painter", "Painter"),
            ("carpenter", "Carpenter"),
            ("helper", "Helper"),
            ("other", "Other"),
        ],
        string="Role in Construction",
    )

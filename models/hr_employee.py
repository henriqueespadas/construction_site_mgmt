from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    role_in_construction = fields.Selection([
        ('engenheiro', 'Engenheiro'),
        ('pedreiro', 'Pedreiro'),
        ('eletricista', 'Eletricista'),
        ('encanador', 'Encanador'),
        ('pintor', 'Pintor'),
        ('carpinteiro', 'Carpinteiro'),
        ('ajudante', 'Ajudante'),
        ('outro', 'Outro'),
    ], string='Role in Construction')
    safety_training_completed = fields.Boolean(default=False)
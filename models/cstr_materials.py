from odoo import models, fields


class ConstructionMaterials(models.Model):
    _name = "cstr.materials"
    _description = "Construction Materials"

    work_id = fields.Many2one("cstr.work", string="Work")
    supplier_id = fields.Many2one("cstr.supplier", string="Supplier")
    budget_ids = fields.One2many('cstr.material.budget', 'material_id', string='Budgets')
    name = fields.Char(string="Name")
    description = fields.Char(string="Description")
    quantity = fields.Integer(string="Quantity")
    unit_price = fields.Float(string="Unit Price")
    total_price = fields.Float(string="Total Price")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('requested', 'Requested'),
        ('ordered', 'Ordered'),
        ('received', 'Received'),
        ('cancelled', 'Cancelled')
    ], string='Purchase Status', default='draft')

    def button_request_material(self):
        if self.state == 'draft':
            self.state = 'requested'

    def button_cancel(self):
        if self.state == 'requested':
            self.state = 'draft'

    def button_open_budget_wizard(self):
        context = {
            'default_material_id': self.id,
        }
        return {
            'name': 'Generate Material Budget',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'cstr.materials.budget.wizard',
            'view_id': self.env.ref('cstr_mgmt.view_materials_budget_wizard_form').id,
            'target': 'new',
            'context': context,
        }

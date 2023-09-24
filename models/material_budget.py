from odoo import api, fields, models

class CstrMaterialBudget(models.Model):
    _name = 'cstr.material.budget'
    _description = 'Material Budget for Construction'

    material_id = fields.Many2one('cstr.materials', 'Material', required=True)
    supplier_id = fields.Many2one('res.partner', 'Supplier', required=True, domain=[('supplier_rank', '>', 0)])
    unit_price = fields.Float('Unit Price', required=True)
    quantity = fields.Float('Quantity', required=True)
    total_price = fields.Float('Total Price', compute='_compute_total_price')

    @api.depends('unit_price', 'quantity')
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.unit_price * record.quantity

from odoo import api, fields, models

class CstrMaterialBudget(models.Model):
    _name = 'cstr.material.budget'
    _description = 'Material Budget for Construction'

    supplier_id = fields.Many2one('res.partner', 'Supplier', required=True, domain=[('supplier_rank', '>', 0)])
    material_id = fields.Many2one('cstr.materials', 'Material', required=True)
    brand = fields.Char('Brand')
    unit_price = fields.Float('Unit Price', required=True)
    total_price = fields.Float('Total Price', compute='_compute_total_price')
    freight_cost = fields.Float('Freight Cost')
    quantity = fields.Float('Quantity', related='material_id.quantity', readonly=True)

    @api.depends('unit_price', 'quantity', 'freight_cost')
    def _compute_total_price(self):
        for record in self:
            record.total_price = (record.unit_price * record.quantity) + record.freight_cost

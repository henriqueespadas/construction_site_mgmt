from odoo import api, fields, models
class MaterialsBudgetWizard(models.TransientModel):
    _name = 'cstr.materials.budget.wizard'
    _description = 'Materials Budget Wizard'

    material_id = fields.Many2one("cstr.materials", string="Material")
    supplier_ids = fields.Many2many("res.partner", string="Suppliers", domain=[('supplier_rank', '>', 0)])
    unit_price = fields.Float(string="Unit Price")
    quantity = fields.Float(string="Quantity")
    brand = fields.Char(string="Brand")

    def button_generate_budget(self):
        for supplier in self.supplier_ids:
            self.env["cstr.materials.budget"].create({
                'material_id': self.material_id.id,
                'supplier_id': supplier.id,
                'unit_price': self.unit_price,
                'quantity': self.quantity,
                'brand': self.brand,
            })



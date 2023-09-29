from odoo import api, fields, models
from odoo.exceptions import ValidationError

class MaterialsBudgetWizard(models.TransientModel):
    _name = "cstr.materials.budget.wizard"
    _description = "Materials Budget Wizard"

    material_budget_ids = fields.Many2many('cstr.materials.budget', string='Material Budgets')
    material_id = fields.Many2one("cstr.materials", string="Material")
    supplier_ids = fields.Many2many(
        "res.partner", string="Suppliers", domain=[("supplier_rank", ">", 0)]
    )
    selected_winner = fields.Boolean(string="Selected Winner")
    unit_price = fields.Float(string="Unit Price")
    quantity = fields.Float(string="Quantity")
    brand = fields.Char(string="Brand")
    freight_cost = fields.Float(string="Freight Cost")
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
        ]
    )

    def button_generate_budget(self):
        for supplier in self.supplier_ids:
            self.env["cstr.materials.budget"].create(
                {
                    "material_id": self.material_id.id,
                    "supplier_id": supplier.id,
                    "unit_price": self.unit_price,
                    "quantity": self.quantity,
                    "brand": self.brand,
                    "freight_cost": self.freight_cost,
                }
            )

    @api.depends("material_id")
    def _compute_material_budget_ids(self):
        for wizard in self:
            if wizard.material_id:
                wizard.material_budget_ids = [(6, 0, wizard.material_id.budget_ids.ids)]

    def button_confirm(self):
        Mail = self.env['mail.mail']
        selected_suppliers = self.material_budget_ids.filtered(lambda r: r.selected_winner)
        if len(selected_suppliers) > 1:
            raise ValidationError("Only one supplier can be selected.")
        elif len(selected_suppliers) == 0:
            raise ValidationError("No suppliers were selected.")
        else:
            self.material_id.write({'state': 'ordered'})
            email_values = {
                'subject': 'Order Confirmation',
                'body_html': '<h1>Order Confirmation</h1><p>Your order has been confirmed.</p>',
                'email_to': selected_suppliers.supplier_id.email,
                'email_from': self.env.user.email,
            }
            email = Mail.create(email_values)
            email.send()
            return {'type': 'ir.actions.act_window_close'}
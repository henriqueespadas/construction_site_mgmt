from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class MaterialsBudgetWizard(models.TransientModel):
    _name = "cstr.materials.budget.wizard"
    _description = "Materials Budget Wizard"

    material_budget_ids = fields.Many2many(
        "cstr.materials.budget",
        compute="_compute_material_budget_ids",
        string="Material Budgets",
    )
    material_id = fields.Many2one("cstr.materials", string="Material")
    supplier_ids = fields.Many2many(
        "res.partner", string="Suppliers", domain=[("supplier_rank", ">", 0)]
    )
    unit_price = fields.Float(string="Unit Price")
    quantity = fields.Float(string="Quantity")
    brand = fields.Char(string="Brand")
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
                }
            )

    def button_select_winner(self):
        for line in self.material_budget_ids:
            if line.selected_winner:
                line.material_id.write(
                    {
                        "supplier_id": line.supplier_id.id,
                        "unit_price": line.unit_price,
                        "budget_winner": True,
                        "state": "ordered",
                    }
                )
                other_lines = self.material_budget_ids.filtered(
                    lambda x: x.id != line.id
                )
                other_lines.write({"budget_winner": False})
        return {"type": "ir.actions.act_window_close"}

    @api.depends("material_id")
    def _compute_material_budget_ids(self):
        for wizard in self:
            if wizard.material_id:
                wizard.material_budget_ids = [(6, 0, wizard.material_id.budget_ids.ids)]
                _logger.info("Budget IDs: %s", wizard.material_id.budget_ids.ids)

from odoo import models, fields


class ConstructionMaterials(models.Model):
    _name = "cstr.materials"
    _description = "Construction Materials"

    work_id = fields.Many2one("cstr.work", string="Work")
    supplier_id = fields.Many2one("cstr.supplier", string="Supplier")
    budget_ids = fields.One2many(
        "cstr.materials.budget", "material_id", string="Budgets"
    )
    budget_winner = fields.Boolean("Budget Winner", default=False)
    name = fields.Char(string="Name")
    description = fields.Char(string="Description")
    quantity = fields.Float(string="Quantity")
    unit_price = fields.Float(string="Unit Price")
    total_price = fields.Float(string="Total Price")
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("requested", "Requested"),
            ("ordered", "Ordered"),
            ("received", "Received"),
            ("cancelled", "Cancelled"),
        ],
        string="Purchase Status",
        default="draft",
    )
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
        ],
        string="Unit of Measure",
    )

    def button_request_material(self):
        if self.state == "draft":
            self.state = "requested"

    def button_cancel(self):
        if self.state == "requested":
            self.state = "draft"

    def button_open_budget_wizard(self):
        context = {
            "default_material_id": self.id,
            "default_quantity": self.quantity,
            "default_unity": self.unity,
        }
        return {
            "name": "Generate Material Budget",
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "cstr.materials.budget.wizard",
            "view_id": self.env.ref("cstr_mgmt.materials_budget_wizard_form_view").id,
            "target": "new",
            "context": context,
        }

    def button_open_winner_wizard(self):
        wiz = self.env["cstr.materials.budget.wizard"].create({"material_id": self.id})
        wiz._compute_material_budget_ids()
        context = {
            "default_material_id": self.id,
        }
        return {
            "name": "Select Budget Winner",
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "cstr.materials.budget.wizard",
            "view_id": self.env.ref("cstr_mgmt.wizard_budget_winner_form_view").id,
            "res_id": wiz.id,
            "target": "new",
            "context": context,
        }

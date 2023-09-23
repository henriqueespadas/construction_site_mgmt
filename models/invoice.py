from odoo import models, fields


class ConstructionInvoice(models.Model):
    _name = "cstr.invoice"
    _inherits = {"account.move": "invoice_id"}
    _description = "Construction Invoice"

    invoice_id = fields.Many2one(
        "account.move", "Related Invoice", required=True, ondelete="cascade"
    )
    cstr_project_id = fields.Many2one("cstr.project", "Construction Project")
    additional_costs = fields.Float("Additional Costs")
    retention_fee = fields.Float("Retention Fee")

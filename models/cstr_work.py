from odoo import api, fields, models


class ConstructionWork(models.Model):
    _name = "cstr.work"
    _description = "Construction Work"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char("Work Name", required=True, track_visibility="onchange")
    estimated_budget = fields.Float("Estimated Budget", track_visibility="onchange")
    actual_budget = fields.Float(
        "Actual Budget", compute="_compute_actual_budget", store=True
    )
    work_type = fields.Selection(
        [
            ("new", "New Construction"),
            ("renovation", "Renovation"),
            ("repair", "Repair"),
        ],
        string="Type of Work",
        default="new",
        track_visibility="onchange",
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("ongoing", "Ongoing"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="draft",
        track_visibility="onchange",
    )
    start_date = fields.Date("Start Date", track_visibility="onchange")
    end_date = fields.Date("End Date", track_visibility="onchange")
    description = fields.Text("Description", track_visibility="onchange")
    notes = fields.Text("Notes")
    work_line_ids = fields.One2many("cstr.work.line", "work_id", string="Work Lines")
    project_id = fields.Many2one(
        "cstr.project", string="Related Project", track_visibility="onchange"
    )
    contractor_id = fields.Many2one(
        "res.partner", string="Contractor", track_visibility="onchange"
    )
    employee_ids = fields.Many2many("hr.employee", string="Employees")
    supplier_id = fields.Many2one("cstr.supplier", string="Supplier")

    @api.depends("work_line_ids.amount")
    def _compute_actual_budget(self):
        for record in self:
            record.actual_budget = sum(line.amount for line in record.work_line_ids)

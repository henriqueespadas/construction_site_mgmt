from odoo import api, fields, models


class ConstructionWork(models.Model):
    _name = "cstr.work"
    _description = "Construction Work"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    project_id = fields.Many2one(
        "cstr.project", string="Related Project", track_visibility="onchange"
    )
    contractor_id = fields.Many2one(
        "res.partner", string="Contractor", track_visibility="onchange"
    )
    supplier_id = fields.Many2one("cstr.supplier", string="Supplier")
    responsible_id = fields.Many2one('res.partner', string='Responsible')
    work_line_ids = fields.One2many(
        "cstr.work.line",
        "work_id",
        string="Work Line Items",
        context={"default_work_id": "work_id"},
    )
    employee_ids = fields.Many2many("hr.employee", string="Employees")
    name = fields.Char("Work Name", required=True, track_visibility="onchange")
    estimated_budget = fields.Float("Estimated Budget", track_visibility="onchange")
    actual_budget = fields.Float(
        "Actual Budget", compute="_compute_actual_budget", store=True
    )
    work_progress_bar = fields.Float(string='Progresso', default=0.0, compute='_compute_work_progress_bar')
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
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Muito Baixa'),
        ('2', 'Baixa'),
        ('3', 'Média'),
        ('4', 'Alta'),
        ('5', 'Muito Alta')
    ], string='Prioridade', default='3')

    @api.depends('work_line_ids.amount')
    def _compute_actual_budget(self):
        for record in self:
            total_amount = sum(line.amount for line in record.work_line_ids)
            record.actual_budget = total_amount

    def _compute_work_progress_bar(self):
        for record in self:
            total_amount = sum(line.work_line_progress_bar for line in record.work_line_ids)
            total_amount = total_amount / len(record.work_line_ids)
            record.work_progress_bar = total_amount


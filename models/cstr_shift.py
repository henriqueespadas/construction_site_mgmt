from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ConstructionShift(models.Model):
    _name = "cstr.shift"
    _description = "Construction Shift"

    project_id = fields.Many2one("cstr.project", string="Project")
    employee_id = fields.Many2one("hr.employee", string="Employee")
    work_id = fields.Many2one("cstr.work", string="Work")
    start_time = fields.Datetime()
    end_time = fields.Datetime()

    @api.depends("start_time", "end_time")
    def _check_shift(self):
        for record in self:
            if not record.start_time or not record.end_time:
                raise ValidationError(_("Start time and end time must be provided"))

            if record.start_time >= record.end_time:
                raise ValidationError(_("End time must be greater than start time"))

            conflicting_shifts = self.search(
                [
                    ("employee_id", "=", record.employee_id.id),
                    ("start_time", "<", record.end_time),
                    ("end_time", ">", record.start_time),
                    ("id", "!=", record.id),
                ]
            )

            if conflicting_shifts:
                raise ValidationError(
                    _("Employee is already allocated in a conflicting shift")
                )

    @api.model_create_multi
    def create(self, vals_list):
        records = super(ConstructionShift, self).create(vals_list)
        records._check_shift()
        return records

    def write(self, vals):
        result = super(ConstructionShift, self).write(vals)
        self._check_shift()
        return result

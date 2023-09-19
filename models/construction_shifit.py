from odoo import api, fields, models, _

class ConstructionShift(models.Model):
    _name = 'construction.shift'
    _description = 'Construction Shift'

    start_time = fields.Datetime()
    end_time = fields.Datetime()
    employee_id = fields.Many2one('hr.employee', string='Employee')

    @api.model
    def allocate_shift(self, employee_id, start_time, end_time):
        if not start_time or not end_time:
            raise Warning(_('Start time and end time must be provided'))

        if start_time >= end_time:
            raise Warning(_('End time must be greater than start time'))

        conflicting_shifts = self.search([
            ('employee_id', '=', employee_id),
            ('start_time', '<', end_time),
            ('end_time', '>', start_time)
        ])

        if conflicting_shifts:
            raise Warning(_('Employee is already allocated in a conflicting shift'))

        self.create({
            'employee_id': employee_id,
            'start_time': start_time,
            'end_time': end_time
        })

        return True

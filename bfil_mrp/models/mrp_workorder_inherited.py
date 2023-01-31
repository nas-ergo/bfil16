from odoo import api, fields, models


# Creating the model


class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workorder'

    resume_time = fields.Datetime(string='Next resume time',)
    state = fields.Selection(
        selection_add=[
            ('pause', 'Paused'),
        ])

    wc_cost = fields.Float(string='WorkCenter Cost', readonly=True, compute='_compute_wc_cost', store=True)
    @api.depends('time_ids.cost_per_time_interval')
    def _compute_wc_cost(self):
        for rec in self:
            rec.wc_cost = sum(time_interval_cost.cost_per_time_interval for time_interval_cost in rec.time_ids)


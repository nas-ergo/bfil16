from odoo import api, fields, models, _, tools



class MrpRoutingWorkcenter(models.Model):
    _inherit = 'mrp.routing.workcenter'
    cost = fields.Float(string='Total workcenter cost',readonly=True, compute='_compute_cost', store=True)
    wc_cost_per_minute = fields.Float(related='workcenter_id.cost_per_min', string='Work Center Cost(Min)')

    @api.depends('time_cycle','workcenter_id.cost_per_min')
    def _compute_cost(self):
        for record in self:
            record.cost=record.workcenter_id.cost_per_min * record.time_cycle

    @api.depends('cost')
    def _compute_total_cost(self):
        self.ensure_one()
        total=0
        for record in self:
            total+=record.cost
        self.wc_total_cost = total
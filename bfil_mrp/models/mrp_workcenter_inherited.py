from odoo import api, fields, models
from odoo.exceptions import ValidationError
# Creating the model


class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    user_id = fields.Many2one('res.users', string='Responsible person',  required=True)
    total_prod_capacity = fields.Float(string='Total Production Capacity(min)', default=1)
    rental_cost = fields.Float(string='Rental Cost')
    labor_cost = fields.Float(string='Labor Cost')
    common_area_cost = fields.Float(string='Common area cost')
    other_costs = fields.Float(string='Other costs')
    cost_per_min = fields.Float(string='Cost Per Minute', readonly=True, compute='_compute_cost_per_minute', store=True)

    @api.constrains('total_prod_capacity', 'rental_cost', 'labor_cost', 'common_area_cost','other_costs')
    def _check_values(self):
        for record in self:
            if record.total_prod_capacity <1:
                raise ValidationError("Production capacity must be greater than or equal to one ")

            if record.rental_cost < 0:
                raise ValidationError("Rental cost can't be negative")

            if record.labor_cost <0:
                raise ValidationError("Labor cost can't be negative")

            if record.common_area_cost <0:
                raise ValidationError("Common area cost can't be negative")

            if record.other_costs < 0:
                raise ValidationError("Costs can't be negative")



    @api.depends('total_prod_capacity','rental_cost','labor_cost','common_area_cost','other_costs')
    def _compute_cost_per_minute(self):
        for record in self:
            total_cost= (record.common_area_cost+record.rental_cost+record.labor_cost+record.other_costs)/record.total_prod_capacity
            record.cost_per_min = total_cost

    @api.onchange('cost_per_min')
    def change_cost_per_hour(self):
        for rec in self:    
            rec.costs_hour = rec.cost_per_min * 60


class MrpWorkcenterProductivity(models.Model):
    _inherit = 'mrp.workcenter.productivity'
    wc_cost_per_min = fields.Float(string="WC c/min", readonly=True)
    cost_per_time_interval = fields.Float(string='Cost', readonly=True, compute='_compute_cost_for_each_interval', store=True)

    @api.depends('duration')
    def _compute_cost_for_each_interval(self):
        for record in self:
            record.wc_cost_per_min= record.workcenter_id.cost_per_min
            record.cost_per_time_interval= record.duration * record.workcenter_id.cost_per_min

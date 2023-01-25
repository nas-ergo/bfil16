from odoo import api, fields, models
from odoo.exceptions import ValidationError
# Creating the model


class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    user_id = fields.Many2one('res.users', string='Responsible person',  required=True)
    total_prod_capacity = fields.Float(string='Total Production Capacity(min)',default=1)
    rental_cost = fields.Float(string='Rental Cost')
    labor_cost = fields.Float(string='Labor Cost')
    common_area_cost = fields.Float(string='Common area cost')
    cost_per_min = fields.Float(string='Cost Per Minute', readonly=True, compute='_compute_cost_per_minute', store=True)

    @api.constrains('total_prod_capacity', 'rental_cost', 'labor_cost', 'common_area_cost')
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



    @api.depends('total_prod_capacity','rental_cost','labor_cost','common_area_cost')
    def _compute_cost_per_minute(self):
        for record in self:
            total_cost= (record.common_area_cost+record.rental_cost+record.labor_cost)/record.total_prod_capacity
            record.cost_per_min = total_cost


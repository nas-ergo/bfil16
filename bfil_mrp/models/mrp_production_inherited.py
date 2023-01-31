from odoo import api, fields, models, _, tools

class MrpProduction(models.Model):

    _inherit = 'mrp.production'
    total_component_cost = fields.Float(string='Total component Cost', readonly=True, store=True,
                                         compute='_compute_total_component_cost')

    total_workcenter_cost = fields.Float(string='Total workcenter Cost', readonly=True, store=True,
                                        compute='_compute_workcenter_component_cost')

    total_cost = fields.Float(string='Overall Cost', readonly=True, store=True,
                              compute='_compute_total_cost')

    @api.depends('move_raw_ids.component_cost')
    def _compute_total_component_cost(self):
        for rec in self:
            rec.total_component_cost = sum(cost.component_cost for cost in rec.move_raw_ids)

    @api.depends('workorder_ids.wc_cost')
    def _compute_workcenter_component_cost(self):
        for rec in self:
            rec.total_workcenter_cost = sum(cost.wc_cost for cost in rec.workorder_ids)

    @api.depends('total_component_cost','total_workcenter_cost')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = record.total_component_cost + record.total_workcenter_cost

    def _get_move_raw_values(self, product_id, product_uom_qty, product_uom, operation_id=False, bom_line=False):
        res = super(MrpProduction, self)._get_move_raw_values(product_id, product_uom_qty, product_uom, operation_id, bom_line)
        res['unit_price'] = product_id.standard_price
        res['component_cost'] = product_uom_qty * product_id.standard_price
        return res

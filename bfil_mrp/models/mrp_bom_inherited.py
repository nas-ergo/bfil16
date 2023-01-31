from odoo import api, fields, models, _, tools


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    cost_per_unit = fields.Float(related='product_id.standard_price', string='Cost/Unit')
    total_cost = fields.Float(string='Total cost', readonly=True, compute='_compute_total_cost', store=True)

    @api.depends('cost_per_unit', 'product_qty')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost=record.product_qty * record.cost_per_unit


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    total_material_cost = fields.Float(string='Total material cost', readonly=True,
                                       compute='_compute_total_material_cost', store=True)
    overall_cost = fields.Float(string='Overall cost', readonly=True, compute='_compute_overall_cost', store=True)
    wc_total_cost = fields.Float(string='Overall workcenter cost', readonly=True, compute='_compute_wc_total_cost', store=True)

    @api.depends('bom_line_ids.total_cost')
    def _compute_total_material_cost(self):
        for rec in self:
            rec.total_material_cost = sum(bom_line.total_cost for bom_line in rec.bom_line_ids)


    @api.depends('operation_ids.cost')
    def _compute_wc_total_cost(self):
        total = 0
        for record in self.operation_ids:
            total += record.cost
        self.wc_total_cost = total

    @api.depends('total_material_cost', 'wc_total_cost')
    def _compute_overall_cost(self):
        for record in self:
            record.overall_cost = record.total_material_cost + record.wc_total_cost

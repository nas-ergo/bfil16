from odoo import api, fields, models, _, tools


class StockMove(models.Model):
    _inherit = 'stock.move'
    component_cost = fields.Float(string='Component Cost')
    unit_price = fields.Float(string='Unit Price', store=True)


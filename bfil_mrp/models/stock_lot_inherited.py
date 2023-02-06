try:
    import qrcode
except ImportError:
    qrcode = None
try:
    import base64
except ImportError:
    base64 = None
from io import BytesIO
from odoo.exceptions import UserError
from odoo import api, fields, models, _, tools

class StockLot(models.Model):
    _inherit = 'stock.lot'

    qr_code_img = fields.Binary('QRcode')
    qr_code = fields.Text(string='QR CODE')
    def generate_qr(self):
        for rec in self:


            if rec.product_id.default_code:
                model_id = rec.product_id.default_code + "(" +rec.product_id.name + ")"

            else:
                model_id = rec.product_id.name

            rec.qr_code = """Welcome to BFIL, where exceptional quality and customer satisfaction come first.
Model No: {} \nLot No: {}\nManufactured By: Bangladesh Furniture Industries Limited (BFIL).""".format(model_id, rec.name)


            if qrcode and base64:

                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=3,
                    border=4,
                )
                if rec.ref:
                    model_id = rec.product_id.name + str(rec.ref)

                else:
                    model_id = rec.product_id.name

                model_sec = "Model No: {}\n".format(model_id)
                lot_sec = "Lot No.: {}\n".format(rec.name)

                qr.add_data("Welcome to BFIL, where exceptional quality and customer satisfaction come first.\n")
                qr.add_data(model_sec)
                qr.add_data(lot_sec)
                qr.add_data("Manufactured By: Bangladesh Furniture Industries Limited (BFIL) ")
                qr.make(fit=True)
                img = qr.make_image()
                temp = BytesIO()
                img.save(temp, format="PNG")
                qr_image = base64.b64encode(temp.getvalue())
                rec.qr_code_img = qr_image
            else:
                raise UserError(_('Necessary Requirements To Run This Operation Is Not Satisfied'))

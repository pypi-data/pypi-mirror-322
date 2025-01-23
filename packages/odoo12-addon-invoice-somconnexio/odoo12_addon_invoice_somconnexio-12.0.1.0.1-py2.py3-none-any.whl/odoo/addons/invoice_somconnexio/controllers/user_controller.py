import base64

from odoo.http import Controller, request, route
from odoo.addons.web.controllers.main import content_disposition, serialize_exception


class UserController(Controller):
    @route(
        ["/web/binary/download_invoice"], auth="user", methods=["GET"], website=False
    )
    @serialize_exception
    def download_invoice(self, invoice_number, **kw):
        try:
            invoice_base64 = request.env["download.invoice"].download_invoice_pdf(
                invoice_number
            )
            file_content = base64.b64decode(invoice_base64)
        except Exception:
            return request.not_found()
        if not file_content:
            return request.not_found()
        else:
            filename = "{}.pdf".format(invoice_number)
            return request.make_response(
                file_content,
                [
                    ("Content-Type", "application/octet-stream"),
                    ("Content-Disposition", content_disposition(filename)),
                ],
            )

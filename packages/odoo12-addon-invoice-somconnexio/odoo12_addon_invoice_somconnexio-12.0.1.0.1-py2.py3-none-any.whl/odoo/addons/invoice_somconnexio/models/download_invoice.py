from pyopencell.resources.invoice import Invoice

from odoo.models import AbstractModel

from ..backblaze.b2_service import B2Service


class DownloadInvoice(AbstractModel):
    _register = True
    _name = "download.invoice"

    def download_invoice_pdf(self, invoice_number):
        invoice = self.env["account.invoice"].search(
            ["|", ("name", "=", invoice_number), ("number", "=", invoice_number)],
            limit=1,
        )
        if invoice.b2_file_id:
            invoice_base64 = B2Service().get_pdf_invoice(invoice.b2_file_id)
        else:
            invoice_base64 = Invoice.getInvoicePdfByNumber(invoice_number)
        return invoice_base64

import os
import urllib

from odoo.models import AbstractModel

from odoo.addons.queue_job.job import job
from odoo.addons.somconnexio.somoffice.user import SomOfficeUser


class SendTokenizedInvoice(AbstractModel):
    _register = True
    _name = "send.tokenized.invoice"

    @job
    def send_tokenized_invoice(self, record):
        token_response = SomOfficeUser(
            record.partner_id.ref,
            record.partner_id.email,
            record.partner_id.vat,
            record.partner_id.lang,
            self.env,
        ).generate_invoice_token(record.id)
        base_url = urllib.parse.urljoin(os.getenv("SOMOFFICE_URL"), "invoice")
        record.invoice_tokenized_url = "{}/{}?locale={}".format(
            base_url,
            token_response["invoice_token"],
            record.partner_id.lang.split("_")[0],
        )
        record.company_id.customer_invoice_mail_template_id.send_mail(record.id, False)

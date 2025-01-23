from odoo import models, api


class Contract(models.Model):
    _inherit = "contract.contract"

    @api.multi
    def _get_related_invoices(self):
        self.ensure_one()
        invoices = super()._get_related_invoices()
        invoices += (
            self.env["contract.account.invoice.line.relation"]
            .search([("contract_id", "=", self.id)])
            .mapped("account_invoice_line_id")
            .mapped("invoice_id")
        )
        return invoices

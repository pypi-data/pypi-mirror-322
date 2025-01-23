from . import schemas
from odoo.fields import Date
from odoo.exceptions import MissingError
from odoo.addons.base_rest import restapi
from werkzeug.exceptions import BadRequest
from odoo.addons.component.core import Component
from odoo.addons.base_rest.http import wrapJsonException
from odoo.addons.base_rest.components.service import skip_secure_params
from odoo.addons.base_rest.components.service import skip_secure_response


MANY_INVOICES = 500
ORDER = "date_invoice"
DESCENDENT = "DESCENDENT"


class AccountInvoiceService(Component):
    _inherit = "account.invoice.service"

    @skip_secure_response
    @skip_secure_params
    def create(self, **params):
        self.env["account.invoice"].with_delay(priority=30).create_invoice(**params)
        return {"result": "OK"}

    @skip_secure_response
    @skip_secure_params
    @restapi.method(
        [(["/update-pdf-file-id"], "PUT")],
    )
    def update_pdf_file_id(self, invoice_number, file_id):
        invoice = self.env["account.invoice"].search([("number", "=", invoice_number)])
        if not invoice.exists():
            raise MissingError(("No invoice could be found"))

        invoice.b2_file_id = file_id
        return {"result": "OK"}

    def search(self, **params):
        limit, offset, sortBy, sortOrder = self._get_paging_params(**params)
        domain, search_param = self._get_search_domain(**params)

        invoices = (
            self.env["account.invoice"]
            .sudo()
            .search(domain, limit=limit, offset=offset, order=sortBy + sortOrder)
        )

        if not invoices:
            raise MissingError(
                (
                    "No invoices with {}: {} could be found".format(
                        search_param, params.get(search_param)
                    )
                )
            )

        ret = {"invoices": [self._invoice_to_dict(invoice) for invoice in invoices]}
        self._paging_to_dit(ret, domain, **params)
        return ret

    def get(self, _id):
        invoice = self.env["account.invoice"].sudo().browse(_id)
        if not invoice.exists():
            raise MissingError(("No invoice could be found"))
        ret = self._invoice_to_dict(invoice)
        self._get_invoice_pdf(ret, invoice)
        return ret

    def _validator_search(self):
        return schemas.S_INVOICE_SEARCH

    def _validator_return_get(self):
        return schemas.S_INVOICE_RETURN_GET

    def _validator_return_search(self):
        return schemas.S_INVOICE_RETURN_SEARCH

    def _get_search_domain(self, **params):
        customer_ref = params.get("customer_ref")
        partner_vat = params.get("partner_vat")
        if customer_ref:
            return [("partner_id.ref", "=", customer_ref)], "customer_ref"
        if partner_vat:
            return [
                ("partner_id.vat", "=", partner_vat),
                ("partner_id.parent_id", "=", False),
            ], "partner_vat"
        raise wrapJsonException(
            BadRequest("customer_ref or partner_vat, must be informed"),
            include_description=True,
        )

    def _get_paging_params(self, **params):
        limit = params.get("limit", MANY_INVOICES)
        offset = params.get("offset", 0)
        sortBy = params.get("sortBy", ORDER)
        sortOrder = params.get("sortOrder", DESCENDENT)
        if limit:
            if isinstance(limit, int) or isinstance(limit, str) and limit.isdigit():
                limit = int(limit)
            else:
                raise wrapJsonException(
                    BadRequest("Limit must be numeric"),
                    include_description=True,
                )
        if offset:
            if isinstance(offset, int) or isinstance(offset, str) and offset.isdigit():
                offset = int(offset)
            else:
                raise wrapJsonException(
                    BadRequest("Offset must be numeric"),
                    include_description=True,
                )
        if sortBy:
            if sortBy not in self.env["account.invoice"].fields_get():
                raise wrapJsonException(
                    BadRequest("Invalid field to sortBy"), include_description=True
                )
        if sortOrder:
            if sortOrder == "ASCENDENT":
                sortOrder = " ASC"
            elif sortOrder == "DESCENDENT":
                sortOrder = " DESC"
            else:
                raise wrapJsonException(
                    BadRequest("sortOrder must be ASCENDENT or DESCENDENT"),
                    include_description=True,
                )

        return limit, offset, sortBy, sortOrder

    def _invoice_to_dict(self, invoice):
        invoice.ensure_one()
        return {
            "id": invoice.id,
            "name": invoice.name or invoice.number,
            "date": Date.to_string((invoice.date_invoice)),
            "total_amount": invoice.amount_total,
            "tax_amount": invoice.amount_tax,
            "base_amount": invoice.amount_untaxed,
            "status": invoice.state,
        }

    def _paging_to_dit(
        self, ret, domain, limit=None, offset=None, sortBy=None, sortOrder=None, **_
    ):
        if limit or offset or sortBy:
            ret["paging"] = {
                "limit": int(limit or MANY_INVOICES),
                "offset": int(offset or 0),
                "totalNumberOfRecords": self.env["account.invoice"]
                .sudo()
                .search_count(domain),
            }
            if sortBy:
                ret["paging"].update(
                    {"sortBy": sortBy, "sortOrder": sortOrder or DESCENDENT}
                )

    def _get_invoice_pdf(self, ret, invoice):
        invoice_pdf_base64 = self.env["download.invoice"].download_invoice_pdf(
            invoice.name or invoice.number
        )
        ret["pdf"] = invoice_pdf_base64

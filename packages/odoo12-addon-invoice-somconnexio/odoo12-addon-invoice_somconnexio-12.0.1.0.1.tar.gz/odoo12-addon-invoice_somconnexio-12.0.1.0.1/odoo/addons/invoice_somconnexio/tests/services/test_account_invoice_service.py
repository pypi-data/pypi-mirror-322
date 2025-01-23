import json

import odoo
from mock import patch
from odoo.addons.somconnexio.tests.common_service import BaseEMCRestCaseAdmin
from ...services.account_invoice_service import MANY_INVOICES, DESCENDENT

HOST = "127.0.0.1"
PORT = odoo.tools.config["http_port"]


class InvoiceServiceRestCase(BaseEMCRestCaseAdmin):
    def setUp(self):
        super().setUp()
        self.url = "/api/invoice"
        self.partner = self.browse_ref("somconnexio.res_partner_1_demo")
        self.invoice = self.browse_ref("invoice_somconnexio.invoice_bi_demo")
        self.invoice_oc = self.browse_ref("invoice_somconnexio.invoice_oc_demo")
        self.total_partmer_test_invoices = (
            self.env["account.invoice"]
            .sudo()
            .search_count([("partner_id.ref", "=", self.partner.ref)])
        )

    def http_post(self, data, headers=None):
        headers = self._add_api_key(headers)
        if self.url.startswith("/"):
            url = "http://{}:{}{}".format(HOST, PORT, self.url)
        return self.session.request("POST", url, data=data, headers=headers)

    def http_put(self, data, path="", headers=None):
        headers = self._add_api_key(headers)
        if self.url.startswith("/"):
            url = "http://{}:{}{}".format(HOST, PORT, "{}{}".format(self.url, path))
        return self.session.request("PUT", url, data=data, headers=headers)

    def test_route_right_create(self):
        data = {"fake": "data"}
        response = self.http_post(data=data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})

        jobs_domain = [
            ("method_name", "=", "create_invoice"),
            ("model_name", "=", "account.invoice"),
        ]
        queued_jobs = self.env["queue.job"].search(jobs_domain)

        self.assertEquals(1, len(queued_jobs))

    def test_route_right_update_pdf_file_id(self):
        new_file_id = "2"
        data = {"invoice_number": self.invoice.number, "file_id": new_file_id}
        response = self.http_put(
            data=json.dumps(data),
            path="/update-pdf-file-id",
            headers={
                "Content-Type": "application/json",
            },
        )
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(decoded_response, {"result": "OK"})

        jobs_domain = [
            ("method_name", "=", "send_tokenized_invoice"),
            ("model_name", "=", "send.tokenized.invoice"),
        ]
        queued_jobs = self.env["queue.job"].search(jobs_domain)

        self.assertEquals(1, len(queued_jobs))

    @odoo.tools.mute_logger("odoo.addons.auth_api_key.models.ir_http")
    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_invoices_search_without_auth(self):
        response = self.http_get_without_auth()

        self.assertEquals(response.status_code, 403)
        self.assertEquals(response.reason, "FORBIDDEN")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_invoices_search_unknown_parameter(self):
        url = "{}?{}={}".format(self.url, "unknown_parameter", "2828")
        response = self.http_get(url)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.reason, "BAD REQUEST")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_invoices_search_multiple_parameters(self):
        url = "{}?{}={}&{}={}".format(
            self.url, "customer_ref", "111111", "partner_vat", "1828028"
        )
        response = self.http_get(url)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.reason, "BAD REQUEST")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_invoices_customer_ref_not_found(self):
        url = "{}?{}={}".format(self.url, "customer_ref", "111111")
        response = self.http_get(url)

        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.reason, "NOT FOUND")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_invoices_partner_vat_not_found(self):
        url = "{}?{}={}".format(self.url, "partner_vat", "111111")
        response = self.http_get(url)
        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.reason, "NOT FOUND")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_invoice_id_not_found(self):
        url = "{}/{}".format(self.url, "999")
        response = self.http_get(url)
        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.reason, "NOT FOUND")

    def test_route_invoices_customer_ref_ok(self):
        url = "{}?{}={}".format(self.url, "customer_ref", self.partner.ref)
        response = self.http_get(url)

        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))
        self.assertTrue(result["invoices"])
        self.assertEqual(len(result["invoices"]), len(self.partner.invoice_ids))

    def test_route_invoices_partner_vat_ok(self):
        url = "{}?{}={}".format(self.url, "partner_vat", self.partner.vat)
        response = self.http_get(url)

        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))
        self.assertEqual(len(result["invoices"]), len(self.partner.invoice_ids))

    @patch(
        "odoo.addons.invoice_somconnexio.models.download_invoice.DownloadInvoice.download_invoice_pdf"  # noqa
    )
    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_invoice_id_ok(self, mock_download):
        mock_download.return_value = "pdf"
        url = "{}/{}".format(self.url, self.invoice.id)
        response = self.http_get(url)

        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))
        mock_download.assert_called_once_with(self.invoice.number)
        self._assert_invoice_to_dict(result)
        self.assertEquals(result["name"], self.invoice.number)
        self.assertEquals(result["pdf"], mock_download.return_value)

    @patch(
        "odoo.addons.invoice_somconnexio.models.download_invoice.DownloadInvoice.download_invoice_pdf"  # noqa
    )
    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_invoice_oc_id_ok(self, mock_download):
        mock_download.return_value = "pdf"
        url = "{}/{}".format(self.url, self.invoice_oc.id)
        response = self.http_get(url)

        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))
        mock_download.assert_called_once_with(self.invoice_oc.name)
        self.assertEquals(result["name"], self.invoice_oc.name)
        self.assertEquals(result["pdf"], mock_download.return_value)

    def test_route_invoices_pagination_ok(self):
        limit = 1
        offset = 0
        sort = "amount_total"
        order = "ASCENDENT"
        url = "{}?{}={}&{}={}&{}={}&{}={}&{}={}".format(
            self.url,
            "customer_ref",
            self.partner.ref,
            "limit",
            limit,
            "offset",
            offset,
            "sortBy",
            sort,
            "sortOrder",
            order,
        )
        response = self.http_get(url)

        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))
        self.assertEqual(len(result["invoices"]), limit)
        self._assert_paging(limit, offset, sort, order, result)

    def test_route_invoices_sorted_ok(self):
        limit = MANY_INVOICES
        offset = 0
        sort = "amount_total"
        order = DESCENDENT
        url = "{}?{}={}&{}={}".format(
            self.url,
            "customer_ref",
            self.partner.ref,
            "sortBy",
            sort,
        )
        response = self.http_get(url)

        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))
        self.assertEqual(result["invoices"][0]["id"], self.invoice_oc.id)
        self.assertEqual(result["invoices"][1]["id"], self.invoice.id)
        self._assert_paging(limit, offset, sort, order, result)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_invoices_search_partner_vat_pagination_bad_limit(self):
        url = "{}?{}={}&{}={}".format(
            self.url, "partner_vat", self.partner.vat, "limit", "XXX"
        )
        response = self.http_get(url)
        self.assertEquals(response.status_code, 400)
        error_msg = response.json().get("description")
        self.assertRegex(error_msg, "Limit must be numeric")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_invoices_search_partner_vat_pagination_bad_offset(self):
        url = "{}?{}={}&{}={}&{}={}".format(
            self.url, "partner_vat", self.partner.vat, "limit", "1", "offset", "XXX"
        )
        response = self.http_get(url)
        self.assertEquals(response.status_code, 400)
        error_msg = response.json().get("description")
        self.assertRegex(error_msg, "Offset must be numeric")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_invoices_search_partner_vat_bad_sort_by(self):
        url = "{}?{}={}&{}={}".format(
            self.url, "partner_vat", self.partner.vat, "sortBy", "XXX"
        )
        response = self.http_get(url)
        self.assertEquals(response.status_code, 400)
        error_msg = response.json().get("description")
        self.assertRegex(error_msg, "Invalid field to sortBy")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_invoices_search_partner_vat_bad_sort_order(self):
        url = "{}?{}={}&{}={}&{}={}".format(
            self.url,
            "partner_vat",
            self.partner.vat,
            "sortBy",
            "name",
            "sortOrder",
            "XXX",
        )
        response = self.http_get(url)
        self.assertEquals(response.status_code, 400)
        error_msg = response.json().get("description")
        self.assertRegex(error_msg, "sortOrder must be ASCENDENT or DESCENDENT")

    def _assert_invoice_to_dict(self, invoice):
        self.assertEquals(invoice["id"], self.invoice.id)
        self.assertEquals(invoice["date"], str(self.invoice.date_invoice))
        self.assertEquals(invoice["total_amount"], self.invoice.amount_total)
        self.assertEquals(invoice["tax_amount"], self.invoice.amount_tax)
        self.assertEquals(invoice["base_amount"], self.invoice.amount_untaxed)
        self.assertEquals(invoice["status"], self.invoice.state)

    def _assert_paging(self, limit, offset, sort, order, result):
        self.assertEquals(result["paging"]["limit"], limit)
        self.assertEquals(result["paging"]["offset"], offset)
        self.assertEquals(
            result["paging"]["totalNumberOfRecords"], self.total_partmer_test_invoices
        )
        self.assertEquals(result["paging"]["sortBy"], sort)
        self.assertEquals(result["paging"]["sortOrder"], order)

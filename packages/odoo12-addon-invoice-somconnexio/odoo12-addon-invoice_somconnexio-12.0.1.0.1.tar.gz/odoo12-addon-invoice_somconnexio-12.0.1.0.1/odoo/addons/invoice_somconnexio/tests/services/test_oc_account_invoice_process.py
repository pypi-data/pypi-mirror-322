from odoo.addons.somconnexio.tests.sc_test_case import SCTestCase
from datetime import datetime
from ...services.oc_account_invoice_process import (
    OpenCellAccountInvoiceProcess,
)
from werkzeug.exceptions import BadRequest
from odoo.exceptions import UserError


class OpenCellInvoiceProcessCase(SCTestCase):
    def setUp(self):
        super().setUp()
        self.process = OpenCellAccountInvoiceProcess(self.env)
        self.date_invoice = datetime(2021, 1, 31)
        self.partner = self.browse_ref("easy_my_coop.res_partner_cooperator_1_demo")
        self.partner.ref = "12345"
        self.product = self.browse_ref("somconnexio.Fibra100Mb")
        self.price_unit = 41
        self.quantity = 1
        self.account = self.env["account.account"].search([("code", "=", "43000000")])
        self.account_taxes = self.env["account.account"].search(
            [("code", "=", "47700000")]
        )
        self.name = "SO2020-076338"
        self.oc_amount_untaxed = 10.0
        self.oc_amount_taxes = 2.1
        self.tax = self.env["account.tax"].search(
            [("name", "=", "IVA 21% (Servicios)")]
        )
        self.account_tax_group = self.env["account.tax.group"].search(
            [("name", "=", "IVA 21%")]
        )
        self.tax.oc_code = "TAX_HIGH"
        self.landline_account = self.browse_ref("somconnexio.account_sc_70500020")
        self.mobile_account = self.browse_ref("somconnexio.account_sc_70500010")
        self.data = {
            "billingAccountCode": str(self.partner.ref) + "_0",
            "invoiceDate": int(self.date_invoice.timestamp() * 1000),
            "invoiceNumber": self.name,
            "amountWithoutTax": 1.0000000000,
            "amountWithTax": 1.210000000000,
            "amountTax": 0.21,
            "categoryInvoiceAgregates": [
                {
                    "categoryInvoiceCode": "ICAT_CONSUMPTION",
                    "listSubCategoryInvoiceAgregateDto": [
                        {
                            "itemNumber": 749,
                            "accountingCode": "70500010",
                            "description": "Consum de dades incloses a l'abonament",
                            "taxCode": "TAX_HIGH",
                            "taxPercent": 21.000000000000,
                            "quantity": None,
                            "amountWithoutTax": 1.0000000000,
                            "amountWithTax": 1.210000000000,
                            "amountTax": 0.21,
                            "invoiceSubCategoryCode": (
                                "ISCAT_SC_CONSUMPTION_DATA_NAC_INC"
                            ),
                            "userAccountCode": "1808_0",
                            "ratedTransaction": None,
                        }
                    ],
                }
            ],
            "taxAggregates": [
                {
                    "description": "IVA 21%",
                    "amountWithoutTax": 1.00000000000,
                    "amountTax": 0.21000000000,
                    "amountWithTax": 1.21000000000,
                    "taxCode": "TAX_HIGH",
                    "taxPercent": 21.000000000000,
                }
            ],
        }

    def test_right_create(self):
        content = self.process.create(**self.data)
        self.assertIn("id", content)
        invoice = self.env["account.invoice"].browse(content["id"])
        self.assertEquals(invoice.partner_id, self.partner)
        self.assertEquals(invoice.date_invoice, self.date_invoice.date())
        self.assertEquals(invoice.name, self.name)
        self.assertEquals(
            invoice.journal_id,
            self.browse_ref("somconnexio.consumption_invoices_journal"),
        )

    def test_route_wrong_create_bad_account_code(self):
        data = self.data.copy()
        data.update(
            {
                "billingAccountCode": "XXX_0",
            }
        )
        self.assertRaises(UserError, self.process.create, **data)

    def test_route_wrong_create_partner_not_found(self):
        data = self.data.copy()
        data.update(
            {
                "billingAccountCode": "0_0",
            }
        )
        self.assertRaises(BadRequest, self.process.create, **data)

    def test_route_wrong_create_missing_partner_id(self):
        data = self.data.copy()
        del data["billingAccountCode"]
        self.assertRaises(UserError, self.process.create, **data)

    def test_route_wrong_create_missing_date_invoice(self):
        data = self.data.copy()
        del data["invoiceDate"]
        self.assertRaises(UserError, self.process.create, **data)

    def test_route_wrong_create_missing_name(self):
        data = self.data.copy()
        del data["invoiceNumber"]
        self.assertRaises(UserError, self.process.create, **data)

    def test_route_right_create_invoice_lines(self):
        data = self.data.copy()
        data.update(
            {
                "amountWithoutTax": 108.530000000000,
                "amountWithTax": 131.320000000000,
                "amountTax": 22.790000000000,
                "categoryInvoiceAgregates": [
                    {
                        "categoryInvoiceCode": "ICAT_CONSUMPTION",
                        "listSubCategoryInvoiceAgregateDto": [
                            {
                                "itemNumber": 749,
                                "accountingCode": "70500010",
                                "description": "Consum de dades incloses a l'abonament",
                                "taxCode": "TAX_HIGH",
                                "taxPercent": 21.000000000000,
                                "quantity": None,
                                "amountWithoutTax": 0e-12,
                                "amountTax": 0e-12,
                                "amountWithTax": 0e-12,
                                "invoiceSubCategoryCode": (
                                    "ISCAT_SC_CONSUMPTION_DATA_NAC_INC"
                                ),
                                "userAccountCode": "1808_0",
                                "ratedTransaction": None,
                            },
                            {
                                "itemNumber": 216,
                                "accountingCode": "70500010",
                                "description": "Consum de dades no incloses a l'abonament",  # noqa
                                "taxCode": "TAX_HIGH",
                                "taxPercent": 21.000000000000,
                                "quantity": None,
                                "amountWithoutTax": 0e-12,
                                "amountTax": 0e-12,
                                "amountWithTax": 0e-12,
                                "invoiceSubCategoryCode": (
                                    "ISCAT_SC_CONSUMPTION_DATA_NAC_OUT"
                                ),
                                "userAccountCode": "1808_0",
                                "ratedTransaction": None,
                            },
                            {
                                "itemNumber": 1,
                                "accountingCode": "70500010",
                                "description": "SMS nacional",
                                "taxCode": "TAX_HIGH",
                                "taxPercent": 21.000000000000,
                                "quantity": None,
                                "amountWithoutTax": 0.080000000000,
                                "amountTax": 0.020000000000,
                                "amountWithTax": 0.100000000000,
                                "invoiceSubCategoryCode": (
                                    "ISCAT_SC_CONSUMPTION_SMS_NAC"
                                ),
                                "userAccountCode": "1808_0",
                                "ratedTransaction": None,
                            },
                            {
                                "itemNumber": 8,
                                "accountingCode": "70500010",
                                "description": "Trucades a número especial",
                                "taxCode": "TAX_HIGH",
                                "taxPercent": 21.000000000000,
                                "quantity": None,
                                "amountWithoutTax": 5.190000000000,
                                "amountTax": 1.090000000000,
                                "amountWithTax": 6.280000000000,
                                "invoiceSubCategoryCode": (
                                    "ISCAT_SC_CONSUMPTION_VOICE_ESP"
                                ),
                                "userAccountCode": "1808_0",
                                "ratedTransaction": None,
                            },
                            {
                                "itemNumber": 2,
                                "accountingCode": "70500010",
                                "description": "Trucades internacionals",
                                "taxCode": "TAX_HIGH",
                                "taxPercent": 21.000000000000,
                                "quantity": None,
                                "amountWithoutTax": 4.080000000000,
                                "amountTax": 0.860000000000,
                                "amountWithTax": 4.940000000000,
                                "invoiceSubCategoryCode": (
                                    "ISCAT_SC_CONSUMPTION_VOICE_INT"
                                ),
                                "userAccountCode": "1808_0",
                                "ratedTransaction": None,
                            },
                            {
                                "itemNumber": 23,
                                "accountingCode": "70500020",
                                "description": "Consum de veu nacional o UE",
                                "taxCode": "TAX_HIGH",
                                "taxPercent": 21.000000000000,
                                "quantity": None,
                                "amountWithoutTax": 0e-12,
                                "amountTax": 0e-12,
                                "amountWithTax": 0e-12,
                                "invoiceSubCategoryCode": (
                                    "ISCAT_SC_CONSUMPTION_VOICE_NAC_BA"
                                ),
                                "userAccountCode": "1808_0",
                                "ratedTransaction": None,
                            },
                            {
                                "itemNumber": 177,
                                "accountingCode": "70500010",
                                "description": "Consum de veu dins de tarifa",
                                "taxCode": "TAX_HIGH",
                                "taxPercent": 21.000000000000,
                                "quantity": None,
                                "amountWithoutTax": 0e-12,
                                "amountTax": 0e-12,
                                "amountWithTax": 0e-12,
                                "invoiceSubCategoryCode": (
                                    "ISCAT_SC_CONSUMPTION_VOICE_NAC_INC"
                                ),
                                "userAccountCode": "1808_0",
                                "ratedTransaction": None,
                            },
                            {
                                "itemNumber": 20,
                                "accountingCode": "70500010",
                                "description": "Consum de veu fora de tarifa",
                                "taxCode": "TAX_HIGH",
                                "taxPercent": 21.000000000000,
                                "quantity": None,
                                "amountWithoutTax": 0e-12,
                                "amountTax": 0e-12,
                                "amountWithTax": 0e-12,
                                "invoiceSubCategoryCode": (
                                    "ISCAT_SC_CONSUMPTION_VOICE_NAC_OUT"
                                ),
                                "userAccountCode": "1808_0",
                                "ratedTransaction": None,
                            },
                            {
                                "itemNumber": 52,
                                "accountingCode": "70500010",
                                "description": "Trucades entre línies de Som Connexió",
                                "taxCode": "TAX_HIGH",
                                "taxPercent": 21.000000000000,
                                "quantity": None,
                                "amountWithoutTax": 0e-12,
                                "amountTax": 0e-12,
                                "amountWithTax": 0e-12,
                                "invoiceSubCategoryCode": (
                                    "ISCAT_SC_CONSUMPTION_VOICE_SC"
                                ),
                                "userAccountCode": "1808_0",
                                "ratedTransaction": None,
                            },
                        ],
                    },
                    {
                        "categoryInvoiceCode": "ICAT_SUBSCRIPTION",
                        "description": "Subscripcions",
                        "userAccountCode": "1808_0",
                        "itemNumber": 5,
                        "amountWithoutTax": 99.180000000000,
                        "amountTax": 20.830000000000,
                        "amountWithTax": 120.010000000000,
                        "listSubCategoryInvoiceAgregateDto": [
                            {
                                "itemNumber": 2,
                                "accountingCode": "70500020",
                                "description": "Subscripció de banda ampla",
                                "taxCode": "TAX_HIGH",
                                "taxPercent": 21.000000000000,
                                "quantity": None,
                                "amountWithoutTax": 66.950000000000,
                                "amountTax": 14.060000000000,
                                "amountWithTax": 81.010000000000,
                                "invoiceSubCategoryCode": ("ISCAT_SC_SUBSCRIPTION_BA"),
                                "userAccountCode": "1808_0",
                                "ratedTransaction": None,
                            },
                            {
                                "itemNumber": 3,
                                "accountingCode": "70500010",
                                "description": "Subscripció mòbil",
                                "taxCode": "TAX_HIGH",
                                "taxPercent": 21.000000000000,
                                "quantity": None,
                                "amountWithoutTax": 32.230000000000,
                                "amountTax": 6.770000000000,
                                "amountWithTax": 39.000000000000,
                                "invoiceSubCategoryCode": ("ISCAT_SC_SUBSCRIPTION_MOV"),
                                "userAccountCode": "1808_0",
                                "ratedTransaction": None,
                            },
                        ],
                    },
                ],
                "taxAggregates": [
                    {
                        "description": "IVA 21%",
                        "amountWithoutTax": 108.530000000000,
                        "amountTax": 22.790000000000,
                        "amountWithTax": 131.320000000000,
                        "taxCode": "TAX_HIGH",
                        "taxPercent": 21.000000000000,
                    }
                ],
            }
        )
        content = self.process.create(**data)
        self.assertIn("id", content)
        invoice = self.env["account.invoice"].browse(content["id"])
        self.assertEquals(invoice.partner_id, self.partner)
        self.assertEquals(invoice.date_invoice, self.date_invoice.date())
        self.assertEquals(invoice.name, self.name)
        self.assertEquals(
            invoice.journal_id,
            self.browse_ref("somconnexio.consumption_invoices_journal"),
        )
        self.assertTrue(invoice.invoice_line_ids)
        self.assertEquals(len(invoice.invoice_line_ids), 5)
        self.assertEquals(0.08, invoice.invoice_line_ids[0].price_subtotal)
        self.assertEquals(0.08, invoice.invoice_line_ids[0].price_unit)
        self.assertEquals(0.100000000000, invoice.invoice_line_ids[0].price_total)
        self.assertEquals(len(invoice.invoice_line_ids[0].invoice_line_tax_ids), 1)
        self.assertEquals(invoice.invoice_line_ids[0].invoice_line_tax_ids[0], self.tax)
        self.assertEquals(invoice.tax_line_ids[0].tax_id, self.tax)
        self.assertEquals(invoice.tax_line_ids[0].amount, 22.79)
        self.assertEquals(
            invoice.invoice_line_ids[0].product_id,
            self.env["product.product"].search(
                [("default_code", "=", "ISCAT_SC_CONSUMPTION_SMS_NAC")]
            ),
        )

    def test_route_bad_subcategory_code(self):
        data = self.data.copy()
        categoryInvoiceAgregates = data["categoryInvoiceAgregates"][0]
        listSubCategoryInvoiceAgregateDto = categoryInvoiceAgregates[
            "listSubCategoryInvoiceAgregateDto"
        ][0]
        listSubCategoryInvoiceAgregateDto["invoiceSubCategoryCode"] = "XXX"

        categoryInvoiceAgregates["listSubCategoryInvoiceAgregateDto"] = [
            listSubCategoryInvoiceAgregateDto
        ]
        data["categoryInvoiceAgregates"] = [categoryInvoiceAgregates]

        self.assertRaises(BadRequest, self.process.create, **data)

    def test_route_bad_tax_line(self):
        data = self.data.copy()
        categoryInvoiceAgregates = data["categoryInvoiceAgregates"][0]
        listSubCategoryInvoiceAgregateDto = categoryInvoiceAgregates[
            "listSubCategoryInvoiceAgregateDto"
        ][0]
        listSubCategoryInvoiceAgregateDto["taxCode"] = "XXX"
        self.assertRaises(BadRequest, self.process.create, **data)

    def test_route_bad_tax_line_aggregate(self):
        data = self.data.copy()
        taxAggregates = data["taxAggregates"][0]
        taxAggregates["taxCode"] = "XXX"
        self.assertRaises(BadRequest, self.process.create, **data)

    def test_route_right_force_totals(self):
        data = self.data.copy()
        data.update(
            {
                "amountWithoutTax": 1.0100000000,
                "amountWithTax": 1.230000000000,
                "amountTax": 0.22,
            }
        )
        content = self.process.create(**data)
        self.assertIn("id", content)
        invoice = self.env["account.invoice"].browse(content["id"])
        self.assertEquals(invoice.amount_tax, 0.22)
        self.assertEquals(invoice.amount_untaxed, 1.01)
        self.assertEquals(invoice.amount_total, 1.23)
        self.assertEquals(0.21, invoice.invoice_line_ids[0].price_tax)
        self.assertEquals(
            invoice.journal_id,
            self.browse_ref("somconnexio.consumption_invoices_journal"),
        )

    def test_route_wrong_duplicate_name(self):
        self.process.create(**self.data)
        self.assertRaises(UserError, self.process.create, **self.data)

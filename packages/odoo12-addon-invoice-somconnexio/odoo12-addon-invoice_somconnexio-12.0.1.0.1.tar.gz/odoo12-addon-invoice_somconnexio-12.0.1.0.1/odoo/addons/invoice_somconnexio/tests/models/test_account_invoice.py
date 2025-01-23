from odoo.addons.somconnexio.tests.sc_test_case import SCTestCase
from odoo import fields
from odoo.exceptions import UserError


class AccountInvoice(SCTestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

        self.account_invoice_obj = self.env["account.invoice"]
        self.payment_term = self.env.ref("account.account_payment_term_advance")
        self.partner3 = self.env.ref("base.res_partner_3")
        self.product = self.env.ref("product.product_product_5")
        self.quantity = 1
        self.price_unit = 12.0
        self.account_rec1_id = self.browse_ref("invoice_somconnexio.account_demo")
        self.journalrec = self.browse_ref("somconnexio.consumption_invoices_journal")

        invoice_line_data = [
            (
                0,
                0,
                {
                    "product_id": self.product.id,
                    "quantity": 10.0,
                    "account_id": self.env["account.account"]
                    .search(
                        [
                            (
                                "user_type_id",
                                "=",
                                self.env.ref("account.data_account_type_revenue").id,
                            )
                        ],
                        limit=1,
                    )
                    .id,
                    "name": "product test 5",
                    "price_unit": 100.00,
                },
            )
        ]

        self.account_invoice_customer0 = self.account_invoice_obj.create(
            dict(
                name="Test Customer Invoice",
                payment_term_id=self.payment_term.id,
                journal_id=self.journalrec.id,
                partner_id=self.partner3.id,
                account_id=self.account_rec1_id.id,
                invoice_line_ids=invoice_line_data,
            )
        )

    def test_set_cooperator_effective_in_partner_with_share_lines_not_have_effects(
        self,
    ):  # noqa
        share_product = self.browse_ref(
            "somconnexio.cooperator_share_product"
        ).product_variant_id
        partner = self.browse_ref("somconnexio.res_partner_1_demo")
        self.env["share.line"].create(
            {
                "share_number": 1,
                "share_product_id": share_product.id,
                "partner_id": partner.id,
                "share_unit_price": share_product.lst_price,
                "effective_date": fields.Date.today(),
            }
        )
        invoice = self.env["account.invoice"].create(
            {
                "partner_id": partner.id,
            }
        )

        invoice.set_cooperator_effective(None)

        self.assertEqual(len(partner.share_ids), 1)

    def test_customer_invoice(self):
        # I check that Initially customer invoice is in the "Draft" state
        self.assertEquals(self.account_invoice_customer0.state, "draft")

        # I check that there is no move attached to the invoice
        self.assertEquals(len(self.account_invoice_customer0.move_id), 0)

        # I validate invoice by creating on
        self.account_invoice_customer0.action_invoice_open()

        # I check that the invoice state is "Open"
        self.assertEquals(self.account_invoice_customer0.state, "open")

    def test_customer_invoice_archived_journal(self):
        # I check that Initially customer invoice is in the "Draft" state
        self.assertEquals(self.account_invoice_customer0.state, "draft")

        # I check that there is no move attached to the invoice
        self.assertEquals(len(self.account_invoice_customer0.move_id), 0)

        self.account_invoice_customer0.journal_id.active = False
        # I validate invoice by creating on
        self.assertRaises(UserError, self.account_invoice_customer0.action_invoice_open)

    def test_create_right_regular_invoice(self):
        tax_id = (
            self.env["account.tax"].search([("name", "=", "IVA 21% (Servicios)")]).id
        )
        invoice_line_params = {
            "name": self.product.name,
            "product_id": self.product.id,
            "quantity": self.quantity,
            "price_unit": self.price_unit,
            "account_id": self.account_rec1_id.id,
            "invoice_line_tax_ids": [(4, tax_id, 0)],
        }
        invoice_line = self.env["account.invoice.line"].create(invoice_line_params)
        invoice_params = {
            "partner_id": self.partner3.id,
            "date_invoice": "2024-01-12",
            "invoice_line_ids": [(6, 0, [invoice_line.id])],
        }
        invoice = self.account_invoice_obj.create(invoice_params)
        self.env["account.invoice.line"].create(invoice_line_params)
        self.assertEquals(self.product, invoice.invoice_line_ids[0].product_id)
        self.assertEquals(
            self.quantity * self.price_unit, invoice.invoice_line_ids[0].price_subtotal
        )
        self.assertEquals(
            (self.quantity * self.price_unit) * 1.21,
            invoice.invoice_line_ids[0].price_total,
        )
        self.assertEquals(
            (self.quantity * self.price_unit) * 0.21,
            invoice.invoice_line_ids[0].price_tax,
        )
        self.assertEquals(self.account_rec1_id, invoice.invoice_line_ids[0].account_id)
        self.assertEquals(invoice.amount_untaxed, self.quantity * self.price_unit)
        self.assertEquals(
            invoice.amount_total, (self.quantity * self.price_unit) * 1.21
        )

{
    "name": "invoice Som Connexió module",
    "version": "12.0.1.0.1",
    "depends": [
        "somconnexio",
    ],
    "external_dependencies": {
        "python": [
            "b2sdk",
            "bi_sc_client",
            "pyopencell",
        ],
    },
    "author": "Coopdevs Treball SCCL, " "Som Connexió SCCL",
    "website": "https://coopdevs.org",
    "category": "Cooperative management",
    "license": "AGPL-3",
    "data": [
        "data/account_journal.xml",
        "views/account_invoice.xml",
        "views/res_company.xml",
        "wizards/account_invoice_confirm_between_dates/account_invoice_confirm_between_dates.xml",  # noqa
        "wizards/contract_invoice_payment/contract_invoice_payment.xml",
        "wizards/invoice_claim_1_send/invoice_claim_1_send.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [
        "demo/invoice.xml",
    ],
}

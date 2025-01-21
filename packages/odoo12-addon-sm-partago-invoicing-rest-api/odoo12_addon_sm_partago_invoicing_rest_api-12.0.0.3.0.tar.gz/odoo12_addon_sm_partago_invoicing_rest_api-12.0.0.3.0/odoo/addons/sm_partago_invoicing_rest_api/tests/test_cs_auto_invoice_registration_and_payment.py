from unittest.mock import Mock

from odoo.tests.common import TransactionCase
from odoo.tests import tagged
from odoo.addons.sm_partago_invoicing_rest_api.services.cs_invoice_services import CsInvoiceService
from odoo.exceptions import ValidationError

@tagged('post_install', 'sm_partago_invoicing_automatic_registration_and_payment')
class TestCsAutoInvoiceRegistrationAndPayment(TransactionCase):

    def setUp(self):
        super(TestCsAutoInvoiceRegistrationAndPayment, self).setUp()
        self.cs_invoice_service = CsInvoiceService(self)
        self.company = self.env.user.company_id
        journal_customer_invoices = self.env["account.journal"].create({
            "name": "Customer Invoices Test",
            "type": "sale",
            "code": "TINV"
        })
        self.company.cs_app_oneshot_pay_journal_id = journal_customer_invoices.id


    def test_automatic_validation_and_payment_active(self):
        # Preparar
        self.company.cs_app_oneshot_automatic_validation_and_payment = True
        mock_invoice = Mock()
        mock_invoice.amount_total = 100.0
        mock_invoice.date_invoice = '2024-03-20'

        # Executar
        self.cs_invoice_service._set_invoice_as_valid_and_paid(mock_invoice, self.company)

        # Verificar
        mock_invoice.action_invoice_open.assert_called_once()
        mock_invoice.pay_and_reconcile.assert_called_once_with(
            pay_journal=self.company.cs_app_oneshot_pay_journal_id,
            pay_amount=100.0,
            date='2024-03-20'
        )

    def test_automatic_validation_and_payment_inactive(self):
        # Preparar
        self.company.cs_app_oneshot_automatic_validation_and_payment = False
        mock_invoice = Mock()

        # Executar
        self.cs_invoice_service._set_invoice_as_valid_and_paid(mock_invoice, self.company)

        # Verificar
        mock_invoice.action_invoice_open.assert_not_called()
        mock_invoice.pay_and_reconcile.assert_not_called()
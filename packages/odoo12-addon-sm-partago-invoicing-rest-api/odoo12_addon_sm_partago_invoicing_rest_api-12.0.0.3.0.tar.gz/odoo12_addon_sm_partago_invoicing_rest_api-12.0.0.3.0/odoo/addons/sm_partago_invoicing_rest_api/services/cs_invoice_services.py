import json
import logging

from odoo import fields
from . import schemas
from odoo.http import Response
from odoo.tools.translate import _
from odoo.addons.component.core import Component
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class CsInvoiceService(Component):
    _inherit = "base.rest.private_abstract_service"
    _name = "cs.invoice.service"
    _usage = "cs-invoice"
    _description = """
        Invoice Services
    """

    def create(self, **params):
        _logger.info(str(self.work.request.httprequest.headers))
        reference_invoice = self._filter_reference(params.get('reference', ""))
        is_exist_invoice_by_ref = self.env['account.invoice'].search([("name", "=", reference_invoice)])
        if is_exist_invoice_by_ref:
            return Response(
                json.dumps({
                    'message':  _("This order has a previously created invoice"),
                    'id': str(is_exist_invoice_by_ref[0].id),
                }),
                status=202,
                content_type="application/json"
            )
        company = self.env.user.company_id
        create_dict = self._prepare_create(params, company)
        invoice = self.env['account.invoice'].create(create_dict)
        self._set_invoice_as_valid_and_paid(invoice, company)
        invoice.message_post(
            subject="Cs prepayment invoice created from APP",
            body=str(params),
            message_type="notification"
        )
        pdf_url = self._generate_invoice_pdf_url(invoice)
        return Response(
            json.dumps({
                'message': _("Creation ok"),
                'id': str(invoice.id),
                'pdfUrl': pdf_url,
            }),
            status=200,
            content_type="application/json"
        )
    
    def _set_invoice_as_valid_and_paid(self, invoice, company):
        if company.cs_app_oneshot_automatic_validation_and_payment:
            invoice.action_invoice_open()
            invoice.pay_and_reconcile(
                pay_journal=company.cs_app_oneshot_pay_journal_id, 
                pay_amount=invoice.amount_total, 
                date=invoice.date_invoice
                )

    def _generate_invoice_pdf_url(self, invoice):
        # Assegurem que la factura té un token d'accés
        invoice._portal_ensure_token()
        base_url = self.env['ir.config_parameter'].get_param('web.base.url') + f"/my/invoices/{invoice.id}"
        return base_url + f"?access_token={invoice.access_token}&report_type=pdf&download=true"

    def _validator_create(self):
        return schemas.S_CS_INVOICE_CREATE

    def _prepare_create(self, params, company):
        reference_invoice = self._filter_reference(params.get('reference', ""))
        customer = params.get('customer', False)
        if not customer:
            raise ValidationError(_("Customer details must be provided."))
        
        # getting (or creating) the partner for the invoice
        partner_id = self._find_or_create_partner(customer)

        create_dict = {
            'state': 'draft',
            'type': 'out_invoice',
            'name': reference_invoice,
            'journal_id': company.cs_app_oneshot_account_journal_id.id,
            'invoice_email_sent': False,
            'invoice_template': 'cs_app_invoice',
            'payment_mode_id': company.cs_app_oneshot_payment_mode_id.id,
            'partner_id': partner_id.id,
            'date_invoice': params.get('date'),
        }

        items = params.get('items', False)
        if items:
            lines_list = []
            for item in items:
                quantity, price = self._process_price_quantity(item['quantity'], item['price'])
                taxes_l = [(4, tax.id) for tax in company.cs_app_oneshot_product_id.taxes_id]
                lines_list.append((0, 0, {
                    'product_id': company.cs_app_oneshot_product_id.id,
                    'name': item['description'],
                    'price_unit': price,
                    'quantity': quantity,
                    'account_id': company.cs_app_oneshot_product_id.property_account_income_id.id,
                    'account_analytic_id': company.cs_app_oneshot_product_id.income_analytic_account_id.id,
                    'line_type': 'default',
                    'invoice_line_tax_ids': taxes_l,
                }))
            create_dict['invoice_line_ids'] = lines_list

        return create_dict

    def _find_or_create_partner(self, customer=False):
        """
        This function always retrieves a partner based on arguments cs_person_index or customer.
        If no partner was found in the database then it will create one and return it
        """

        #TODO: although this function works, it seems a little messy, it needs some reformatting

        cs_person_index = self._filter_reference(customer.get('reference', ''))
        related_partners = self.env['res.partner'].search([('cs_person_index', '=', cs_person_index)], order="id asc")

        # if no partner were found then we need either email based search or create a new one
        if not related_partners:

            customer_email = customer.get('email')
            
            if customer_email:
                related_partners = self.env['res.partner'].search([('email', '=', customer_email)], order="id asc")
            
            if len(related_partners) > 1:
                raise ValidationError(f"Partner identification error with reference: {cs_person_index}")
            elif not related_partners:
                # Then this means it's their first invoice so we need to create a new partner
                country_id = self.env['res.country'].search([('code', '=', customer.get("country"))], limit=1)

                new_partner_dict = {
                    "name": customer.get("name"),
                    "firstname": customer.get("firstname"),
                    "lastname": customer.get("lastname"),
                    "email": customer.get("email"),
                    "phone": customer.get("phone"),
                    "reference": customer.get("reference"),
                    "street": customer.get("address"),
                    "zip": customer.get("postalCode"),
                    "city": customer.get("city"),
                    "country_id": country_id.id if country_id else False,
                }
                related_partners = self.env["res.partner"].create(new_partner_dict)
            
            related_partners[0].write({'cs_person_index': cs_person_index})
        
        return related_partners[0]

    @staticmethod
    def _filter_reference(reference):
        return reference.replace("T/", '').split('/', maxsplit=1)[0]

    @staticmethod
    def _process_price_quantity(quantity, price):
        """
        If the price is 1 cent and the quantities are greater than 50, multiply cents by the quantity
        return: tuple(quantity, price)
        """
        return 1, (quantity * price)
        # if quantity > 50 and price == 0.01:
        #     return 1, (quantity * price)
        # return quantity, price

    def update_to_paid(self, **params):
        _logger.info("Updating invoice status: " + str(params))

        invoice_id = params.get('id')

        invoice = self.env['account.invoice'].browse(int(invoice_id))
        if not invoice.exists():
            raise ValidationError(f"Invoice with ID {invoice_id} not found.")

        invoice.action_invoice_open()

        payments_vals = {
                'amount': invoice.amount_total,
                'payment_date': fields.Date.today(),
                'payment_type': 'inbound',
                'partner_id': invoice.partner_id.id,
                'partner_type': 'customer',
                'journal_id': invoice.payment_mode_id.fixed_journal_id.id,
                'payment_method_id': invoice.payment_mode_id.payment_method_id.id,
            }
        payment = self.env['account.register.payments'].with_context(active_ids=[invoice.id], active_model='account.invoice').create(payments_vals)
        payment.create_payments()

        return Response(
            json.dumps({
                'message': _("Update invoice to paid ok"),
                'id': invoice_id,
                'new_status': invoice.state,
            }),
            status=200,
            content_type="application/json"
        )

    def _validator_update_to_paid(self):
        return schemas.S_CS_INVOICE_UPDATE

from odoo import fields, models, _


class ResConfigSettings(models.TransientModel):
    """
    general config prepaid invoice (oneshot)
    """
    _inherit = 'res.config.settings'

    # INVOICING
    cs_app_oneshot_payment_mode_id = fields.Many2one(
        related='company_id.cs_app_oneshot_payment_mode_id',
        string=_("Payment mode (for prepayment invoices generated from APP(oneshot))"),
        readonly=False)

    cs_app_oneshot_product_id = fields.Many2one(
        related='company_id.cs_app_oneshot_product_id',
        string=_("Product (for product invoices generated from APP(oneshot))"),
        readonly=False)

    cs_app_oneshot_account_journal_id = fields.Many2one(
        related='company_id.cs_app_oneshot_account_journal_id',
        string=_("Account journal (for account journal invoices generated from APP(oneshot) )"),
        readonly=False)
    
    cs_app_oneshot_pay_journal_id = fields.Many2one(
        related='company_id.cs_app_oneshot_pay_journal_id',
        string=_("Pay journal (for pay journal invoices generated from APP(oneshot) )"),
        readonly=False)
    
    cs_app_oneshot_automatic_validation_and_payment = fields.Boolean(
        related='company_id.cs_app_oneshot_automatic_validation_and_payment',
        string=_("Automatic validation and payment registry (for invoices generated from APP(oneshot)"),
        readonly=False)
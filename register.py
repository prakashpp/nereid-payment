# -*- coding: utf-8 -*-
"""
    register

    A payments register which modules could optionally use to record payment
    details.

    :copyright: © 2011-2012 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.model import ModelWorkflow, ModelSQL, ModelView, fields
from trytond.pyson import Equal, Eval, Not


class Register(ModelSQL, ModelView):
    "Nereid Payemnt Register"
    _name = "nereid.payment.register"
    _description = __doc__

    _rec_name = 'reference'

    # Internal reference like Sale order no that is sent to payment provider
    reference = fields.Char(
        'Reference', required=True, readonly=True, select=1
    )
    # Transaction ID if any generated by the payment provider
    transaction_id = fields.Char('Transaction ID', select=1)

    sale = fields.Many2One('sale.sale', 'Sale', readonly=True, select=1)
    company = fields.Many2One('company.company', 'Company', required=True,
        readonly=True)
    website = fields.Many2One('nereid.website', 'Website', required=True,
        readonly=True)

    # Payment related information

    #: The gateway used
    method = fields.Char('Payment Model', required=True, readonly=True)
    #: A payment product if known, for example: Mastercard
    payment_product = fields.Char('Payment Product', readonly=True)
    amount = fields.Numeric('Amount', required=True, readonly=True)
    currency = fields.Many2One('currency.currency', 'Currency', required=True,
        readonly=True)
    process_status = fields.Char('Process Status', readonly=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('in-progress', 'In Progress'),
        ('failed', 'Failed'),
        ('complete', 'Complete')
    ], 'System Status', readonly=True)
    notes = fields.Text('Notes')
    logs = fields.One2Many(
        'nereid.payment.register.log', 'register', 'Logs', readonly=True
    )


Register()


class RegisterLog(ModelSQL, ModelView):
    "Logs for the paypal notification"
    _name = "nereid.payment.register.log"
    _description = __doc__

    register = fields.Many2One(
        'nereid.payment.register', 'Register', required=True
    )
    message = fields.Text('Message')

RegisterLog()


class Invoice(ModelWorkflow, ModelSQL, ModelView):
    "Add payment register record to sale"
    _name = "account.invoice"

    nereid_payment_register = fields.Many2One(
        'nereid.payment.register', 'Nereid Payment Record',
        states={
            'readonly': Not(Equal(Eval('state'), 'draft')),
        }
    )

Invoice()

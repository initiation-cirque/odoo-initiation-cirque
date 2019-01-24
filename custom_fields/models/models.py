# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CustomSaleOrder(models.Model):
    _inherit = 'sale.order'

    event_date = fields.Datetime(string="Event Date")

    @api.multi
    def _prepare_invoice(self):
        """
        override this private method to pass the event date to invoice.
        """
        res = super(CustomSaleOrder, self)._prepare_invoice()
        res.update({
            'event_date': self.event_date,
            })
        return res


class CustomSaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    @api.multi
    def _create_invoice(self, order, so_line, amount):
        """
        override this private method to pass the event date to invoice.
        """
        invoice = super(CustomSaleAdvancePaymentInv, self)._create_invoice(order, so_line, amount)
        invoice.update({
            'event_date': order.event_date,
            })
        return invoice


class CustomPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    event_date = fields.Datetime(string="Event Date")

    @api.multi
    def action_view_invoice(self):
        """
        override this private method to pass the event date to invoice.
        """
        result = super(CustomPurchaseOrder, self).action_view_invoice()
        result['context']['default_event_date'] = self.event_date
        return result


class CustomAccountInvoice(models.Model):
    _inherit = 'account.invoice'

    event_date = fields.Datetime(string="Event Date")


class CustomCRMLead(models.Model):
    _inherit = 'crm.lead'

    event_date = fields.Datetime(string="Event Date")
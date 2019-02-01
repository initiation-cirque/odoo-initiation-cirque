# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CustomSaleOrder(models.Model):
    _inherit = 'sale.order'

    event_date = fields.Datetime(string="Event Date", default=fields.Datetime.now())

    @api.multi
    def _prepare_invoice(self):
        """
        override this private method to pass the event date to invoice.
        """
        res = super(CustomSaleOrder, self)._prepare_invoice()
        res.update({
            'event_date': self.event_date or fields.Datetime.now(),
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
            'event_date': order.event_date or fields.Datetime.now(),
            })
        return invoice


class CustomPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    event_date = fields.Datetime(string="Event Date", default=fields.Datetime.now())

    @api.multi
    def action_view_invoice(self):
        """
        override this private method to pass the event date to invoice.
        """
        result = super(CustomPurchaseOrder, self).action_view_invoice()
        result['context']['default_event_date'] = self.event_date or fields.Datetime.now()
        return result


class CustomAccountInvoice(models.Model):
    _inherit = 'account.invoice'

    event_date = fields.Datetime(string="Event Date", default=fields.Datetime.now())


class CustomCRMLead(models.Model):
    _inherit = 'crm.lead'

    event_date = fields.Datetime(string="Event Date", default=fields.Datetime.now())


class CustomProcurementRule(models.Model):
    _inherit = 'procurement.rule'

    def _prepare_purchase_order(self, product_id, product_qty, product_uom, origin, values, partner):
        """Inheritted this method to add origin's event date to PO event date"""
        result = super(CustomProcurementRule, self)._prepare_purchase_order(product_id, product_qty, 
                                                        product_uom, origin, values, partner)
        if result['origin']:
            so = self.env['sale.order'].sudo().search([('name', 'ilike', result['origin'])])
            if so:
                result.update({'event_date': so.event_date or False})
        return result

    @api.multi
    def _run_buy(self, product_id, product_qty, product_uom, location_id, name, origin, values):
        """Overridden this method to update the event date for existing PO, if existing PO event date is not set"""
        cache = {}
        suppliers = product_id.seller_ids\
            .filtered(lambda r: (not r.company_id or r.company_id == values['company_id']) and (not r.product_id or r.product_id == product_id))
        if not suppliers:
            msg = _('There is no vendor associated to the product %s. Please define a vendor for this product.') % (product_id.display_name,)
            raise UserError(msg)

        supplier = self._make_po_select_supplier(values, suppliers)
        partner = supplier.name

        domain = self._make_po_get_domain(values, partner)

        if domain in cache:
            po = cache[domain]
        else:
            po = self.env['purchase.order'].sudo().search([dom for dom in domain])
            po = po[0] if po else False
            cache[domain] = po
        if not po:
            vals = self._prepare_purchase_order(product_id, product_qty, product_uom, origin, values, partner)
            company_id = values.get('company_id') and values['company_id'].id or self.env.user.company_id.id
            po = self.env['purchase.order'].with_context(force_company=company_id).sudo().create(vals)
            cache[domain] = po
        elif not po.origin or origin not in po.origin.split(', '):
            if po.origin:
                if origin:
                    po.write({'origin': po.origin + ', ' + origin})
                else:
                    po.write({'origin': po.origin})
            else:
                po.write({'origin': origin})
            # update event date of SO ie. origin if PO event date is not set.
            if not po.event_date:
                so = self.env['sale.order'].sudo().search([('name', 'ilike', origin)])
                if so:
                    po.write({'event_date': so.event_date or False})
        # Create Line
        po_line = False
        for line in po.order_line:
            if line.product_id == product_id and line.product_uom == product_id.uom_po_id:
                if line._merge_in_existing_line(product_id, product_qty, product_uom, location_id, name, origin, values):
                    vals = self._update_purchase_order_line(product_id, product_qty, product_uom, values, line, partner)
                    po_line = line.write(vals)
                    break
        if not po_line:
            vals = self._prepare_purchase_order_line(product_id, product_qty, product_uom, values, po, supplier)
            self.env['purchase.order.line'].sudo().create(vals)
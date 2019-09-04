# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CustomSaleOrder(models.Model):
    _inherit = 'sale.order'

    event_date = fields.Datetime(string="Event Date", default=fields.Datetime.now())

    ipcountryname = fields.Text(string="Geoip Country")
    ipcountryiso = fields.Text(string="Geoip Country ISO")
    ipcity = fields.Text(string="Geoip City")
    source1 = fields.Text(string="Source 1")
    medium1 = fields.Text(string="Medium 1")
    campaign1 = fields.Text(string="Campaign 1")
    url1 = fields.Text(string="Url 1")
    source1_date = fields.Datetime(string="Source Date 1")
    gclid = fields.Text(string="Google Click ID")

    @api.multi
    def _prepare_invoice(self):
        """
        override this private method to pass the event date to invoice.
        """
        res = super(CustomSaleOrder, self)._prepare_invoice()
        res.update({
            'event_date': self.event_date or fields.Datetime.now(),
            
            'ipcountryname': self.ipcountryname,
            'ipcountryiso': self.ipcountryiso,
            'ipcity': self.ipcity,
            'source1': self.source1,
            'source1_date': self.source1_date,
            'medium1': self.medium1,
            'campaign1':self.campaign1,
            'url1':self.url1,
            'gclid':self.gclid
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

            'ipcountryname': order.ipcountryname,
            'ipcountryiso': order.ipcountryiso,
            'ipcity': order.ipcity,
            'source1': order.source1,
            'source1_date': order.source1_date,
            'medium1': order.medium1,
            'campaign1':order.campaign1,
            'url1':order.url1,
            'gclid':order.gclid
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

    ipcountryname = fields.Text(string="Geoip Country")
    ipcountryiso = fields.Text(string="Geoip Country ISO")
    ipcity = fields.Text(string="Geoip City")
    source1 = fields.Text(string="Source 1")
    medium1 = fields.Text(string="Medium 1")
    campaign1 = fields.Text(string="Campaign 1")
    url1 = fields.Text(string="Url 1")
    source1_date = fields.Datetime(string="Source Date 1")
    gclid = fields.Text(string="Google Click ID")

    @api.model
    def create(self,vals):
        """
        override this private method to update the custom fields in sale order to invoice.
        """
        res = super(CustomAccountInvoice,self).create(vals)
        if res.origin:
            sale_order = self.env['sale.order'].search([('name',"ilike",res.origin)])
            if sale_order:
                vals={
                'ipcountryname': sale_order.ipcountryname,
                'ipcountryiso': sale_order.ipcountryiso,
                'ipcity': sale_order.ipcity,
                'source1': sale_order.source1,
                'source1_date': sale_order.source1_date,
                'medium1': sale_order.medium1,
                'campaign1':sale_order.campaign1,
                'url1':sale_order.url1,
                'gclid':sale_order.gclid
                }
                res.update(vals)

        return res


class CustomCRMLead(models.Model):
    _inherit = 'crm.lead'

    event_date = fields.Datetime(string="Event Date", default=fields.Datetime.now())

    ipcountryname = fields.Text(string="Geoip Country")
    ipcountryiso = fields.Text(string="Geoip Country ISO")
    ipcity = fields.Text(string="Geoip City")
    source1 = fields.Text(string="Source 1")
    medium1 = fields.Text(string="Medium 1")
    campaign1 = fields.Text(string="Campaign 1")
    url1 = fields.Text(string="Url 1")
    source1_date = fields.Datetime(string="Source Date 1")
    gclid = fields.Text(string="Google Click ID")


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
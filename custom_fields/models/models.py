# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CustomSaleOrder(models.Model):
    _inherit = 'sale.order'

    event_date = fields.Datetime(string="Event Date")

    ipcountryname = fields.Text(string="Geoip Country")
    ipcountryiso = fields.Text(string="Geoip Country ISO")
    ipcity = fields.Text(string="Geoip City")
    source1 = fields.Text(string="Source 1")
    medium1 = fields.Text(string="Medium 1")
    campaign1 = fields.Text(string="Campaign 1")
    url1 = fields.Text(string="Url 1")
    source1_date = fields.Datetime(string="Source Date 1")
    gclid = fields.Text(string="Google Click ID")

    # ------------- Booking Fields -----------------
    bookingnumber = fields.Char(string="Booking number")

    web_formid = fields.Char(string="Form id")
    web_product = fields.Char(string="Product")
    web_subproduct = fields.Char(string="Subproduct")
    web_price = fields.Char(string="Price")
    web_eventaddress_street = fields.Char(string="Event street")
    web_eventaddress_street2 = fields.Char(string="Event street 2")
    web_eventaddress_city = fields.Char(string="Event city")
    web_eventaddress_zip = fields.Char(string="Event zip")
    web_eventaddress_country = fields.Char(string="Event country")

    # ------------- Extra information fields -----------------

    web_extra_phone = fields.Char(string="Extra phone")
    web_participant_firstname = fields.Char(string="Participant first name")
    web_participant_lastname = fields.Char(string="Participant last name")
    web_participants_firstnames = fields.Char(string="Birthday first names")
    web_dateofbirth = fields.Date(string="Date of birth")
    web_age_year = fields.Char(string="Years")
    web_age_month = fields.Char(string="Months")
    web_age_days = fields.Char(string="Days")
    web_age_year_next = fields.Char(string="NextYears")
    web_health_issue = fields.Text(string="Health issue")
    web_health_issue_details = fields.Text(string="Health issue details")
    web_language = fields.Text(string="Website language")

    # ------------- Message field-----------------
    web_message = fields.Text(string="Message")


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
            'gclid':self.gclid,
            'bookingnumber': self.bookingnumber, 
            'web_formid': self.web_formid, 
            'web_product': self.web_product, 
            'web_subproduct': self.web_subproduct, 
            'web_price': self.web_price, 
            'web_eventaddress_street': self.web_eventaddress_street, 
            'web_eventaddress_street2': self.web_eventaddress_street2, 
            'web_eventaddress_city': self.web_eventaddress_city, 
            'web_eventaddress_zip': self.web_eventaddress_zip, 
            'web_eventaddress_country': self.web_eventaddress_country, 
            'web_extra_phone': self.web_extra_phone, 
            'web_participant_firstname': self.web_participant_firstname, 
            'web_participant_lastname': self.web_participant_lastname, 
            'web_participants_firstnames': self.web_participants_firstnames, 
            'web_dateofbirth': self.web_dateofbirth, 
            'web_age_year': self.web_age_year, 
            'web_age_month': self.web_age_month, 
            'web_age_days': self.web_age_days, 
            'web_age_year_next': self.web_age_year_next, 
            'web_health_issue': self.web_health_issue, 
            'web_health_issue_details': self.web_health_issue_details, 
            'web_language': self.web_language, 
            'web_message': self.web_message,

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
            'gclid':order.gclid,
            'bookingnumber': order.bookingnumber, 
            'web_formid': order.web_formid, 
            'web_product': order.web_product, 
            'web_subproduct': order.web_subproduct, 
            'web_price': order.web_price, 
            'web_eventaddress_street': order.web_eventaddress_street, 
            'web_eventaddress_street2': order.web_eventaddress_street2, 
            'web_eventaddress_city': order.web_eventaddress_city, 
            'web_eventaddress_zip': order.web_eventaddress_zip, 
            'web_eventaddress_country': order.web_eventaddress_country, 
            'web_extra_phone': order.web_extra_phone, 
            'web_participant_firstname': order.web_participant_firstname, 
            'web_participant_lastname': order.web_participant_lastname, 
            'web_participants_firstnames': order.web_participants_firstnames, 
            'web_dateofbirth': order.web_dateofbirth, 
            'web_age_year': order.web_age_year, 
            'web_age_month': order.web_age_month, 
            'web_age_days': order.web_age_days, 
            'web_age_year_next': order.web_age_year_next, 
            'web_health_issue': order.web_health_issue, 
            'web_health_issue_details': order.web_health_issue_details, 
            'web_language': order.web_language, 
            'web_message': order.web_message,
            })
        return invoice


class CustomPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    event_date = fields.Datetime(string="Event Date")
    bookingnumber = fields.Char(string="Booking number")

    @api.multi
    def action_view_invoice(self):
        """
        override this private method to pass the event date to invoice.
        """
        result = super(CustomPurchaseOrder, self).action_view_invoice()
        result['context']['default_event_date'] = self.event_date or fields.Datetime.now()
        result['context']['default_bookingnumber'] = self.bookingnumber or ''
        return result


class CustomAccountInvoice(models.Model):
    _inherit = 'account.invoice'

    event_date = fields.Datetime(string="Event Date")

    ipcountryname = fields.Text(string="Geoip Country")
    ipcountryiso = fields.Text(string="Geoip Country ISO")
    ipcity = fields.Text(string="Geoip City")
    source1 = fields.Text(string="Source 1")
    medium1 = fields.Text(string="Medium 1")
    campaign1 = fields.Text(string="Campaign 1")
    url1 = fields.Text(string="Url 1")
    source1_date = fields.Datetime(string="Source Date 1")
    gclid = fields.Text(string="Google Click ID")

    # ------------- Booking Fields -----------------
    bookingnumber = fields.Char(string="Booking number")

    web_formid = fields.Char(string="Form id")
    web_product = fields.Char(string="Product")
    web_subproduct = fields.Char(string="Subproduct")
    web_price = fields.Char(string="Price")
    web_eventaddress_street = fields.Char(string="Event street")
    web_eventaddress_street2 = fields.Char(string="Event street 2")
    web_eventaddress_city = fields.Char(string="Event city")
    web_eventaddress_zip = fields.Char(string="Event zip")
    web_eventaddress_country = fields.Char(string="Event country")

    # ------------- Extra information fields -----------------

    web_extra_phone = fields.Char(string="Extra phone")
    web_participant_firstname = fields.Char(string="Participant first name")
    web_participant_lastname = fields.Char(string="Participant last name")
    web_participants_firstnames = fields.Char(string="Birthday first names")
    web_dateofbirth = fields.Date(string="Date of birth")
    web_age_year = fields.Char(string="Years")
    web_age_month = fields.Char(string="Months")
    web_age_days = fields.Char(string="Days")
    web_age_year_next = fields.Char(string="NextYears")
    web_health_issue = fields.Text(string="Health issue")
    web_health_issue_details = fields.Text(string="Health issue details")
    web_language = fields.Text(string="Website language")

    # ------------- Message field-----------------
    web_message = fields.Text(string="Message")

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
                'gclid':sale_order.gclid,
                'bookingnumber': sale_order.bookingnumber, 
                'web_formid': sale_order.web_formid, 
                'web_product': sale_order.web_product, 
                'web_subproduct': sale_order.web_subproduct, 
                'web_price': sale_order.web_price, 
                'web_eventaddress_street': sale_order.web_eventaddress_street, 
                'web_eventaddress_street2': sale_order.web_eventaddress_street2, 
                'web_eventaddress_city': sale_order.web_eventaddress_city, 
                'web_eventaddress_zip': sale_order.web_eventaddress_zip, 
                'web_eventaddress_country': sale_order.web_eventaddress_country, 
                'web_extra_phone': sale_order.web_extra_phone, 
                'web_participant_firstname': sale_order.web_participant_firstname, 
                'web_participant_lastname': sale_order.web_participant_lastname, 
                'web_participants_firstnames': sale_order.web_participants_firstnames, 
                'web_dateofbirth': sale_order.web_dateofbirth, 
                'web_age_year': sale_order.web_age_year, 
                'web_age_month': sale_order.web_age_month, 
                'web_age_days': sale_order.web_age_days, 
                'web_age_year_next': sale_order.web_age_year_next, 
                'web_health_issue': sale_order.web_health_issue, 
                'web_health_issue_details': sale_order.web_health_issue_details, 
                'web_language': sale_order.web_language, 
                'web_message': sale_order.web_message,
                }
                res.update(vals)

        return res


class CustomCRMLead(models.Model):
    _inherit = 'crm.lead'

    event_date = fields.Datetime(string="Event Date")

    ipcountryname = fields.Text(string="Geoip Country")
    ipcountryiso = fields.Text(string="Geoip Country ISO")
    ipcity = fields.Text(string="Geoip City")
    source1 = fields.Text(string="Source 1")
    medium1 = fields.Text(string="Medium 1")
    campaign1 = fields.Text(string="Campaign 1")
    url1 = fields.Text(string="Url 1")
    source1_date = fields.Datetime(string="Source Date 1")
    gclid = fields.Text(string="Google Click ID")


    # ------------- Booking Fields -----------------
    bookingnumber = fields.Char(string="Booking number")

    web_formid = fields.Char(string="Form id")
    web_product = fields.Char(string="Product")
    web_subproduct = fields.Char(string="Subproduct")
    web_price = fields.Char(string="Price")
    web_eventaddress_street = fields.Char(string="Event street")
    web_eventaddress_street2 = fields.Char(string="Event street 2")
    web_eventaddress_city = fields.Char(string="Event city")
    web_eventaddress_zip = fields.Char(string="Event zip")
    web_eventaddress_country = fields.Char(string="Event country")

    # ------------- Extra information fields -----------------

    web_extra_phone = fields.Char(string="Extra phone")
    web_participant_firstname = fields.Char(string="Participant first name")
    web_participant_lastname = fields.Char(string="Participant last name")
    web_participants_firstnames = fields.Char(string="Birthday first names")
    web_dateofbirth = fields.Date(string="Date of birth")
    web_age_year = fields.Char(string="Years")
    web_age_month = fields.Char(string="Months")
    web_age_days = fields.Char(string="Days")
    web_age_year_next = fields.Char(string="NextYears")
    web_health_issue = fields.Text(string="Health issue")
    web_health_issue_details = fields.Text(string="Health issue details")
    web_language = fields.Text(string="Website language")

    # ------------- Message field-----------------
    web_message = fields.Text(string="Message")


class CustomProcurementRule(models.Model):
    _inherit = 'procurement.rule'

    def _prepare_purchase_order(self, product_id, product_qty, product_uom, origin, values, partner):
        """Inheritted this method to add origin's event date to PO event date"""
        result = super(CustomProcurementRule, self)._prepare_purchase_order(product_id, product_qty, 
                                                        product_uom, origin, values, partner)
        if result['origin']:
            so = self.env['sale.order'].sudo().search([('name', 'ilike', result['origin'])])
            if so:
                result.update({'event_date': so.event_date or False,
                                'bookingnumber': so.bookingnumber or False})
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
                    po.write({'event_date': so.event_date or False,
                                'bookingnumber': so.bookingnumber or False})
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
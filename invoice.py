#This file is part account_invoice_contact module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields
from trytond.pyson import Eval

__all__ = ['Invoice']
__metaclass__ = PoolMeta

_STATES = {
    'readonly': Eval('state') != 'draft',
}
_DEPENDS = ['state']


class Invoice:
    __name__ = 'account.invoice'
    contact_address = fields.Many2One('party.address', 'Contact Address',
        states=_STATES, depends=['state', 'party'],
        domain=[('party', '=', Eval('party'))])

    def on_change_party(self):
        changes = super(Invoice, self).on_change_party()

        changes['contact_address'] = None
        if self.party:
            contact_address = self.party.address_get(type='contact')
            if contact_address:
                changes['contact_address'] = contact_address.id
                changes['contact_address.rec_name'] = contact_address.rec_name
        return changes
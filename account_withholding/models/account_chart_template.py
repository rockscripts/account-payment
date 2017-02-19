# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api
import logging
_logger = logging.getLogger(__name__)


class WizardMultiChartsAccounts(models.TransientModel):
    _inherit = 'wizard.multi.charts.accounts'

    @api.multi
    def _create_bank_journals_from_o2m(self, company, acc_template_ref):
        """
        Bank - Cash journals are created with this method
        Inherit this function in order to add checks to cash and bank
        journals. This is because usually will be installed before chart loaded
        and they will be disable by default
        """
        res = super(
            WizardMultiChartsAccounts, self)._create_bank_journals_from_o2m(
            company, acc_template_ref)

        # creamos diario para retenciones
        inbound_withholding = self.env.ref(
            'account_withholding.account_payment_method_in_withholding')
        outbound_withholding = self.env.ref(
            'account_withholding.account_payment_method_out_withholding')
        journal = self.env['account.journal'].create({
            'name': 'Retenciones',
            'type': 'cash',
            'company_id': company.id,
            'inbound_payment_method_ids': [
                (4, inbound_withholding.id, None)],
            'outbound_payment_method_ids': [
                (4, outbound_withholding.id, None)],
        })
        # we dont want this journal to have accounts and we can not inherit
        # to avoid creation, so we delete it
        journal.default_credit_account_id.unlink()

        return res
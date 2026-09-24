# -*- coding: utf-8 -*-
"""The liquid glass theme in a real web client, on 20.0 (OWL 3)."""
from odoo.tests import HttpCase, tagged

from odoo.addons.muk_web_theme.tests.test_web_client import READY, wait_for


@tagged('post_install', '-at_install')
class TestLiquidGlassWebClient(HttpCase):

    def test_01_the_apps_sidebar_opens_and_closes(self):
        prepare = """
            for (let i = 0; i < 100 && !document.querySelector('.o_navbar_sidebar_toggle'); i++) {
                await new Promise(r => setTimeout(r, 200));
            }
            document.querySelector('.o_navbar_sidebar_toggle').click();
        """
        code = wait_for(
            "!!document.querySelector('.o_apps_sidebar.o_sidebar_open .o_apps_sidebar_item')",
            "'sidebar: ' + document.querySelector('.o_apps_sidebar')?.className", prepare)
        self.browser_js('/odoo', code, READY, login='admin', timeout=120)

    def test_02_the_form_sits_on_the_glass(self):
        """No light panel behind the chatter, no empty glass bar above each field."""
        partner = self.env['res.partner'].create({'name': 'Glass Co', 'is_company': True})
        action = self.env.ref('contacts.action_contacts')
        condition = """(() => {
            const chatter = document.querySelector('.o-mail-Form-chatter');
            if (!chatter) { return false; }
            const transparent = getComputedStyle(chatter).backgroundColor === 'rgba(0, 0, 0, 0)';
            const visible = (e) => e.offsetWidth > 0 && e.offsetHeight > 0;
            const emptyGlass = [...document.querySelectorAll('.o_form_sheet .o_cell')].filter(c =>
                visible(c) && ![...c.querySelectorAll('*')].some(visible)
                && getComputedStyle(c).backgroundColor !== 'rgba(0, 0, 0, 0)');
            return transparent && emptyGlass.length === 0;
        })()"""
        failure = """'chatter background: ' + getComputedStyle(document.querySelector('.o-mail-Form-chatter')).backgroundColor"""
        self.browser_js('/odoo/action-%s/%s' % (action.id, partner.id), wait_for(condition, failure),
                        READY, login='admin', timeout=120)

# -*- coding: utf-8 -*-
"""The MuK backend theme in a real web client, on 20.0 (OWL 3)."""
from odoo.tests import HttpCase, tagged

READY = "odoo.isReady === true"


def wait_for(condition_js, failure_js, prepare_js='', seconds=25):
    """Run `prepare_js` once, then poll `condition_js` until true or timeout."""
    return """
const deadline = Date.now() + %d;
(async function () {
    %s
    (async function check() {
        if (await (async () => (%s))()) {
            console.log('test successful');
        } else if (Date.now() > deadline) {
            console.error(%s);
        } else {
            setTimeout(check, 200);
        }
    })();
})();
""" % (seconds * 1000, prepare_js, condition_js, failure_js)


@tagged('post_install', '-at_install')
class TestMukWebClient(HttpCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env['res.partner'].create({'name': 'Muk Smoke Co', 'is_company': True})
        cls.partner.message_post(body='A plain comment', message_type='comment')
        cls.env['mail.message'].create({
            'model': 'res.partner', 'res_id': cls.partner.id,
            'message_type': 'tracking', 'body': 'A tracking message',
        })
        cls.action = cls.env.ref('contacts.action_contacts')

    def _form_url(self):
        return '/odoo/action-%s/%s' % (self.action.id, self.partner.id)

    def test_01_the_apps_bar_is_there(self):
        code = wait_for(
            "document.querySelector('.mk_apps_sidebar_panel .mk_apps_sidebar_menu li') && "
            "document.body.className.includes('mk_sidebar_type_')",
            "'apps bar: ' + !!document.querySelector('.mk_apps_sidebar_panel') + ', body: ' + document.body.className")
        self.browser_js('/odoo', code, READY, login='admin', timeout=120)

    def test_02_tracking_messages_can_be_hidden(self):
        prepare = """
            localStorage.setItem('muk_web_chatter.tracking', 'true');
            const text = () => (document.querySelector('.o-mail-Chatter') || {}).textContent || '';
            for (let i = 0; i < 100 && !(text().includes('A tracking message') && document.querySelector('.o_muk_tracking_toggle')); i++) {
                await new Promise(r => setTimeout(r, 200));
            }
            document.querySelector('.o_muk_tracking_toggle').click();
        """
        code = wait_for(
            "(() => { const t = document.querySelector('.o-mail-Chatter').textContent; "
            "return t.includes('A plain comment') && !t.includes('A tracking message'); })()",
            "'chatter still shows: ' + document.querySelector('.o-mail-Chatter')?.textContent.slice(0, 300)",
            prepare)
        self.browser_js(self._form_url(), code, READY, login='admin', timeout=120)

    def test_03_the_chatter_can_be_resized(self):
        code = wait_for("!!document.querySelector('.o-mail-Form-chatter .mk_chatter_resize')",
                        "'no resize handle on the chatter'")
        self.browser_js(self._form_url(), code, READY, login='admin', timeout=120)

    def test_04_a_dialog_toggles_full_screen(self):
        prepare = """
            for (let i = 0; i < 100 && !document.querySelector('.o_form_view .o_field_x2many_list_row_add button, .o_form_view .o-kanban-button-new, .o_form_view button.o_kanban_quick_create'); i++) {
                await new Promise(r => setTimeout(r, 200));
            }
            const add = [...document.querySelectorAll('.o_form_view button')].find(b => /Add|Agregar/.test(b.textContent) && b.closest('.o_field_widget[name=child_ids]'));
            add.click();
            for (let i = 0; i < 100 && !document.querySelector('.modal .mk_btn_dialog_size'); i++) {
                await new Promise(r => setTimeout(r, 200));
            }
            document.querySelector('.modal .mk_btn_dialog_size').click();
        """
        code = wait_for("!!document.querySelector('.modal .modal-dialog.modal-fs')",
                        "'dialog size: ' + document.querySelector('.modal .modal-dialog')?.className",
                        prepare)
        self.browser_js(self._form_url(), code, READY, login='admin', timeout=120)

    def test_05_the_settings_open_with_the_theme_colours(self):
        """The colour fields are read from SCSS when Settings open; that crashed on 20.0
        while muk_web_theme still asked web_editor.assets for them."""
        code = wait_for(
            "!!document.querySelector('.o_setting_container [name=color_brand_light], .o_setting_container [name=theme_color_appsmenu_text]')",
            "'settings: ' + (document.querySelector('.o_error_dialog')?.innerText || 'no colour field').slice(0, 300)")
        self.browser_js('/odoo/settings', code, READY, login='admin', timeout=120)

    def test_06_the_apps_menu_opens(self):
        """MuK's own apps menu; theme_liquid_glass replaces it with a sidebar."""
        if self.env['ir.module.module'].search_count(
                [('name', '=', 'theme_liquid_glass'), ('state', '=', 'installed')]):
            self.skipTest('theme_liquid_glass replaces the apps menu')
        prepare = """
            // The menu closes itself when an action finishes loading
            // (ACTION_MANAGER:UI-UPDATED): open it once the home action is there.
            for (let i = 0; i < 100 && !(document.querySelector('.o_navbar_apps_menu button')
                    && document.querySelector('.o_action_manager > .o_action')); i++) {
                await new Promise(r => setTimeout(r, 200));
            }
            await new Promise(r => setTimeout(r, 500));
            document.querySelector('.o_navbar_apps_menu button').click();
        """
        code = wait_for("!!document.querySelector('.mk_app_menu .o_app')",
                        "'apps menu did not open'", prepare)
        self.browser_js('/odoo', code, READY, login='admin', timeout=120)

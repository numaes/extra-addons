# -*- coding: utf-8 -*-
"""Colours chosen in the settings are written into the SCSS the backend compiles.

[20.0] This went through web_editor's `web_editor.assets`, which no longer exists;
the module carries its own `muk_web_colors.assets`.
"""
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestColors(TransactionCase):

    def _settings(self, **vals):
        settings = self.env['res.config.settings'].create(vals)
        settings.execute()
        return settings

    def test_01_a_light_colour_is_saved_and_read_back(self):
        self._settings(color_brand_light='#123456')
        values = self.env['res.config.settings'].default_get(['color_brand_light'])
        self.assertEqual(values['color_brand_light'], '#123456')
        custom_url = '/_custom/web._assets_primary_variables/muk_web_colors/static/src/scss/colors_light.scss'
        attachment = self.env['ir.attachment'].search([('url', '=', custom_url)])
        self.assertEqual(len(attachment), 1)
        self.assertIn(b'#123456', attachment.raw.content if hasattr(attachment.raw, 'content') else bytes(attachment.raw))
        self.assertTrue(self.env['ir.asset'].search([('path', '=', custom_url)]))

    def test_02_a_dark_colour_goes_to_the_dark_bundle(self):
        self._settings(color_primary_dark='#654321')
        values = self.env['res.config.settings'].default_get(['color_primary_dark'])
        self.assertEqual(values['color_primary_dark'], '#654321')
        self.assertTrue(self.env['ir.attachment'].search([
            ('url', '=', '/_custom/web.assets_web_dark/muk_web_colors/static/src/scss/colors_dark.scss')]))

    def test_03_reset_restores_the_file(self):
        original = self.env['res.config.settings'].default_get(['color_brand_light'])['color_brand_light']
        settings = self._settings(color_brand_light='#abcdef')
        settings.action_reset_light_color_assets()
        self.assertEqual(
            self.env['res.config.settings'].default_get(['color_brand_light'])['color_brand_light'], original)
        self.assertFalse(self.env['ir.attachment'].search([
            ('url', '=', '/_custom/web._assets_primary_variables/muk_web_colors/static/src/scss/colors_light.scss')]))

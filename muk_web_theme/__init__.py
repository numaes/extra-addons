from . import models

from odoo.tools import BinaryBytes, file_open


def _setup_module(env):
    # [20.0] A Binary field takes a BinaryValue: raw bytes wrapped, no base64.
    if env.ref('base.main_company', False):
        with file_open('web/static/img/favicon.ico', 'rb') as file:
            env.ref('base.main_company').write({
                'favicon': BinaryBytes(file.read(), filename='favicon.ico')
            })
        with file_open('muk_web_theme/static/src/img/background.png', 'rb') as file:
            env.ref('base.main_company').write({
                'background_image': BinaryBytes(file.read(), filename='background.png')
            })


def _uninstall_cleanup(env):
    env['res.config.settings']._reset_theme_color_assets()

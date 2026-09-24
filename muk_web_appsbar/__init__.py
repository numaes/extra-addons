from . import models

from odoo.tools import BinaryBytes, file_open


def _setup_module(env):
    # [20.0] A Binary field takes a BinaryValue: raw bytes wrapped, no base64.
    if env.ref('base.main_company', False):
        with file_open('base/static/img/res_company_logo.png', 'rb') as file:
            env.ref('base.main_company').write({
                'appbar_image': BinaryBytes(file.read(), filename='res_company_logo.png')
            })

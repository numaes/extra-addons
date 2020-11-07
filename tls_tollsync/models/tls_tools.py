import logging
import time

import requests

from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)
TIMEOUT = 20


class TollSyncTools(models.AbstractModel):
    _name = 'tls.tools'
    _description = "Toll Sync tools"

    @api.model
    def booster_login(self, login=None, password=None, get_token=None):
        client_login = login or self.get_params(['tls.booster_login'])[0]
        client_pass = password or self.get_params(['tls.booster_password'])[0]
        api_url, use_booster = self.get_params(['tls.booster_api_url', 'tls.use_route_booster'])
        if not all([client_login, client_pass, use_booster]):
            return
        payload = {'username': client_login, 'password': client_pass}
        resp = self.request(F"{api_url}/login", json=payload).json()  # REQUEST
        if resp.get('success') and resp.get('token'):
            _logger.info("Access token received from the Tollsync.eu")
            self.set_params({'tls.booster_token': resp['token']})
            if get_token:
                return resp['token']
            return True
        raise UserError(_("The account for the Tollsync.eu is not configured: {error}").format(error=resp.get('message')))

    @api.model
    def request(self, url, method='post', sleep=0, **kwargs):
        time.sleep(sleep)
        try:
            resp = getattr(requests, method)(url, timeout=TIMEOUT, **kwargs)
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            if e.response.status_code == 401:
                _logger.debug('Access token is empty or has expired')
                return {'status_code': e.response.status_code}
            raise UserError(_("Unable to connect to {url}, received the error: {error}").format(url=url, error=str(e)))
        return resp

    @api.model
    def get_provider(self, code):
        return self.env['tls.toll.provider'].search([('code', '=', code)], limit=1)

    @api.model
    def get_params(self, names):
        param = self.env['ir.config_parameter'].sudo().get_param
        return [True if param(i) == 'True' else param(i) for i in names]

    def set_params(self, vals):
        set_param = self.env['ir.config_parameter'].sudo().set_param
        for param in vals:
            if vals[param] and vals[param] not in self.get_params([param]):
                set_param(param, vals[param])

    def auto_sync(self):
        pass

    def manual_sync(self, count=0, pid=None):
        if pid is not None:
            self.env['tls.toll.provider'].search([('id', '=', pid)]).write({'last_sync': fields.Datetime.now()})
        return count

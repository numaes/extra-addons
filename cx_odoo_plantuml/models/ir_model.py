from odoo import models


#########
# Model #
#########
class Model(models.Model):
    _inherit = "ir.model"

    # -- Get name and inherit
    def is_inherited(self, module_list):
        """
        Check if module is declared earlier in the module list.
        :param  module_list: list of model names (e.g. ['base', 'sale_management'...])
        :return: dict of {model: Inherited} (e.g. {'res.partner': True, 'my.model': False, ...}
        """
        res = {}
        for rec in self:
            inherited = False
            model_modules = rec.get_modules()
            if model_modules:
                for module in module_list:
                    if module in model_modules:
                        inherited = True
                        break
            res.update({rec.model: inherited})
        return res

    # -- Return a set of modules model id present in
    def get_modules(self):
        xml_ids = models.Model._get_external_ids(self)
        module_names = set(xml_id.split('.')[0] for xml_id in xml_ids[self.id])
        return module_names

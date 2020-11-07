odoo.define('tls_tollsync.toll_tree', function (require) {
    "use strict";

    const core = require('web.core');
    const ListController = require('web.ListController');
    const ListView = require('web.ListView');
    const viewRegistry = require('web.view_registry');

    const _t = core._t;

    let TollsListController = ListController.extend({
        buttons_template: 'TollsListView.buttons',
        renderButtons: function () {
            this._super.apply(this, arguments); // Possibly sets this.$buttons
            if (this.$buttons) {
                const self = this;
                this.$buttons.on('click', '.o_button_toll_sync', function () {
                    self._rpc({
                        model: 'tls.tools',
                        method: 'manual_sync',
                        args: [[]]
                    }).then(function (res) {
                        self.do_notify(_t("Fetch completed"), _.str.sprintf(_t("%d records were successfully fetched"), res || 0));
                        self.reload();
                    })
                })
            }
        }
    })

    let TollsListView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: TollsListController
        })
    })

    viewRegistry.add('tls_toll_tree', TollsListView);
})
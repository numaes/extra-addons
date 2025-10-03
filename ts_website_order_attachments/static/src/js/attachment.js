/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.add_attachment = publicWidget.Widget.extend({
    selector: '.div-attached-files',
    events: {
        'click #btn_remove_file': 'RemoveAttchedFile',
    },

     RemoveAttchedFile: function (ev) {
     var attachment_id = ev.target.closest('div')
        rpc("/shop/attachments" , {
            "attachment_id":attachment_id.id
             }).then(function (data) {
                window.location.reload()
        });
        attachment_id.remove();
     },
});

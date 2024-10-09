/** @odoo-module **/
import { bus } from "@bus/services/bus_service";
import { Component,useState, onWillUpdateProps, onWillStart } from "@odoo/owl";
import { useBus, useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { renderToString } from "@web/core/utils/render"
import { _t } from "@web/core/l10n/translation";

export class ColorPickerWidget extends Component {
static template = "ColorPickerWidget";
setup() {
        super.setup();
        this.actionService = useService("action");
        this.dialog = useService("dialog");
        this.notification = useService("notification");
        this.orm = useService("orm");


}
}


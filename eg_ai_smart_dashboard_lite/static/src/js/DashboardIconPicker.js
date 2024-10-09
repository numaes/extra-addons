/** @odoo-module **/
import { bus } from "@bus/services/bus_service";
import { Component,useState, onWillUpdateProps, onWillStart } from "@odoo/owl";
import { useBus, useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { renderToString } from "@web/core/utils/render"
import { _t } from "@web/core/l10n/translation";



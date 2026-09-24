/* @odoo-module */

import { patch } from "@web/core/utils/patch";

import { Chatter } from "@mail/chatter/web_portal_project/chatter";

import { setShowTracking, trackingState } from "../core/tracking_state";

patch(Chatter.prototype, {
    setup() {
        super.setup();
        this.trackingState = trackingState;
    },
    onClickTrackingToggle() {
        setShowTracking(!this.trackingState.show);
    },
});

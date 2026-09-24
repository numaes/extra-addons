/* @odoo-module */

import { patch } from "@web/core/utils/patch";

import { Thread } from "@mail/core/common/thread";

import { trackingState } from "../tracking_state";

patch(Thread.prototype, {
    /**
     * Hide tracking messages in a record's chatter when the user turned them off.
     * Discuss channels are never filtered.
     */
    get orderedMessages() {
        const messages = super.orderedMessages;
        if (trackingState.show || this.props.thread.model === "discuss.channel") {
            return messages;
        }
        return messages.filter((message) => message.message_type !== "tracking");
    },
});

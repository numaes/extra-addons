/* @odoo-module */

import { proxy } from "@odoo/owl";
import { browser } from "@web/core/browser/browser";

const STORAGE_KEY = "muk_web_chatter.tracking";

function readStored() {
    try {
        const stored = browser.localStorage.getItem(STORAGE_KEY);
        return stored != null ? JSON.parse(stored) : true;
    } catch {
        return true;
    }
}

/**
 * Whether the chatter shows tracking messages, shared by the chatter's toggle and
 * the message thread.
 *
 * [20.0] In 18.0 the chatter passed a `showTrackingMessages` prop to Thread, added
 * by extending `Thread.props`. Thread now declares its props inside setup with a
 * strict schema (`useProps`), which cannot be extended, so the two components share
 * this reactive state instead.
 */
export const trackingState = proxy({ show: readStored() });

export function setShowTracking(show) {
    browser.localStorage.setItem(STORAGE_KEY, JSON.stringify(show));
    trackingState.show = show;
}

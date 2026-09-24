/** @odoo-module **/

import { session } from '@web/session';
import { patch } from '@web/core/utils/patch';

import { Dialog } from '@web/core/dialog/dialog';

/**
 * [20.0] The dialog has a size signal of its own (`dialogSize`, read by `this.size`),
 * so the user's "maximize" preference and the size toggle set it, instead of a
 * `data.size` of this module's that the template had to be rewired to read.
 */
patch(Dialog.prototype, {
    setup() {
        super.setup();
        this.mukInitialSize = this.props.size || 'lg';
        if (session.dialog_size === 'maximize') {
            this.dialogSize.set('fs');
        }
    },
    toggleMukDialogSize() {
        this.dialogSize.set(this.size === 'fs' ? this.mukInitialSize : 'fs');
    },
});

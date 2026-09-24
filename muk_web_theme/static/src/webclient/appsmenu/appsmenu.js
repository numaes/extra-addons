/** @odoo-module **/

import { url } from "@web/core/utils/urls";
import { user } from "@web/core/user";
import { useBus, useService } from "@web/core/utils/hooks";

import { Dropdown } from "@web/core/dropdown/dropdown";
import { useLayoutEffect } from "@web/owl2/utils";

export class AppsMenu extends Dropdown {
    setup() {
    	super.setup();
    	this.commandPaletteOpen = false;
        this.commandService = useService("command");
    	if (user.activeCompany.has_background_image) {
            this.imageUrl = url('/web/image', {
                model: 'res.company',
                field: 'background_image',
                id: user.activeCompany.id,
            });
    	} else {
    		this.imageUrl = '/muk_web_theme/static/src/img/background.png';
    	}
        useLayoutEffect(
            (isOpen) => {
            	if (isOpen) {
            		const openMainPalette = (ev) => {
            	    	if (
            	    		!this.commandServiceOpen && 
            	    		ev.key.length === 1 &&
            	    		!ev.ctrlKey &&
            	    		!ev.altKey
            	    	) {
	            	        this.commandService.openMainPalette(
            	        		{ searchValue: `/${ev.key}` }, 
            	        		() => { this.commandPaletteOpen = false; }
            	        	);
	            	    	this.commandPaletteOpen = true;
            	    	}
            		}
	            	window.addEventListener("keydown", openMainPalette);
	                return () => {
	                	window.removeEventListener("keydown", openMainPalette);
	                	this.commandPaletteOpen = false;
	                }
            	}
            },
            () => [this.state.isOpen]
		);
    	useBus(this.env.bus, "ACTION_MANAGER:UI-UPDATED", () => this.state.close());
    }
    onOpened() {
		super.onOpened();
		// [20.0] menuRef is a signal ref: read it by calling it.
		const menu = this.menuRef && this.menuRef();
		if (menu) {
			menu.style.backgroundImage = `url('${this.imageUrl}')`;
		}
    }
}

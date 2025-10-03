/**@odoo-module **/
import { PosStore } from "@point_of_sale/app/services/pos_store";
import { normalize } from "@web/core/l10n/utils";
import { patch } from "@web/core/utils/patch";
patch(PosStore.prototype, {

    // @override
    getProductsBySearchWord(searchWord, products) {
        const words = normalize(searchWord);
        const searchWords = words.toLowerCase().split(/\s+/).filter(word => word.length > 1);

        // Search 1. Exact matches
        const exactMatches = products.filter((product) => product.exactMatch(words));
        if (exactMatches.length > 0 && words.length > 2) {
            return this.sortByWordIndex(exactMatches, words);
        }
        // Search 2. All other matches (full string + split words)
        const matches = products.filter((p) => {
            const productText = normalize(p.searchString).toLowerCase();
            const variantTexts = p.product_variant_ids.flatMap(variant =>
                variant.product_template_variant_value_ids.map(vv => 
                    normalize(vv.name, false).toLowerCase()
                )
            );
            // Full string match
            if (productText.includes(words) || 
                variantTexts.some(variantText => variantText.includes(words))) {
                return true;
            }
            // Split word match - all words must be found
            return searchWords.every(searchWord => {
                return productText.includes(searchWord) || 
                       variantTexts.some(variantText => variantText.includes(searchWord));
            });
        });
        return this.sortByWordIndex(Array.from(new Set([...exactMatches, ...matches])), words);
    }

});

// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
import { DisposableDelegate } from '@lumino/disposable';
import { Signal } from '@lumino/signaling';
export class SearchProviderRegistry {
    constructor() {
        this._changed = new Signal(this);
        this._providerMap = new Map();
    }
    /**
     * Add a provider to the registry.
     *
     * @param key - The provider key.
     * @returns A disposable delegate that, when disposed, deregisters the given search provider
     */
    register(key, provider) {
        this._providerMap.set(key, provider);
        this._changed.emit();
        return new DisposableDelegate(() => {
            this._providerMap.delete(key);
            this._changed.emit();
        });
    }
    /**
     * Returns a matching provider for the widget.
     *
     * @param widget - The widget to search over.
     * @returns the search provider, or undefined if none exists.
     */
    getProviderForWidget(widget) {
        return this._findMatchingProvider(this._providerMap, widget);
    }
    /**
     * Signal that emits when a new search provider has been registered
     * or removed.
     */
    get changed() {
        return this._changed;
    }
    _findMatchingProvider(providerMap, widget) {
        // iterate through all providers and ask each one if it can search on the
        // widget.
        for (const P of providerMap.values()) {
            if (P.canSearchOn(widget)) {
                return new P();
            }
        }
        return undefined;
    }
}
//# sourceMappingURL=searchproviderregistry.js.map
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
import { Signal } from '@lumino/signaling';
/**
 * A console history manager object.
 */
export class ConsoleHistory {
    /**
     * Construct a new console history object.
     */
    constructor(options) {
        this._cursor = 0;
        this._hasSession = false;
        this._history = [];
        this._placeholder = '';
        this._setByHistory = false;
        this._isDisposed = false;
        this._editor = null;
        this._filtered = [];
        this.sessionContext = options.sessionContext;
        void this._handleKernel();
        this.sessionContext.kernelChanged.connect(this._handleKernel, this);
    }
    /**
     * The current editor used by the history manager.
     */
    get editor() {
        return this._editor;
    }
    set editor(value) {
        if (this._editor === value) {
            return;
        }
        const prev = this._editor;
        if (prev) {
            prev.edgeRequested.disconnect(this.onEdgeRequest, this);
            prev.model.value.changed.disconnect(this.onTextChange, this);
        }
        this._editor = value;
        if (value) {
            value.edgeRequested.connect(this.onEdgeRequest, this);
            value.model.value.changed.connect(this.onTextChange, this);
        }
    }
    /**
     * The placeholder text that a history session began with.
     */
    get placeholder() {
        return this._placeholder;
    }
    /**
     * Get whether the console history manager is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources held by the console history manager.
     */
    dispose() {
        this._isDisposed = true;
        this._history.length = 0;
        Signal.clearData(this);
    }
    /**
     * Get the previous item in the console history.
     *
     * @param placeholder - The placeholder string that gets temporarily added
     * to the history only for the duration of one history session. If multiple
     * placeholders are sent within a session, only the first one is accepted.
     *
     * @returns A Promise for console command text or `undefined` if unavailable.
     */
    back(placeholder) {
        if (!this._hasSession) {
            this._hasSession = true;
            this._placeholder = placeholder;
            // Filter the history with the placeholder string.
            this.setFilter(placeholder);
            this._cursor = this._filtered.length - 1;
        }
        --this._cursor;
        this._cursor = Math.max(0, this._cursor);
        const content = this._filtered[this._cursor];
        return Promise.resolve(content);
    }
    /**
     * Get the next item in the console history.
     *
     * @param placeholder - The placeholder string that gets temporarily added
     * to the history only for the duration of one history session. If multiple
     * placeholders are sent within a session, only the first one is accepted.
     *
     * @returns A Promise for console command text or `undefined` if unavailable.
     */
    forward(placeholder) {
        if (!this._hasSession) {
            this._hasSession = true;
            this._placeholder = placeholder;
            // Filter the history with the placeholder string.
            this.setFilter(placeholder);
            this._cursor = this._filtered.length;
        }
        ++this._cursor;
        this._cursor = Math.min(this._filtered.length - 1, this._cursor);
        const content = this._filtered[this._cursor];
        return Promise.resolve(content);
    }
    /**
     * Add a new item to the bottom of history.
     *
     * @param item The item being added to the bottom of history.
     *
     * #### Notes
     * If the item being added is undefined or empty, it is ignored. If the item
     * being added is the same as the last item in history, it is ignored as well
     * so that the console's history will consist of no contiguous repetitions.
     */
    push(item) {
        if (item && item !== this._history[this._history.length - 1]) {
            this._history.push(item);
        }
        this.reset();
    }
    /**
     * Reset the history navigation state, i.e., start a new history session.
     */
    reset() {
        this._cursor = this._history.length;
        this._hasSession = false;
        this._placeholder = '';
    }
    /**
     * Populate the history collection on history reply from a kernel.
     *
     * @param value The kernel message history reply.
     *
     * #### Notes
     * History entries have the shape:
     * [session: number, line: number, input: string]
     * Contiguous duplicates are stripped out of the API response.
     */
    onHistory(value) {
        this._history.length = 0;
        let last = '';
        let current = '';
        if (value.content.status === 'ok') {
            for (let i = 0; i < value.content.history.length; i++) {
                current = value.content.history[i][2];
                if (current !== last) {
                    this._history.push((last = current));
                }
            }
        }
        // Reset the history navigation cursor back to the bottom.
        this._cursor = this._history.length;
    }
    /**
     * Handle a text change signal from the editor.
     */
    onTextChange() {
        if (this._setByHistory) {
            this._setByHistory = false;
            return;
        }
        this.reset();
    }
    /**
     * Handle an edge requested signal.
     */
    onEdgeRequest(editor, location) {
        const model = editor.model;
        const source = model.value.text;
        if (location === 'top' || location === 'topLine') {
            void this.back(source).then(value => {
                if (this.isDisposed || !value) {
                    return;
                }
                if (model.value.text === value) {
                    return;
                }
                this._setByHistory = true;
                model.value.text = value;
                let columnPos = 0;
                columnPos = value.indexOf('\n');
                if (columnPos < 0) {
                    columnPos = value.length;
                }
                editor.setCursorPosition({ line: 0, column: columnPos });
            });
        }
        else {
            void this.forward(source).then(value => {
                if (this.isDisposed) {
                    return;
                }
                const text = value || this.placeholder;
                if (model.value.text === text) {
                    return;
                }
                this._setByHistory = true;
                model.value.text = text;
                const pos = editor.getPositionAt(text.length);
                if (pos) {
                    editor.setCursorPosition(pos);
                }
            });
        }
    }
    /**
     * Handle the current kernel changing.
     */
    async _handleKernel() {
        var _a;
        const kernel = (_a = this.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
        if (!kernel) {
            this._history.length = 0;
            return;
        }
        return kernel.requestHistory(Private.initialRequest).then(v => {
            this.onHistory(v);
        });
    }
    /**
     * Set the filter data.
     *
     * @param filterStr - The string to use when filtering the data.
     */
    setFilter(filterStr = '') {
        // Apply the new filter and remove contiguous duplicates.
        this._filtered.length = 0;
        let last = '';
        let current = '';
        for (let i = 0; i < this._history.length; i++) {
            current = this._history[i];
            if (current !== last &&
                filterStr === current.slice(0, filterStr.length)) {
                this._filtered.push((last = current));
            }
        }
        this._filtered.push(filterStr);
    }
}
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    Private.initialRequest = {
        output: false,
        raw: true,
        hist_access_type: 'tail',
        n: 500
    };
})(Private || (Private = {}));
//# sourceMappingURL=history.js.map
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
import { DataConnector } from '@jupyterlab/statedb';
/**
 * A kernel connector for completion handlers.
 */
export class KernelConnector extends DataConnector {
    /**
     * Create a new kernel connector for completion requests.
     *
     * @param options - The instantiation options for the kernel connector.
     */
    constructor(options) {
        super();
        this._session = options.session;
    }
    /**
     * Fetch completion requests.
     *
     * @param request - The completion request text and details.
     */
    async fetch(request) {
        var _a;
        const kernel = (_a = this._session) === null || _a === void 0 ? void 0 : _a.kernel;
        if (!kernel) {
            throw new Error('No kernel for completion request.');
        }
        const contents = {
            code: request.text,
            cursor_pos: request.offset
        };
        const msg = await kernel.requestComplete(contents);
        const response = msg.content;
        if (response.status !== 'ok') {
            throw new Error('Completion fetch failed to return successfully.');
        }
        return {
            start: response.cursor_start,
            end: response.cursor_end,
            matches: response.matches,
            metadata: response.metadata
        };
    }
}
//# sourceMappingURL=kernelconnector.js.map
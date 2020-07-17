// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
import { DataConnector } from '@jupyterlab/statedb';
/**
 * DummyConnector's fetch method always returns a rejected Promise.
 * This class is only instantiated if both CompletionHandler._connector and
 * CompletionHandler._fetchItems are undefined.
 */
export class DummyConnector extends DataConnector {
    fetch(_) {
        return Promise.reject('Attempting to fetch with DummyConnector. Please ensure connector responseType is set.');
    }
}
//# sourceMappingURL=dummyconnector.js.map
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
import { Signal } from '@lumino/signaling';
import { Logger } from './logger';
/**
 * A concrete implementation of ILoggerRegistry.
 */
export class LoggerRegistry {
    /**
     * Construct a LoggerRegistry.
     *
     * @param defaultRendermime - Default rendermime to render outputs
     * with when logger is not supplied with one.
     */
    constructor(options) {
        this._loggers = new Map();
        this._registryChanged = new Signal(this);
        this._isDisposed = false;
        this._defaultRendermime = options.defaultRendermime;
        this._maxLength = options.maxLength;
    }
    /**
     * Get the logger for the specified source.
     *
     * @param source - The name of the log source.
     *
     * @returns The logger for the specified source.
     */
    getLogger(source) {
        const loggers = this._loggers;
        let logger = loggers.get(source);
        if (logger) {
            return logger;
        }
        logger = new Logger({ source, maxLength: this.maxLength });
        logger.rendermime = this._defaultRendermime;
        loggers.set(source, logger);
        this._registryChanged.emit('append');
        return logger;
    }
    /**
     * Get all loggers registered.
     *
     * @returns The array containing all registered loggers.
     */
    getLoggers() {
        return Array.from(this._loggers.values());
    }
    /**
     * A signal emitted when the logger registry changes.
     */
    get registryChanged() {
        return this._registryChanged;
    }
    /**
     * The max length for loggers.
     */
    get maxLength() {
        return this._maxLength;
    }
    set maxLength(value) {
        this._maxLength = value;
        this._loggers.forEach(logger => {
            logger.maxLength = value;
        });
    }
    /**
     * Whether the register is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose the registry and all loggers.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this._loggers.forEach(x => x.dispose());
        Signal.clearData(this);
    }
}
//# sourceMappingURL=registry.js.map
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
var __rest = (this && this.__rest) || function (s, e) {
    var t = {};
    for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
        t[p] = s[p];
    if (s != null && typeof Object.getOwnPropertySymbols === "function")
        for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) {
            if (e.indexOf(p[i]) < 0 && Object.prototype.propertyIsEnumerable.call(s, p[i]))
                t[p[i]] = s[p[i]];
        }
    return t;
};
import { OutputAreaModel } from '@jupyterlab/outputarea';
import { OutputModel } from '@jupyterlab/rendermime';
import { Signal } from '@lumino/signaling';
/**
 * Log Output Model with timestamp which provides
 * item information for Output Area Model.
 */
export class LogOutputModel extends OutputModel {
    /**
     * Construct a LogOutputModel.
     *
     * @param options - The model initialization options.
     */
    constructor(options) {
        super(options);
        this.timestamp = new Date(options.value.timestamp);
        this.level = options.value.level;
    }
}
/**
 * Implementation of `IContentFactory` for Output Area Model
 * which creates LogOutputModel instances.
 */
class LogConsoleModelContentFactory extends OutputAreaModel.ContentFactory {
    /**
     * Create a rendermime output model from notebook output.
     */
    createOutputModel(options) {
        return new LogOutputModel(options);
    }
}
/**
 * Output Area Model implementation which is able to
 * limit number of outputs stored.
 */
export class LoggerOutputAreaModel extends OutputAreaModel {
    constructor(_a) {
        var { maxLength } = _a, options = __rest(_a, ["maxLength"]);
        super(options);
        this.maxLength = maxLength;
    }
    /**
     * Add an output, which may be combined with previous output.
     *
     * @returns The total number of outputs.
     *
     * #### Notes
     * The output bundle is copied. Contiguous stream outputs of the same `name`
     * are combined. The oldest outputs are possibly removed to ensure the total
     * number of outputs is at most `.maxLength`.
     */
    add(output) {
        super.add(output);
        this._applyMaxLength();
        return this.length;
    }
    /**
     * Whether an output should combine with the previous output.
     *
     * We combine if the two outputs are in the same second, which is the
     * resolution for our time display.
     */
    shouldCombine(options) {
        const { value, lastModel } = options;
        const oldSeconds = Math.trunc(lastModel.timestamp.getTime() / 1000);
        const newSeconds = Math.trunc(value.timestamp / 1000);
        return oldSeconds === newSeconds;
    }
    /**
     * Get an item at the specified index.
     */
    get(index) {
        return super.get(index);
    }
    /**
     * Maximum number of outputs to store in the model.
     */
    get maxLength() {
        return this._maxLength;
    }
    set maxLength(value) {
        this._maxLength = value;
        this._applyMaxLength();
    }
    /**
     * Manually apply length limit.
     */
    _applyMaxLength() {
        if (this.list.length > this._maxLength) {
            this.list.removeRange(0, this.list.length - this._maxLength);
        }
    }
}
/**
 * A concrete implementation of ILogger.
 */
export class Logger {
    /**
     * Construct a Logger.
     *
     * @param source - The name of the log source.
     */
    constructor(options) {
        this._isDisposed = false;
        this._contentChanged = new Signal(this);
        this._stateChanged = new Signal(this);
        this._rendermime = null;
        this._version = 0;
        this._level = 'warning';
        this.source = options.source;
        this.outputAreaModel = new LoggerOutputAreaModel({
            contentFactory: new LogConsoleModelContentFactory(),
            maxLength: options.maxLength
        });
    }
    /**
     * The maximum number of outputs stored.
     *
     * #### Notes
     * Oldest entries will be trimmed to ensure the length is at most
     * `.maxLength`.
     */
    get maxLength() {
        return this.outputAreaModel.maxLength;
    }
    set maxLength(value) {
        this.outputAreaModel.maxLength = value;
    }
    /**
     * The level of outputs logged
     */
    get level() {
        return this._level;
    }
    set level(newValue) {
        const oldValue = this._level;
        if (oldValue === newValue) {
            return;
        }
        this._level = newValue;
        this._log({
            output: {
                output_type: 'display_data',
                data: {
                    'text/plain': `Log level set to ${newValue}`
                }
            },
            level: 'metadata'
        });
        this._stateChanged.emit({ name: 'level', oldValue, newValue });
    }
    /**
     * Number of outputs logged.
     */
    get length() {
        return this.outputAreaModel.length;
    }
    /**
     * A signal emitted when the list of log messages changes.
     */
    get contentChanged() {
        return this._contentChanged;
    }
    /**
     * A signal emitted when the log state changes.
     */
    get stateChanged() {
        return this._stateChanged;
    }
    /**
     * Rendermime to use when rendering outputs logged.
     */
    get rendermime() {
        return this._rendermime;
    }
    set rendermime(value) {
        if (value !== this._rendermime) {
            const oldValue = this._rendermime;
            const newValue = (this._rendermime = value);
            this._stateChanged.emit({ name: 'rendermime', oldValue, newValue });
        }
    }
    /**
     * The number of messages that have ever been stored.
     */
    get version() {
        return this._version;
    }
    /**
     * Log an output to logger.
     *
     * @param log - The output to be logged.
     */
    log(log) {
        // Filter by our current log level
        if (Private.LogLevel[log.level] <
            Private.LogLevel[this._level]) {
            return;
        }
        let output = null;
        switch (log.type) {
            case 'text':
                output = {
                    output_type: 'display_data',
                    data: {
                        'text/plain': log.data
                    }
                };
                break;
            case 'html':
                output = {
                    output_type: 'display_data',
                    data: {
                        'text/html': log.data
                    }
                };
                break;
            case 'output':
                output = log.data;
                break;
            default:
                break;
        }
        if (output) {
            this._log({
                output,
                level: log.level
            });
        }
    }
    /**
     * Clear all outputs logged.
     */
    clear() {
        this.outputAreaModel.clear(false);
        this._contentChanged.emit('clear');
    }
    /**
     * Add a checkpoint to the log.
     */
    checkpoint() {
        this._log({
            output: {
                output_type: 'display_data',
                data: {
                    'text/html': '<hr/>'
                }
            },
            level: 'metadata'
        });
    }
    /**
     * Whether the logger is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose the logger.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this.clear();
        this._rendermime = null;
        Signal.clearData(this);
    }
    _log(options) {
        // First, make sure our version reflects the new message so things
        // triggering from the signals below have the correct version.
        this._version++;
        // Next, trigger any displays of the message
        this.outputAreaModel.add(Object.assign(Object.assign({}, options.output), { timestamp: Date.now(), level: options.level }));
        // Finally, tell people that the message was appended (and possibly
        // already displayed).
        this._contentChanged.emit('append');
    }
}
var Private;
(function (Private) {
    let LogLevel;
    (function (LogLevel) {
        LogLevel[LogLevel["debug"] = 0] = "debug";
        LogLevel[LogLevel["info"] = 1] = "info";
        LogLevel[LogLevel["warning"] = 2] = "warning";
        LogLevel[LogLevel["error"] = 3] = "error";
        LogLevel[LogLevel["critical"] = 4] = "critical";
        LogLevel[LogLevel["metadata"] = 5] = "metadata";
    })(LogLevel = Private.LogLevel || (Private.LogLevel = {}));
})(Private || (Private = {}));
//# sourceMappingURL=logger.js.map
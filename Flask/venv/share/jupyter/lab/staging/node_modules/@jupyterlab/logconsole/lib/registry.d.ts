import { IRenderMimeRegistry } from '@jupyterlab/rendermime';
import { ISignal } from '@lumino/signaling';
import { ILogger, ILoggerRegistry, ILoggerRegistryChange } from './tokens';
/**
 * A concrete implementation of ILoggerRegistry.
 */
export declare class LoggerRegistry implements ILoggerRegistry {
    /**
     * Construct a LoggerRegistry.
     *
     * @param defaultRendermime - Default rendermime to render outputs
     * with when logger is not supplied with one.
     */
    constructor(options: LoggerRegistry.IOptions);
    /**
     * Get the logger for the specified source.
     *
     * @param source - The name of the log source.
     *
     * @returns The logger for the specified source.
     */
    getLogger(source: string): ILogger;
    /**
     * Get all loggers registered.
     *
     * @returns The array containing all registered loggers.
     */
    getLoggers(): ILogger[];
    /**
     * A signal emitted when the logger registry changes.
     */
    get registryChanged(): ISignal<this, ILoggerRegistryChange>;
    /**
     * The max length for loggers.
     */
    get maxLength(): number;
    set maxLength(value: number);
    /**
     * Whether the register is disposed.
     */
    get isDisposed(): boolean;
    /**
     * Dispose the registry and all loggers.
     */
    dispose(): void;
    private _defaultRendermime;
    private _loggers;
    private _maxLength;
    private _registryChanged;
    private _isDisposed;
}
export declare namespace LoggerRegistry {
    interface IOptions {
        defaultRendermime: IRenderMimeRegistry;
        maxLength: number;
    }
}

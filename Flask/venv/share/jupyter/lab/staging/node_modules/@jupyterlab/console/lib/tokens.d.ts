import { IWidgetTracker } from '@jupyterlab/apputils';
import { Token } from '@lumino/coreutils';
import { ConsolePanel } from './panel';
/**
 * The console tracker token.
 */
export declare const IConsoleTracker: Token<IConsoleTracker>;
/**
 * A class that tracks console widgets.
 */
export interface IConsoleTracker extends IWidgetTracker<ConsolePanel> {
}

import { JupyterFrontEndPlugin } from '@jupyterlab/application';
/**
 * A plugin for adding a saving status item to the status bar.
 */
export declare const savingStatusPlugin: JupyterFrontEndPlugin<void>;
/**
 * A plugin providing a file path widget to the status bar.
 */
export declare const pathStatusPlugin: JupyterFrontEndPlugin<void>;
/**
 * Export the plugins as default.
 */
declare const plugins: JupyterFrontEndPlugin<any>[];
export default plugins;

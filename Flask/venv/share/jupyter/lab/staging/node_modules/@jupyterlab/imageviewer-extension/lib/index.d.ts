import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { IImageTracker } from '@jupyterlab/imageviewer';
/**
 * The image file handler extension.
 */
declare const plugin: JupyterFrontEndPlugin<IImageTracker>;
/**
 * Export the plugin as default.
 */
export default plugin;
/**
 * Add the commands for the image widget.
 */
export declare function addCommands(app: JupyterFrontEnd, tracker: IImageTracker): void;

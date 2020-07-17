import { JupyterFrontEndPlugin } from '@jupyterlab/application';
import { IHTMLViewerTracker } from '@jupyterlab/htmlviewer';
/**
 * The HTML file handler extension.
 */
declare const htmlPlugin: JupyterFrontEndPlugin<IHTMLViewerTracker>;
/**
 * Export the plugins as default.
 */
export default htmlPlugin;

import { JupyterFrontEndPlugin } from '@jupyterlab/application';
import { IVDOMTracker } from '@jupyterlab/vdom';
/**
 * The MIME type for VDOM.
 */
export declare const MIME_TYPE = "application/vdom.v1+json";
declare const plugin: JupyterFrontEndPlugin<IVDOMTracker>;
export default plugin;

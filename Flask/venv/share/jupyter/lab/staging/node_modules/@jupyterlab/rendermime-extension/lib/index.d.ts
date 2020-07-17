import { JupyterFrontEndPlugin } from '@jupyterlab/application';
import { IRenderMimeRegistry } from '@jupyterlab/rendermime';
/**
 * A plugin providing a rendermime registry.
 */
declare const plugin: JupyterFrontEndPlugin<IRenderMimeRegistry>;
/**
 * Export the plugin as default.
 */
export default plugin;

import { JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ILauncher } from '@jupyterlab/launcher';
/**
 * A service providing an interface to the the launcher.
 */
declare const plugin: JupyterFrontEndPlugin<ILauncher>;
/**
 * Export the plugin as default.
 */
export default plugin;

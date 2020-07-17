import { JupyterFrontEndPlugin } from '@jupyterlab/application';
import { IMarkdownViewerTracker } from '@jupyterlab/markdownviewer';
/**
 * The markdown viewer plugin.
 */
declare const plugin: JupyterFrontEndPlugin<IMarkdownViewerTracker>;
/**
 * Export the plugin as default.
 */
export default plugin;

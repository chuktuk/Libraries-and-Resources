import { JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ILatexTypesetter } from '@jupyterlab/rendermime';
/**
 * The MathJax latexTypesetter plugin.
 */
declare const plugin: JupyterFrontEndPlugin<ILatexTypesetter>;
/**
 * Export the plugin as default.
 */
export default plugin;

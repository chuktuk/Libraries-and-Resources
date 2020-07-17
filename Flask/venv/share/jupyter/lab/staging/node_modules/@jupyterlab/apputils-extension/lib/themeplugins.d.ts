import { JupyterFrontEndPlugin } from '@jupyterlab/application';
import { IThemeManager } from '@jupyterlab/apputils';
/**
 * The default theme manager provider.
 */
export declare const themesPlugin: JupyterFrontEndPlugin<IThemeManager>;
/**
 * The default theme manager's UI command palette and main menu functionality.
 *
 * #### Notes
 * This plugin loads separately from the theme manager plugin in order to
 * prevent blocking of the theme manager while it waits for the command palette
 * and main menu to become available.
 */
export declare const themesPaletteMenuPlugin: JupyterFrontEndPlugin<void>;

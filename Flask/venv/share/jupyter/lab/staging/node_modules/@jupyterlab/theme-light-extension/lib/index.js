// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
import { IThemeManager } from '@jupyterlab/apputils';
/**
 * A plugin for the Jupyter Light Theme.
 */
const plugin = {
    id: '@jupyterlab/theme-light-extension:plugin',
    requires: [IThemeManager],
    activate: (app, manager) => {
        const style = '@jupyterlab/theme-light-extension/index.css';
        manager.register({
            name: 'JupyterLab Light',
            isLight: true,
            themeScrollbars: false,
            load: () => manager.loadCSS(style),
            unload: () => Promise.resolve(undefined)
        });
    },
    autoStart: true
};
export default plugin;
//# sourceMappingURL=index.js.map
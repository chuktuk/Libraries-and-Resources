// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
import { JupyterLabMenu } from './labmenu';
/**
 * An extensible FileMenu for the application.
 */
export class FileMenu extends JupyterLabMenu {
    constructor(options) {
        super(options);
        this.menu.title.label = 'File';
        this.quitEntry = false;
        // Create the "New" submenu.
        this.newMenu = new JupyterLabMenu(options, false);
        this.newMenu.menu.title.label = 'New';
        this.closeAndCleaners = new Set();
        this.consoleCreators = new Set();
    }
    /**
     * Dispose of the resources held by the file menu.
     */
    dispose() {
        this.newMenu.dispose();
        this.consoleCreators.clear();
        super.dispose();
    }
}
//# sourceMappingURL=file.js.map
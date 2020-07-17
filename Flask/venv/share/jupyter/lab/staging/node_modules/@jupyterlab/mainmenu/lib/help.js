// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
import { JupyterLabMenu } from './labmenu';
/**
 * An extensible Help menu for the application.
 */
export class HelpMenu extends JupyterLabMenu {
    /**
     * Construct the help menu.
     */
    constructor(options) {
        super(options);
        this.menu.title.label = 'Help';
        this.kernelUsers = new Set();
    }
}
//# sourceMappingURL=help.js.map
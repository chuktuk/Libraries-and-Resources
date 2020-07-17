// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
import { JupyterLabMenu } from './labmenu';
/**
 * An extensible Edit menu for the application.
 */
export class EditMenu extends JupyterLabMenu {
    /**
     * Construct the edit menu.
     */
    constructor(options) {
        super(options);
        this.menu.title.label = 'Edit';
        this.undoers = new Set();
        this.clearers = new Set();
        this.goToLiners = new Set();
    }
    /**
     * Dispose of the resources held by the edit menu.
     */
    dispose() {
        this.undoers.clear();
        this.clearers.clear();
        super.dispose();
    }
}
//# sourceMappingURL=edit.js.map
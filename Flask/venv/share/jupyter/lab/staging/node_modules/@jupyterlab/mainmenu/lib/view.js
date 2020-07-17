// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
import { JupyterLabMenu } from './labmenu';
/**
 * An extensible View menu for the application.
 */
export class ViewMenu extends JupyterLabMenu {
    /**
     * Construct the view menu.
     */
    constructor(options) {
        super(options);
        this.menu.title.label = 'View';
        this.editorViewers = new Set();
    }
    /**
     * Dispose of the resources held by the view menu.
     */
    dispose() {
        this.editorViewers.clear();
        super.dispose();
    }
}
//# sourceMappingURL=view.js.map
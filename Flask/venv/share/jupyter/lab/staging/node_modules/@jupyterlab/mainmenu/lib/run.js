// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
import { JupyterLabMenu } from './labmenu';
/**
 * An extensible Run menu for the application.
 */
export class RunMenu extends JupyterLabMenu {
    /**
     * Construct the run menu.
     */
    constructor(options) {
        super(options);
        this.menu.title.label = 'Run';
        this.codeRunners = new Set();
    }
    /**
     * Dispose of the resources held by the run menu.
     */
    dispose() {
        this.codeRunners.clear();
        super.dispose();
    }
}
//# sourceMappingURL=run.js.map
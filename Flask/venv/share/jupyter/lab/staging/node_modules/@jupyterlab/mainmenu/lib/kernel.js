// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
import { JupyterLabMenu } from './labmenu';
/**
 * An extensible Kernel menu for the application.
 */
export class KernelMenu extends JupyterLabMenu {
    /**
     * Construct the kernel menu.
     */
    constructor(options) {
        super(options);
        this.menu.title.label = 'Kernel';
        this.kernelUsers = new Set();
    }
    /**
     * Dispose of the resources held by the kernel menu.
     */
    dispose() {
        this.kernelUsers.clear();
        super.dispose();
    }
}
//# sourceMappingURL=kernel.js.map
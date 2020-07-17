// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
import { JupyterLabMenu } from './labmenu';
/**
 * An extensible Tabs menu for the application.
 */
export class TabsMenu extends JupyterLabMenu {
    /**
     * Construct the tabs menu.
     */
    constructor(options) {
        super(options);
        this.menu.title.label = 'Tabs';
    }
}
//# sourceMappingURL=tabs.js.map
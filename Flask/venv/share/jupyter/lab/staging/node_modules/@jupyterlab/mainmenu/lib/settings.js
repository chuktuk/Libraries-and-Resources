// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
import { JupyterLabMenu } from './labmenu';
/**
 * An extensible Settings menu for the application.
 */
export class SettingsMenu extends JupyterLabMenu {
    /**
     * Construct the settings menu.
     */
    constructor(options) {
        super(options);
        this.menu.title.label = 'Settings';
    }
}
//# sourceMappingURL=settings.js.map
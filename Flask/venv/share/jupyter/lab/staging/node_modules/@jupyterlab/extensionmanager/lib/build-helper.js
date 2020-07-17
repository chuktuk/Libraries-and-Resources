// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
import { Dialog, showDialog } from '@jupyterlab/apputils';
import * as React from 'react';
/**
 * Instruct the server to perform a build
 *
 * @param builder the build manager
 */
export function doBuild(builder) {
    if (builder.isAvailable) {
        return builder
            .build()
            .then(() => {
            return showDialog({
                title: 'Build Complete',
                body: 'Build successfully completed, reload page?',
                buttons: [
                    Dialog.cancelButton(),
                    Dialog.warnButton({ label: 'Reload' })
                ]
            });
        })
            .then(result => {
            if (result.button.accept) {
                location.reload();
            }
        })
            .catch(err => {
            void showDialog({
                title: 'Build Failed',
                body: React.createElement("pre", null, err.message)
            });
        });
    }
    return Promise.resolve();
}
//# sourceMappingURL=build-helper.js.map
import { IWidgetTracker } from '@jupyterlab/apputils';
import { IDocumentWidget } from '@jupyterlab/docregistry';
import { Token } from '@lumino/coreutils';
import { FileEditor } from './widget';
/**
 * A class that tracks editor widgets.
 */
export interface IEditorTracker extends IWidgetTracker<IDocumentWidget<FileEditor>> {
}
/**
 * The editor tracker token.
 */
export declare const IEditorTracker: Token<IEditorTracker>;

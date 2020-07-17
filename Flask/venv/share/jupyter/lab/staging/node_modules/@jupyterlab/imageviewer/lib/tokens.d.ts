import { IWidgetTracker } from '@jupyterlab/apputils';
import { IDocumentWidget } from '@jupyterlab/docregistry';
import { Token } from '@lumino/coreutils';
import { ImageViewer } from './widget';
/**
 * A class that tracks image widgets.
 */
export interface IImageTracker extends IWidgetTracker<IDocumentWidget<ImageViewer>> {
}
/**
 * The image tracker token.
 */
export declare const IImageTracker: Token<IImageTracker>;

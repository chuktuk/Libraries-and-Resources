import { IWidgetTracker } from '@jupyterlab/apputils';
import { Token } from '@lumino/coreutils';
import { MarkdownDocument } from './widget';
/**
 * The markdownviewer tracker token.
 */
export declare const IMarkdownViewerTracker: Token<IMarkdownViewerTracker>;
/**
 * A class that tracks markdown viewer widgets.
 */
export interface IMarkdownViewerTracker extends IWidgetTracker<MarkdownDocument> {
}

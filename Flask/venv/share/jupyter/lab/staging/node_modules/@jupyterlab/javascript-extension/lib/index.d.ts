import { IRenderMime } from '@jupyterlab/rendermime-interfaces';
import { RenderedJavaScript } from '@jupyterlab/rendermime';
export declare const TEXT_JAVASCRIPT_MIMETYPE = "text/javascript";
export declare const APPLICATION_JAVASCRIPT_MIMETYPE = "application/javascript";
export declare class ExperimentalRenderedJavascript extends RenderedJavaScript {
    render(model: IRenderMime.IMimeModel): Promise<void>;
}
/**
 * A mime renderer factory for text/javascript data.
 */
export declare const rendererFactory: IRenderMime.IRendererFactory;
declare const extension: IRenderMime.IExtension;
export default extension;

import { IRenderMime } from '@jupyterlab/rendermime-interfaces';
/**
 * The MathJax Typesetter.
 */
export declare class MathJaxTypesetter implements IRenderMime.ILatexTypesetter {
    /**
     * Create a new MathJax typesetter.
     */
    constructor(options: MathJaxTypesetter.IOptions);
    /**
     * Typeset the math in a node.
     *
     * #### Notes
     * MathJax schedules the typesetting asynchronously,
     * but there are not currently any callbacks or Promises
     * firing when it is done.
     */
    typeset(node: HTMLElement): void;
    /**
     * Initialize MathJax.
     */
    private _init;
    /**
     * Handle MathJax loading.
     */
    private _onLoad;
    private _initPromise;
    private _initialized;
    private _url;
    private _config;
}
/**
 * Namespace for MathJaxTypesetter.
 */
export declare namespace MathJaxTypesetter {
    /**
     * MathJaxTypesetter constructor options.
     */
    interface IOptions {
        /**
         * The url to load MathJax from.
         */
        url: string;
        /**
         * A configuration string to compose into the MathJax URL.
         */
        config: string;
    }
}

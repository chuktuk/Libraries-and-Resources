import { Widget } from '@lumino/widgets';
import { TagTool } from './tool';
/**
 * A widget which hosts a cell tags area.
 */
export declare class TagWidget extends Widget {
    /**
     * Construct a new tag widget.
     */
    constructor(name: string);
    /**
     * Create tag div with icon and attach to this.node.
     */
    buildTag(): void;
    /**
     * Handle `after-attach` messages for the widget.
     */
    onAfterAttach(): void;
    /**
     * Handle `before-detach` messages for the widget.
     */
    onBeforeDetach(): void;
    /**
     * Handle the DOM events for the widget.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the dock panel's node. It should
     * not be called directly by user code.
     */
    handleEvent(event: Event): void;
    /**
     * Handle `update-request` messages. Check if applied to current active cell.
     */
    onUpdateRequest(): void;
    /**
     * Update styling to reflect whether tag is applied to current active cell.
     */
    toggleApplied(): void;
    /**
     * Handle the `'click'` event for the widget.
     */
    private _evtClick;
    /**
     * Handle the `'mouseover'` event for the widget.
     */
    private _evtMouseOver;
    /**
     * Handle the `'mouseout'` event for the widget.
     */
    private _evtMouseOut;
    name: string;
    private applied;
    parent: TagTool | null;
}

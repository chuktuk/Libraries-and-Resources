import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { DataConnector, IDataConnector } from '@jupyterlab/statedb';
/**
 * A data connector for fetching settings.
 *
 * #### Notes
 * This connector adds a query parameter to the base services setting manager.
 */
export declare class SettingConnector extends DataConnector<ISettingRegistry.IPlugin, string> {
    constructor(connector: IDataConnector<ISettingRegistry.IPlugin, string>);
    /**
     * Fetch settings for a plugin.
     * @param id - The plugin ID
     *
     * #### Notes
     * The REST API requests are throttled at one request per plugin per 100ms.
     */
    fetch(id: string): Promise<ISettingRegistry.IPlugin | undefined>;
    list(query?: 'active' | 'all'): Promise<{
        ids: string[];
        values: ISettingRegistry.IPlugin[];
    }>;
    save(id: string, raw: string): Promise<void>;
    private _connector;
    private _throttlers;
}

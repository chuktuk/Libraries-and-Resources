import { Builder } from '@jupyterlab/services';
/**
 * Instruct the server to perform a build
 *
 * @param builder the build manager
 */
export declare function doBuild(builder: Builder.IManager): Promise<void>;

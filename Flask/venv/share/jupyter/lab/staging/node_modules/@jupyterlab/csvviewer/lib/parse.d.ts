/**
 * Interface for a delimiter-separated data parser.
 *
 * @param options: The parser options
 * @returns An object giving the offsets for the rows or columns parsed.
 *
 * #### Notes
 * The parsers are based on [RFC 4180](https://tools.ietf.org/html/rfc4180).
 */
export declare type IParser = (options: IParser.IOptions) => IParser.IResults;
export declare namespace IParser {
    /**
     * The options for a parser.
     */
    interface IOptions {
        /**
         * The data to parse.
         */
        data: string;
        /**
         * Whether to return column offsets in the offsets array.
         *
         * #### Notes
         * If false, the returned offsets array contains just the row offsets. If
         * true, the returned offsets array contains all column offsets for each
         * column in the rows (i.e., it has nrows*ncols entries). Individual rows
         * will have empty columns added or extra columns merged into the last
         * column if they do not have exactly ncols columns.
         */
        columnOffsets: boolean;
        /**
         * The delimiter to use. Defaults to ','.
         */
        delimiter?: string;
        /**
         * The row delimiter to use. Defaults to '\r\n'.
         */
        rowDelimiter?: string;
        /**
         * The quote character for quoting fields. Defaults to the double quote (").
         *
         * #### Notes
         * As specified in [RFC 4180](https://tools.ietf.org/html/rfc4180), quotes
         * are escaped in a quoted field by doubling them (for example, "a""b" is the field
         * a"b).
         */
        quote?: string;
        /**
         * The starting index in the string for processing. Defaults to 0. This
         * index should be the first character of a new row. This must be less than
         * data.length.
         */
        startIndex?: number;
        /**
         * Maximum number of rows to parse.
         *
         * If this is not given, parsing proceeds to the end of the data.
         */
        maxRows?: number;
        /**
         * Number of columns in each row to parse.
         *
         * #### Notes
         * If this is not given, the ncols defaults to the number of columns in the
         * first row.
         */
        ncols?: number;
    }
    /**
     * The results from a parser.
     */
    interface IResults {
        /**
         * The number of rows parsed.
         */
        nrows: number;
        /**
         * The number of columns parsed, or 0 if only row offsets are returned.
         */
        ncols: number;
        /**
         * The index offsets into the data string for the rows or data items.
         *
         * #### Notes
         * If the columnOffsets argument to the parser is false, the offsets array
         * will be an array of length nrows, where `offsets[r]` is the index of the
         * first character of row r.
         *
         * If the columnOffsets argument to the parser is true, the offsets array
         * will be an array of length `nrows*ncols`, where `offsets[r*ncols + c]` is
         * the index of the first character of the item in row r, column c.
         */
        offsets: number[];
    }
}
/**
 * Parse delimiter-separated data.
 *
 * @param options: The parser options
 * @returns An object giving the offsets for the rows or columns parsed.
 *
 * #### Notes
 * This implementation is based on [RFC 4180](https://tools.ietf.org/html/rfc4180).
 */
export declare function parseDSV(options: IParser.IOptions): IParser.IResults;
/**
 * Parse delimiter-separated data where no delimiter is quoted.
 *
 * @param options: The parser options
 * @returns An object giving the offsets for the rows or columns parsed.
 *
 * #### Notes
 * This function is an optimized parser for cases where there are no field or
 * row delimiters in quotes. Note that the data can have quotes, but they are
 * not interpreted in any special way. This implementation is based on [RFC
 * 4180](https://tools.ietf.org/html/rfc4180), but disregards quotes.
 */
export declare function parseDSVNoQuotes(options: IParser.IOptions): IParser.IResults;

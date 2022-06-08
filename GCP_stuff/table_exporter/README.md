<h1>Table Export App</h1>

<h4>Purpose</h4>
<p>BigQuery will export tables in various formats, but when the export
is more than one file, it chooses file sizes arbitrarily to a point. This
app will let you choose the max file size and whether or not to gzip the
resulting files.</p>

<h4>Setup</h4>
<ol>
  <li>This app is designed to be executed from a unix style terminal</li>
  <li>This terminal must have a connection to Google Cloud Storage</li>
  <li>Users must add execute permissions to the shell scripts:
    <ul>
      <li><code>chmod +x gsutil_cp.sh</code></li>
      <li><code>chmod +x gsutil_gzip_cp.sh</code></li>
    </ul>
  </li>
  <li>Install Python package dependencies:
    <ul>
      <li><code>pip install -r requirements.txt</code></li>
    </ul>
  </li>
</ol>

<h4>Usage</h4>
<ul>
  <li>Input files must be in parquet format. See <a
    href="https://cloud.google.com/bigquery/docs/exporting-data#bq"
    >Exporting Table Data from BigQuery</a> for help.</li>
  <li>File output can be csv or json</li>
  <li>The <code>max_file_size</code> parameter specifies "pre-zipped" max size.
    Zipped file sizes will be smaller if zipping is enabled.</li>
  <li>input_dir and outpur_dir parameters should be supplied as
    <code>gs://bucket/path/to/files</code></li>
  <li>Tip: give your output_dir a distinct name for each export</li>
</ul>

<h4>Example Usage</h4>
<ul>
  <li><code>cd table_exporter</code></li>
  <li><code>python app.py --extension=json --disable_gzip
    --input_dir=gs://<bucket>/parquet_files
    --output_dirgs://<bucket>/<my_output_dir>/output</code></li>

<h4>View App Documentation</h4>
<ul><li><code>python app.py -h</code></li></ul>

<h4>Available Parameters</h4>
<table style="float:left;">
  <tr>
    <th>parameter</th>
    <th>data</th>
    <th>info</th>
  </tr>
  <tr>
    <td>--extension</td><td>required</td><td>csv, json</td>
  <tr>
  <tr>
    <td>--input_dir</td><td>required</td><td>format: gs://bucket/path/to/files</td>
  <tr>
  <tr>
    <td>--output_dir</td><td>required</td><td>format: gs://bucket/path/to/output</td>
  <tr>
  <tr>
    <td>--max_file_size</td><td>optional</td><td>default=10: max pre-zipped file size in GB</td>
  <tr>
  <tr>
    <td>--disable_logging</td><td>on/off</td><td>turn off logging (not recommended)</td>
  <tr>
  <tr>
    <td>--disable_gzip</td><td>on/off</td><td>turn off gzip compression</td>
  <tr>
  <tr>
    <td>--write_prefix</td><td>optional</td><td>default=DATA: for output files</td>
  <tr>
</table>

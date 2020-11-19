<h1>Flask Tutorial Application</h1>
<br>
<p>This app follows the primary flask tutorial in the <a href="https://flask.palletsprojects.com/en/1.1.x/">Flask Documentation</a></p>
<br>
<h3>Running the App</h3>
<div>Set the following environment variables (use <code>set</code> for windows and <code>export</code> for linux/mac):
<ul>
    <li>FLASK_APP=flaskr</li>
    <li>FLASK_ENV=development</li>
</ul>
    <div>Then run <code>flask run</code></div>
</div>
<br>
<h3>Deploying the App</h3>
<h4>Preparing the app for production</h4>
<ul>
    <li>Change the <code>SECRET_KEY</code> value from <code>'dev'</code> to a random string in the app factory function in /flaskr/__init__.py</li>
    <li>Another option instead of changing this value is to use an environment variable that differs in dev/prod</li>
</ul>
<hr>
<h4>Installing on another machine</h4>
<ul>
    <li>Copy the <code>dist/flaskr-1.0.0-py3-none-any.whl</code> file or download from <a href="https://github.com/chuktuk">GitHub</a></li>
    <li>Create and activate a virtual environment using anaconda</li>
    <ul>
        <li>cd to the <code>flask-tutorial</code> directory</li>
        <li>run <code>py -3 -m venv venv</code> (windows) or <code>python3 -m venv venv</code> (linux/mac)</li>
        <li>activate the environment running <code>venv\Scripts\activate</code> (winodws) or <code>. venv/bin/activate</code> (linux/mac)</li>
    </ul>
    <li>install the app with pip <code>pip install flaskr-1.0.0-py3-none-any.whl</code></li>
    <li>initialize the app by setting (set/export depending on os) <code>FLASK_APP=flaskr</code> and running <code>flask init-db</code></li>
    <li>create the <code>venv/var/flaskr-instance/config.py</code> file and add <code>SECRET_KEY = b''</code> including a random bytes string</li>
</ul>
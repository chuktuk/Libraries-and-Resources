<h1>Flask Template</h1>
<hr>

<div>
<h3>Adapting Template to New Apps</h3>
<p>The majority of the app is generic, but a few things need to be updated. Check the <code>.env</code> file and edit 
the environment variables needed (see <b>Deploying to Production</b> section for a list).</p>
</div>
<hr>

<div>
<h3>Running Unit Tests</h3>
<p>Before running unit test, set the <code>ENV_FOR_FLASK</code> environment variable to <code>config.TestConfig</code>.</p>
</div>

<div>
<h3>Deploying to Production</h3>
<p>There are some environment variables that need to be configured for production. The generic ones below plus any used 
for app security. The app entrypoint also needs to be set as <code>wsgi.py</code> using either 
<code>FLASK_APP=wsgi.py</code> or configuring the entrypoint as specified by the production server environment.</p>
<ul>
<li><code>APPLICATION_NAME="Name of App"</code></li>
<li><code>APP_PACKAGE_HOME=Name of primary app package</code></li>
<li><code>FLASK_ENV=production</code></li>
<li><code>ENV_FOR_FLASK=config.ProdConfig</code></li>
<li><code>DATABASE_URL=url_for_prod_database</code></li>
<li><code>LOGGING=</code> True or False to turn on file logging for the app</li>
<li><code>EMAIL_LOGS=</code> True or False to turn on email of log errors</li>
<li><code>MAIL_SERVER=smtp_mail_server</code></li>
<li><code>MAIL_SENDER=sender@address.com</code></li>
<li><code>MAIL_PASSWORD=password</code> if needed for mail protocols</li>
<li><code>MAIL_RECIPIENT=recipient@address.com</code></li>
<li><code>MAIL_SUBJECT="Email Subject"</code></li>
<li><code>MAIL_PORT=port</code> (if not 25)</li>
<li><code>MAIL_USE_TLS</code> if using TLS security</li>
</ul>
</div>
<hr>

<div>
<h3>Setting up the Dev Database</h3>
<p>Setting up the database for dev for this app requires running the commands below.<br>
Also see <a href="https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database">Flask Mega Tutorial</a>
documentation for assistance.</p>
<h4>Associated commands</h4>
<ul>
<li><code>flask init db</code></li>
<li><code>flask db migrate</code></li>
<li><code>flask db upgrade</code></li>
</ul>
</div>

<hr>
<div>
<h3>Flask Context in the Terminal</h3>
<p>In <code>wsgi.py</code> the <code>make_shell_context</code> function allows you to run <code>flask shell</code> in
the terminal to get a python session with the flask app context. You can then interact with objects like databases or 
classes in the terminal. See <a href="https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database">
Flask Mega Tutorial: Part 4</a> for more details.</p>
</div>
<hr>

<div>
<h3>Working with the SQLAlchemy Database in Terminal</h3>
<p>You can initiate an instance of the app context in the terminal by running <code>flask shell</code>. Some useful 
database commands are listed below.</p>
<ul>
<li>u = User(username='name', email='email@email.com')</li>
<li>u.set_password('P@55w0rd')</li>
<li>db.session.add(u)</li>
<li>db.session.commit()</li>
</ul>
</div>
<hr>

<div>
<h3>Ensure Language Support</h3>
<p>Run the pybabel commands from a terminal to generate language support files. Deploy with these files or generate
in production. There is command line support for this in <code>cli.py</code></p>
<ul>
<li><code>flask translate init `language-code`</code> to initialize a new language</li>
<li><code>flask translate update</code> to update your changes</li>
<li><code>flask translate compile</code> after adding new translations to the messages.po file</li>
</ul>
</div>
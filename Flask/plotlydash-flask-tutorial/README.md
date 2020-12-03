<h1>Flask/Dash Application</h1>
<p>This application is designed to unify Dash and Flask by providing 
a primary Flask application that includes multiple Dash dashboards.</p>

<div>
Environment variables needed to run:
<ul>
    <li>ENV_FOR_FLASK (specifies dev/prod environment)
        <ul>
            <li>config.DevConfig</li>
            <li>config.ProdConfig</li>
        </ul>
    </li>
    <li>SECRET_KEY (production environment only)</li>
    
</ul>
<p>Can set these using .env file and dotenv package.</p>
</div>

<div>
Application entry point is <code>wsgi.py</code>.
</div>

<div>
<h2>Running in a Dev Environment</h2>
<p>set/export <code>ENV_FOR_FLASK = config.DevConfig</code></p>
</div>

<div>
<h2>Running in Production</h2>
<p>The dev environment is not secured with a strong SECRET_KEY, so always
set to <code>config.ProdConfig</code> when deploying.</p>
<p>set/export <code>ENV_FOR_FLASK = config.ProdConfig</code></p>
<p>set/export <code>SECRET_KEY =</code> assigning a random bytes string</p>
<p>can also use the dotenv package with a .env file to set these variables</p>
</div>

<div>
<h2>To Do:</h2>
<p>Turn the <code>dashboard.py</code> file into two files. One that assembles and returns each dashboard layout
and another file that contains the <code>init_dashboard</code> functions using functions from the other file to assemble
the layouts into the apps.</p>
</div>

<div>
<h2>Notes:</h2>
<p>Some of the callbacks are working exactly right in the multi-page app, but this was more of a proof of concept
for layout and general functionality than anything else.</p>
</div>
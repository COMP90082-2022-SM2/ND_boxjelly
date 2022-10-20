# Getting Started with Flask Backend

## Python Flask App Deployment
### Project Initialization
#### Environment & Repository Set-up
cd src
Set up a Python Virtual Environment: python3 -m venv dbControlByFlask
Activate the Virtual Environment: source dbControlByFlask/bin/activate
cd dbControlByFlask
Install Dependencies: pip3 install Flask
Install Heroku plugins
heroku plugins:install buildpack-registry
heroku plugins:install buildpacks
Heroku Python & Java buildpacks required: 
heroku buildpacks:set heroku/python (This detects your app as Python)
heroku buildpacks:add heroku/java ('Tabula' library requires Java runtime on the environment)
Initialize the Git Repository: git init
heroku login
Clone the repo: heroku git:clone -a db-control-by-flask2

#### Heroku Deployment Set-up
Create a text file listing project dependencies/packages: pip3 freeze > requirements.txt
Create Procfile tell Heroku how the Python app will be running: nano Procfile  -use Gunicorn (a Web Server Gateway Interface HTTP Server) as it's compatible with Flask

### Deploy the app using Heroku pipelines
（Use Git to manage changes)

heroku login
git add .
git commit -am "make it better"
git branch: to check which branch you are currently on              
git push heroku Sophie:master (Push the git repo to the Heroku remote ‘master’ branch)

## API
| Urls                                   | Request Method | Purpose                        |
| -------------------------------------- | -------------- | ------------------------------ |
| /process                               | GET            | Extract texts                  |
| /view                                  | GET            | View results                   |

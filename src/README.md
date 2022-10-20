# Getting Started with Flask Backend

## Python Flask App Deployment
### Project Initialization
#### Environment & Repository Set-up
1. ```cd src```
2. Set up a Python Virtual Environment: ```python3 -m venv dbControlByFlask```
3. Activate the Virtual Environment: ```source dbControlByFlask/bin/activate```
4. ```cd dbControlByFlask```
5. Install Dependencies: ```pip3 install Flask```

Install Heroku plugins
1. ```heroku plugins:install buildpack-registry```
2. ```heroku plugins:install buildpacks```

Heroku Python & Java buildpacks required: 
1. ```heroku buildpacks:set heroku/python``` (This detects your app as Python)
2. ```heroku buildpacks:add heroku/java``` ('Tabula' library requires Java runtime on the environment)
3. Initialize the Git Repository: ```git init```
4. ```heroku login```
5. Clone the repo: ```heroku git:clone -a db-control-by-flask2```

#### Heroku Deployment Set-up
1. Create a text file listing project dependencies/packages: ```pip3 freeze > requirements.txt```
2. Create Procfile tell Heroku how the Python app will be running: ```nano Procfile```  -use Gunicorn (a Web Server Gateway Interface HTTP Server) as it's compatible with Flask



## API
| Urls                                   | Request Method | Purpose                        |
| -------------------------------------- | -------------- | ------------------------------ |
| /process                               | GET            | Extract texts                  |
| /view                                  | GET            | View results                   |

## Reference 
[Flask Documentation](https://flask.palletsprojects.com/en/2.2.x/)
[Heroku Documentation](https://devcenter.heroku.com/)

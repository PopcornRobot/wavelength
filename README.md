# Wavelength

Wavelegnth is a project developed by Popcorn Robot team

## Installation (Local Development)

note: you may use whichever method you are most comfortable with.

- install Postgres Database. I recommend [Postgres App](https://postgresapp.com/)
- optional: install SQL client of your choice. I recommend [TablePlus](https://tableplus.co)
- install [yarn](https://github.com/yarnpkg/yarn): `npm install --global yarn`
- install [commitizen](https://github.com/commitizen/cz-cli): `npm install commitizen -g`
- use your preffered virtual environment, we are using pipenv: `pipenv`
- clone repo: `git clone https://github.com/PopcornRobot/wavelength.git`
- install dependencies: `pip install requirements.txt`
- start server: `python manage.py runserver_plus`

## Deploy on Heroku

This template has a Dockerfile that is Django deployment ready using Heroku's container build manifest process. Each process in the Dockerfile is annotated to explain each process. Migrations will be runned manually via Heroku docker container command line.

## Docker (build steps)

remove existing images

```bash
docker stop django-heroku
docker rm django-heroku
```

build locally (this will map to port 8007):

```bash
docker build -t web:latest .
docker run -d --name django-heroku -e "PORT=8765" -e "DEBUG=1" -p 8007:8765 web:latest
```

view static files:

```bash
docker exec django-heroku ls /app/staticfiles
docker exec django-heroku ls /app/staticfiles/admin
```

to run commands within deployed heroku container:

```bash
heroku run python manage.py makemigrations -a {{HEROKU_APP_NAME}}
heroku run python manage.py migrate -a {{HEROKU_APP_NAME}}
```

## First deploy on Heroku

### Deploy via container manifest

- sign up for a Heroku acount and download their [CLI](https://devcenter.heroku.com/articles/heroku-cli)
- create a new Heroku app: `heroku create`. This will generate a new app and corresponding remotes. You will then push to this remote to deploy on Heroku master.
- after creating your heroku app, note the name in ther url and git remotes, they look something like: `https://{{HEROKU_APP_NAME}}.herokuapp.com/ | https://git.heroku.com/{{HEROKU_APP_NAME}}.git` In this example, the name of our application is:  `{{HEROKU_APP_NAME}}`
- add `SECRET_KEY` environment varaible to Heroku: `heroku config:set SECRET_KEY={{YOU_SECRET_KEY}} -a {{HEROKU_APP_NAME}}` This is a 50 character maximum string that is randomly generated and use to validate your application.
- we will be using [Heroku container build manifest](https://devcenter.heroku.com/articles/build-docker-images-heroku-yml) to deploy our Docker images.
- setup your Heroku container stack: `heroku stack:set container -a {{HEROKU_APP_NAME}}`
- create an `heroku.yml` (already created in this repo) file this will inform heroku on the Dockerfile to build from and any commands to run.
- initialize a Git repo and create a commit ie `git add .`, `git commit -am "featL first commit:"` and `git push`.
- install the `heroku-manifest` plugin from the beta CLI channel: `heroku plugins:install @heroku-cli/plugin-manifest`
- add the Heroku remote: `heroku git:remote -a {{HEROKU_APP_NAME}}` this links up your remotes with heroku master
- deploy to Heroku master to build your image and deploy your container: `git push heroku master`

### Create the Postgres database

```bash
heroku addons:create heroku-postgresql:hobby-dev -a {{HEROKU_APP_NAME}}
```

Once the database is up, run the migrations:

```bash
heroku run python manage.py makemigrations -a {{HEROKU_APP_NAME}}
heroku run python manage.py migrate -a {{HEROKU_APP_NAME}}
```

Note: be sure to update site url in your allowed host.  Replace anywhere that has, `{{HEROKU_APP_NAME}}`

There are three types of stages:
- `setup` is used to define Heroku addons and configuration variables to create during app provisioning.
- `release` is used to define tasks that you would like to execute during a release.
- `run` is used to define which commands to run for the web and worker processes.

## Workflow

- make sure you are on master: `git checkout master`
- make sure master is up to date, in master branch: `git pull`
- branch off `git checkout -b feature/your-feature-branch`
- add to branch `git add .`
- user commitizen to commit: `git cz` (follow command prompts)
- push your code: `git push`

## Tips
- reset your branch `git reset --hard HEAD`

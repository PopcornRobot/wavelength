# Wavelength

Wavelegnth is a project developed by Popcorn Robot team

## Installation (Local Development)

note: you may use whichever method you are most comfortable with.

- use your preffered virtual environment, we are using pipenv: `pipenv`
- clone repo: `git clone https://github.com/PopcornRobot/wavelength.git`
- install dependencies: `pip install requirements.txt`

## Deploy on Heroku

This template has a Dockerfile that is Django deployment ready using Heroku's container build manifest process. Each process in the Dockerfile is annotated to eplain each process. Migrations will be runned manually via Heroku docker container command line.

## Docker

remove existing images

```bash
docker stop django-heroku
docker rm django-heroku
```

build locally:

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

## Deploying on Heroku

### Deploy via container manifest

Sign up for a Heroku acount and download their [CLI](https://devcenter.heroku.com/articles/heroku-cli)

create a new Heroku app. This will generate a new app and corresponding remotes. You will then push to this remote to deploy on Heroku master. In this example, the name of our application is:  `{{HEROKU_APP_NAME}}`

Note: be sure to update this in your allowed host.  Replace anywhere that has, `{{HEROKU_APP_NAME}}`

```bash
heroku create
```

add `SECRET_KEY` environment varaible to Heroku. This is a 50 character maximum string that is randomly generated and use to validate your application.

Note: remember to replace `YOUR_SECRET_KEY` with your key and rplace `{{HEROKU_APP_NAME}}` with your app's name

```bash
heroku config:set SECRET_KEY={{YOU_SECRET_KEY}} -a {{HEROKU_APP_NAME}}
```

We will be using [Heroku container build manifest](https://devcenter.heroku.com/articles/build-docker-images-heroku-yml) to deploy our Docker images.

Setup your Heroku container stack

```bash
heroku stack:set container -a {{HEROKU_APP_NAME}}
```

Create an `heroku.yml` file this will inform heroku on the Dockerfile to build from and any commands to run.

There are three types of stages:

- `setup` is used to define Heroku addons and configuration variables to create during app provisioning.
- `release` is used to define tasks that you'd like to execute during a release.
- `run` is used to define which commands to run for the web and worker processes.

Next, install the `heroku-manifest` plugin from the beta CLI channel:

```bash
heroku plugins:install @heroku-cli/plugin-manifest
```

With that, initialize a Git repo and create a commit.

Then, add the Heroku remote:

```bash
heroku git:remote -a {{HEROKU_APP_NAME}}
```

Deploy to Heroku master to build your image and deploy your container:

```bash
git push heroku master
```

### Add PostgresDB

#### Create the Postgres database

```bash
heroku addons:create heroku-postgresql:hobby-dev -a {{HEROKU_APP_NAME}}
```

Once the database is up, run the migrations:

```bash
heroku run python manage.py makemigrations -a {{HEROKU_APP_NAME}}
heroku run python manage.py migrate -a {{}}

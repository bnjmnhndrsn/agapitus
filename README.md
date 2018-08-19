# agapitus
Twitter bot tweeting images from wikipedia commons, using the [Petronax facade API](https://github.com/bnjmnhndrsn/petronax)

# installation
- install pyenv and pyenv-virtualenv
- create virtualenv and activate it
- install python dependencies
- intall Postgres.app
- run in Postgres console:
```
CREATE DATABASE agapitus_dev;
```
- create .env file, with the following lines:
```
DATABASE_URL=postgres://:@localhost/agapitus_dev
TWITTER_CONSUMER_KEY=[get this from twitter]
TWITTER_CONSUMER_SECRET=[get this from twitter]
TWITTER_ACCESS_TOKEN=[get this from twitter]
TWITTER_ACCESS_TOKEN_SECRET=[get this from twitter]
```
- run tasks using `heroku local` so dev environment variables are loaded. or set them in current environment manually.
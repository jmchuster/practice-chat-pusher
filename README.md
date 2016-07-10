# practice-chat-pusher

Design and prototype a secure realtime notification system

We would like to be able to push information to user's browsers, instead of having the users poll the backend for new data periodically. Please build a proof of concept application on Heroku using Django and the Pusher add-on. The application should utilize private channels to propagate changes to users in realtime securely. One possible multi-user real-time app idea is a simple chat room, or a shared todo list.

Please also brainstorm and come up with a good strategy for how individual developers in a team can rely on the Pusher realtime system even when developing locally.

Please also think about how you would be able to build a real time notification system like Pusher.

# python-getting-started

A barebones Python app, which can easily be deployed to Heroku.

This application supports the [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) article - check it out.

## Running Locally

Make sure you have Python [installed properly](http://install.python-guide.org).  Also, install the [Heroku Toolbelt](https://toolbelt.heroku.com/) and [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

```sh
$ git clone git@github.com:heroku/python-getting-started.git
$ cd python-getting-started

$ pip install -r requirements.txt

$ createdb python_getting_started

$ python manage.py migrate
$ python manage.py collectstatic

$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku master

$ heroku run python manage.py migrate
$ heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)

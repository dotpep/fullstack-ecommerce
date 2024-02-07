# Full Stack Ecommerce using Django

Full-Stack Django ecommerce project.

## Features

- [ ] 

## Installation

- create virtual environment
- install dependencies from requirements.txt or pipfile
- `python manage.py runserver`

---

Sending email verification:
- get google app password from here [Sign in with app passwords](https://support.google.com/accounts/answer/185833?hl=en&sjid=10291959553872721365-EU)
- fill environment variables `.env`
- uncomment or comment this line to testing email sending:

```python
# Uncomment/Comment 
# This line for sent actual email verification text
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# This line for sent console email verification text
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

---

Payment:

Local Environment Stripe Webhook listener CLI tool in Test mode:

- install stripe.exe cli tool/file [Get started with the Stripe CLI](https://stripe.com/docs/stripe-cli)
- (go to Listen to Stripe events in stripe webpage) copy `endpoint_secret` variable and replace in .env `STRIPE_WEBHOOK_SECRET` with `endpoint_secret`
- `stripe login`
- `stripe listen --forward-to localhost:8000/payment/stripe-webhook/`

---

Environment Variables:

- create `.env` file in core project folder
- add env const variables like this without any spacing and quotes (check `ENV_NAME = env('ENV_NAME')`)
- replace this line of code with your own tokens in settings:

```txt
EMAIL_HOST_SENDER=actualyourdata
EMAIL_HOST_APP_PASSWORD=actualyourdata

STRIPE_PUBLISHABLE_KEY=actualyourdata
STRIPE_SECRET_KEY=actualyourdata
STRIPE_API_VERSION=actualyourdata

YOOKASSA_SECRET_KEY=actualyourdata
YOOKASSA_SHOP_ID=actualyourdata
```

---

Connect Celery and Redis as broker (for payment successful email message background task) (I am using Windows and WSL for that) - run all separate.

- run django server `python manage.py runserver`
- run stripe webhook `stripe listen --forward-to localhost:8000/payment/stripe-webhook/` [Get started with the Stripe CLI](https://stripe.com/docs/stripe-cli) and [Use incoming webhooks to get real-time updates](https://stripe.com/docs/webhooks)

---

- install redis [For windows you need WSL](https://redis.io/docs/install/install-redis/install-redis-on-windows/) `sudo apt-get install redis`
- run redis server with `redis-server` or `sudo service redis-server start` and you can check it by `redis-cli` and in redis cli `ping` you must receive PONG message

---

- run celery workers
- install `pip install celery`
- run `celery -A project worker -l info` or `celery -A project worker --loglevel=INFO` [Running the Celery worker server](https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html#redis)
- you can ran two or more celery workers by given different name using `-n` flag in `celery workers` command
- `celery -A project worker -l info -n mysecondworker_name`

---

- run celery-beat
- instead `celery -A project worker -l info` or `celery -A project worker --loglevel=INFO`
- add `celery -A project worker -l info --beat` or `celery -A project worker --loglevel=INFO --beat`
- or in Windows you can:
- `python -m celery -A project beat --loglevel=info` (project is name of django application that is in my case i called project and you must be in `core` directory and see project folder that contains celery.py)

---

- run flower (for monitoring and managing Celery clusters) [celery flower python](https://flower.readthedocs.io/en/latest/index.html)
- `celery -A project flower`
- Flower by default works in port of 5555 to see flower celery cluster interface panel like django admin panel go to:
- `http://127.0.0.1:5555/` or for task `http://127.0.0.1:5555/tasks`

---

You can Test celery in admin panel:

- go to `http://127.0.0.1:8000/admin`
- check this app section:
- CELERY RESULTS
- PERIODIC TASKS

---

Admin panel (superuser):

- username: admin
- password: admin

### Note

- you can also delete db.sqlite3
- specify google fonts in settings `GOOGLE_FONTS = ['Montserrat:wght@300,400,500', 'Roboto']` and pass it to (`base.html` and `index.html`)

## Tech stack

Back-end:

- Python
- Django
- Django Rest Framework (DRF)
- Djoser Auth
- API
- Postgres
- Redis
- Celery
Server-side and Othes:
- Swagger and Redoc Docs
- Nginx
- Gunicorn
- Docker
- Docker Compose
- GitHub Actions
- Git
Front-end:
- Django HTMX
- JavaScript
- Ajax
- HTML, CSS
- Bootstrap and Font Awesome
Third party API services:
- Stripe

## Contribution

## LICENCE



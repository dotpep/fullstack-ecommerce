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



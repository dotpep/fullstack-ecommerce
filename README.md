# Full Stack Ecommerce using Django

Full-Stack Django ecommerce project.

## Features

- Faker generate fakeproducts
- API support with Swagger and Redoc documentation
- Celery with Redis, Celery beat and Flower
- Docker-compose for Nginx, Gunicorn, PostgreSQL, Celery, Redis and etc.

## Tasks

- [ ] Add poetry instead pipenv

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

Other additonal:

- Flower for monitoring celery
- WeasyPrint for generating pdf paymnet invoice reports
- Django Crispy Forms
- Email Verification

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
- Yookassa

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

> Stripe provides payment processing API service, we can use this service to implement payment system for our website.

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

> Celery is background task or distributed task queue processor and focused on real-time operation but also supports scheduling, we can give tasks to celery that takes long time to process to do that task in background of queue without making our website client wait, for example until email message arrives and is fully processed in our backend. (It takes 2 seconds to send an email, but we don't need the client to wait for page to reload while that email is sent).

Connect Celery and Redis as broker (for payment successful email message background task) (I am using Windows and WSL for that) - run all separate.

- run django server `python manage.py runserver`
- run stripe webhook `stripe listen --forward-to localhost:8000/payment/stripe-webhook/` [Get started with the Stripe CLI](https://stripe.com/docs/stripe-cli) and [Use incoming webhooks to get real-time updates](https://stripe.com/docs/webhooks)

---

> Redis is fast nosql key value database that runs in RAM memory (uses for caching and etc.) and message broker in our case we use it as message broker for celery that requires a message transport to send and receive messages. [Redis - What is a message broker?](https://redis.com/solutions/use-cases/messaging/)

- install redis [For windows you need WSL](https://redis.io/docs/install/install-redis/install-redis-on-windows/) `sudo apt-get install redis`
- run redis server with `redis-server` or `sudo service redis-server start` and you can check it by `redis-cli` and in redis cli `ping` you must receive PONG message

---

> Celery workers is separate/indiviual machine that takes task provided by message broker (also runs in separate machine/server) and perform that task to complete. (Common many celery workers and one message broker or may any amount of workers/brokers). [Stackoverflow - What is a Celery worker node exactly?](https://stackoverflow.com/questions/28450026/what-is-a-celery-worker-node-exactly)

- run celery workers
- install `pip install celery`
- run `celery -A project worker -l info` or `celery -A project worker --loglevel=INFO` [Running the Celery worker server](https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html#redis)
- you can ran two or more celery workers by given different name using `-n` flag in `celery workers` command
- `celery -A project worker -l info -n mysecondworker_name`

---

> Celery beat is a scheduler that sends predefined tasks to a celery worker at a given time. It kicks off tasks at regular intervals, which are then executed by available worker nodes in the cluster. [Celery beat - Periodic Tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html)

- run celery-beat
- instead `celery -A project worker -l info` or `celery -A project worker --loglevel=INFO`
- add `celery -A project worker -l info --beat` or `celery -A project worker --loglevel=INFO --beat`
- or in Windows you can:
- `python -m celery -A project beat --loglevel=info` (project is name of django application that is in my case i called project and you must be in `core` directory and see project folder that contains celery.py)

---

> Flower uses for monitoring and managing Celery clusters. It provides real-time information about the status of Celery workers and tasks with information and interface panel like admin panel in django.

- run flower [celery flower python](https://flower.readthedocs.io/en/latest/index.html)
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

---

WeasyPrint for generating pdf (for payment invoice - is paid or not paid) on Windows 10

> WeasyPrint uses for creating pdf statistical reports, invoices, tickets... using visual rendering engine for HTML and CSS that can export to PDF.

- install WeasyPrint `pip install WeasyPrint`
- install GTK:
- download the MSYS2 from the official website: [MSYS2](https://www.msys2.org/) (which provides a Unix-like environment on Windows and allows you to install GTK)
- update MSYS2 `pacman -Syu` its update the package database and core system packages
- install GTK and its dependencies, run the following command `pacman -S mingw-w64-x86_64-gtk3`
- setup env variables - after installing GTK, you need to add the GTK bin directory to your system's PATH environment variable so that WeasyPrint can find it. (GTK bin directory. by default, it should be something like `C:\msys64\mingw64\bin`.)
- check installation by `gtk-launch --version` or `gtk3-demo` on windows powershell
- run django server and check if any errors of WeasyPrint accurs or not
- unnecessary command to apply static files like css for WeasyPrint pdf templates `python manage.py collectstatic`

---

Faker for creating fake product

- faker script that created fake products added to django base command (BaseCommand) path file: `management/command/fakeproducts.py`
- and you can run it by `python manage.py fakeproducts`

---

Configure Postgresql Database

- install postgres [PostgreSQL Downloads](https://www.postgresql.org/download/)
- in postgres shell to enter `psql -U postgres` and enter password
- new user `CREATE USER username WITH PASSWORD 'Userpassword1234'`;
- new database `CREATE DATABASE database_name OWNER username;`
- grant privileges to the user `GRANT ALL PRIVILEGES ON DATABASE database_name TO username;`
- see created database `\l` and to exit `\q`
- uncomment section of PostgreSQL in settings if needed
- add variable to `.env`

```text
POSTGRES_DB=database_name
POSTGRES_USER=username
POSTGRES_PASSWORD=Userpassword1234
POSTGRES_HOST=db
```

### Note

- you can also delete db.sqlite3
- specify google fonts in settings `GOOGLE_FONTS = ['Montserrat:wght@300,400,500', 'Roboto']` and pass it to (`base.html` and `index.html`)

## LICENCE

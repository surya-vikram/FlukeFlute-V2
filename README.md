# Steps to Run
## Navigate to backend directory and make sure to activate venv in all terminals
### Terminal 1 
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
### Terminal 2
- `redis-server --port 6380`
### Terminal 3
- `~/go/bin/MailHog`
### Terminal 1
- `./run.sh`
### Terminal 4
- `celery -A app.extensions.celery_app worker -l info`
### Terminal 5
- `celery -A app.extensions.celery_app beat -l info`
### Terminal 6
- `redis-cli -p 6380 -n 1`
- `KEYS *`

## Navigate to frontend directory 
### Terminal 7
- `npm i`
- `npm run serve`

# ------------------------------------------------------------
## Redis, Celery, MailHog commands

### Redis Operations

- `redis-server`: To start the server.
- `redis-server --port 6380`: To start the server on port 6380 in case of clash. 
- `ctrl + C`: to stop redis.
- `redis-cli`: To go inside cli. Do this in separate terminal.
- `redis-cli -p 6380`: To go inside cli connected to 6380 in separate terminal.
- `KEYS *`: To see all the cached items.
- `SHUTDOWN NOSAVE`: To stop the execution.
- `ps aux | grep redis-server`: To see all the running redis ports.
- `kill 13399`: To stop the execution with id 13399.
- `sudo kill 13399`: To stop the execution which requires root privileges.

### Celery Operations

- `celery -A app.extensions.celery_app worker -l info`
- `celery -A app.extensions.celery_app beat -l info`

### Mailhog Operations
 - `~/go/bin/MailHog`: starts mailhog.
 - `localhost:8025`: view mailhog ui.



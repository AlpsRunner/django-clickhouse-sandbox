# django-clickhouse-sandbox
simple project to learn how gather and send statistics from django to clickhouse


# Dependecies

* Celery 4.3.1
* Django 2.2
* Redis 4.0.9
* ClickHouse 19.16.3.6


# How to install:
```
  git clone https://github.com/AlpsRunner/django-clickhouse-sandbox.git
  cd django-clickhouse-sandbox
  
  pip3 install -r requirements.txt

  export CLICKHOUSE_DB_URL='<your clickhouse URL>:8123'
  export CLICKHOUSE_DB_USERNAME='<your clickhouse user name>'
  export CLICKHOUSE_DB_PASS='<your clickhouse user pass>'

  python3 manage.py makemigrations
  python3 manage.py migrate
  python3 manage.py fill_db
```

# How to install dependencies (Ubuntu):

To install ClickHouse visit [https://clickhouse.yandex/docs/ru/getting_started/](https://clickhouse.yandex/docs/ru/getting_started/).

```
  celery installation:  
    sudo apt install python-celery-common
  
  redis installation:
    sudo apt install redis
```

# How to work with ClickHouse DB:
```
  create:  
    python3 manage.py create_clickhouse_db
  
  drop:
    python3 manage.py drop_clickhouse_db
  
  show unique active users count by days:
    python3 manage.py active_users_count_by_days
  
  show unique active users by days
    python3 manage.py active_users_by_days
```

# How to run in debug mode:
```
  To run celery tasks (2000 user activity sumulation every 1 min  and sending data to clickhouse every 5 min):
    celery -A dataclick worker -l info -B --concurrency=1  
  
  To see django DB and ClickHouse Stat:
    python3 manage.py runserver 0.0.0.0:8000
```

# How to run in prod mode:
```
  in first terminal:
     python3 manage.py runserver 0.0.0.0:8000
  
  in second terminal run celery beat:
    celery -A dataclick beat
  
  in third terminal run celery worker:
    celery -A dataclick worker --concurrency=1
```

Then visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
You will see statistics of the simulation.

# Technical Details:

IMPORTANT: set ONLY --concurrency=1 for celery worker to prevent data collisions in ClickHouse DB because no thread sync implemented. 

# Known Issue:

If you have error when connecting to ClickHouse DB check <listen_host> setting (Ubuntu):  
  
    sudo nano /etc/clickhouse-server/config.xml
    
      change
        <!-- <listen_host>0.0.0.0</listen_host> -->
      to
        <listen_host>0.0.0.0</listen_host>
  
    sudo systemctl restart clickhouse-server

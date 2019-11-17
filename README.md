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

  python manage.py makemigrations
  python manage.py migrate
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
    python3 manage.py  active_users_by_days
```

# How to run in debug mode:
```
  in first terminal:
     python3 manage.py runserver 0.0.0.0:8000
  
  in other terminal run celery tasks (user activity sumulation and sending data to clickhouse):
    celery -A dataclick worker -l -B info --concurrency=1
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

Then visit [http://127.0.0.1:8000/index/](http://127.0.0.1:8000/).
or
[http://<server-IP>:8000/index/](http://<server-IP>:8000/).
You will see statistics of sumulation.

# Technical Details:
IMPORTANT to set --concurrency=1 for celery worker to prevent data collisions in ClickHouse DB because no thread sync implemented. 


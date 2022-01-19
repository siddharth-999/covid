# COVID PROJECT

## **PROJECT SETUP**
1. **Clone this repository:**
      * git clone git@github.com:siddharth-999/covid-case-app.git
2. **Create virtual environment:**
      * sudo apt install virtualenv
      * virtualenv --python='/usr/bin/python3.6' covid-env
      * source covid-env/bin/activate
      * cd covid-case-app/
3.  **Install dependencies**:
      * pip install -r requirements.txt
4.  **create postgres** install postgres database **/** create db if already install
      *  **install postgresql**
            * wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
            * sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -sc)-pgdg main" > /etc/apt/sources.list.d/PostgreSQL.list'
            * sudo apt update
            * sudo apt-get install postgresql-10
      * **create database**
           *  sudo su - postgres
                * postgres@xxx:~$ psql
                * create database <bd_name>;
                * create user <admin_name> password <password>;
                * grant all privileges on database <bd_name> to <admin_name>;
                * postgres=# \q
                * postgres@xxx:~$ exit
5.  **Install redis server**
     * sudo apt update
     * sudo apt install redis-server
     * redis-cli #just to test
         * <redis_ip:port> PING
         * PONG #output
     * redis-server
6.  **create local.py** in <repo_name>/covid/
    * local.py content:
        ```
        DEBUG = True
        # DATABASE CONNECTION
        DATABASES = {
            'default':
                {
                    'ENGINE': 'django.db.backends.postgresql_psycopg2',
                    'NAME': '<bd_name>',
                    'USER': '<admin_name>',
                    'PASSWORD': '<password>',
                    'HOST': 'localhost',
                    'PORT': '<db_port>'
                }
        }
        BROKER_URL = 'redis://<redis_ip:port>/8'
        CELERY_RESULT_BACKEND = 'redis://<redis_ip:port>/10'
        ANYMAIL = {
            'POSTMARK_SERVER_TOKEN': '<postmark_server_token>',
            'TEST_MODE': True,
            'VERBOSITY': 0,
        }
        DEFAULT_FROM_EMAIL = 'covid <domain_email>' # email will be sent from this email
        ```
7.  **Run migrations:**
      * ./manage.py migrate
8.  **Create superuser:**
      * ./manage.py createsuperuser
9.  **Run the server:**
      * ./manage.py runserver
10. **Run celery:**
      * celery -A covid beat  --loglevel=INFO
      * celery -A covid worker --autoscale=6,2 --loglevel=INFO
11.  **Browse below url:**
      * Swagger url:- `http://localhost:8000/api/docs`
      * Admin url: - `http://localhost:8000/admin/`

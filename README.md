# ccasp
Cloud Controlled Automation Fall Semester 2015 Senior Project

Check requirements.txt for required Python libraries -- install with <code>pip</code> or <code>easy_install</code>.
Requires <code>postgresql-devel</code> and <code>python-devel</code> packages.

<code>settings_change_me.py</code> in <code>Microcontrollers/Microcontrollers/</code> should be modified, renamed to ```settings.py``` and the <code>DATABASE</code> values should be set to

```javascript
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'mydb',      # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'USER': 'myuser',
            'PASSWORD': 'password',
            'HOST': 'localhost', # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            'PORT': '5432',          # Set to empty string for default.
        }
    }
```

More information about setting up and configuring Django with Postgres can be found <a href="https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-django-with-postgres-nginx-and-gunicorn#Step-Seven">here</a>.

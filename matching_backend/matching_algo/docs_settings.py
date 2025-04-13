from django.conf import settings

if not settings.configured:
    settings.configure(
        DEBUG=True,
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'matching_algo',  # Use app name directly
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        USE_TZ=True,
        SECRET_KEY='docs-secret-key',
        DEFAULT_AUTO_FIELD='django.db.models.BigAutoField',
        LOGGING_CONFIG=None,
    )
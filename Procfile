web: waitress-serve --port=$PORT --threads=$WEB_CONCURRENCY --channel-timeout=20 session_token_auth_demo.wsgi:application
release: python manage.py migrate

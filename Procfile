web: sentry --config=sentry.conf.py run web
worker: sentry --config=sentry.conf.py run worker --loglevel=INFO
cron: sentry --config=sentry.conf.py run cron --loglevel=INFO
release: sentry --config=sentry.conf.py upgrade --noinput

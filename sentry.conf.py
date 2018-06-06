from sentry.conf.server import *

import os
import urlparse

SENTRY_SINGLE_ORGANIZATION = True
SENTRY_FEATURES['auth:register'] = False

DEBUG = False
CONF_ROOT = os.path.dirname(__file__)

# Get and parse dokku env vars
db_url = urlparse.urlparse(os.environ['DATABASE_URL'])
redis_url = urlparse.urlparse(os.environ['REDIS_URL'])

DATABASES = {
  'default': {
    'ENGINE': 'sentry.db.postgres',
    'NAME': db_url.path[1:],
    'USER': db_url.username,
    'PASSWORD': db_url.password,
    'HOST': db_url.hostname,
    'PORT': db_url.port
  }
}
SENTRY_USE_BIG_INTS = True

SENTRY_CACHE = 'sentry.cache.redis.RedisCache'

BROKER_URL = os.environ['REDIS_URL']

SENTRY_RATELIMITER = 'sentry.ratelimits.redis.RedisRateLimiter'
SENTRY_BUFFER = 'sentry.buffer.redis.RedisBuffer'
SENTRY_QUOTAS = 'sentry.quotas.redis.RedisQuota'
SENTRY_TSDB = 'sentry.tsdb.redis.RedisTSDB'
SENTRY_DIGESTS = 'sentry.digests.backends.redis.RedisBackend'

SENTRY_WEB_HOST = '0.0.0.0'
SENTRY_WEB_PORT = os.environ.get('PORT')
SENTRY_WEB_OPTIONS = {
    'workers': 2,
    'secure_scheme_headers': {'X-FORWARDED-PROTO': 'https'},
}

SENTRY_OPTIONS.update({
  'redis.clusters': {
    'default': {
      'hosts': {
        0: {
          'host': redis_url.hostname,
          'port': redis_url.port,
          'password': redis_url.password,
        }
      }
    },
  },
  'system.secret-key': os.environ['SECRET_KEY'],
  'system.admin-email': os.environ.get('SENTRY_ADMIN_EMAIL', ''),
  'filestore.backend': 'filesystem',
  'filestore.options': {'location': '/tmp/sentry-files'},
})

GITHUB_EXTENDED_PERMISSIONS = ['repo']

# Expose any env that starts with SC_
for env_key, env_val in os.environ.items():
    if env_key.startswith('SC_'):
        globals()[env_key[3:]] = env_val

from sentry.conf.server import *

import os
import os.path
import urlparse

CONF_ROOT = os.path.dirname(__file__)

DEBUG = False

# Get and parse dokku postgres dsn
postgres_url = urlparse.urlparse(os.environ['DATABASE_URL'])

DATABASES = {
  'default': {
    'ENGINE': 'sentry.db.postgres',
    'NAME': postgres_url.path[1:],
    'USER': postgres_url.username,
    'PASSWORD': postgres_url.password,
    'HOST': postgres_url.hostname,
    'PORT': postgres_url.port
  }
}

# You should not change this setting after your database has been created
# unless you have altered all schemas first
SENTRY_USE_BIG_INTS = True

###########
# General #
###########

# Instruct Sentry that this install intends to be run by a single organization
# and thus various UI optimizations should be enabled.
SENTRY_SINGLE_ORGANIZATION = True

# Disable registration
SENTRY_FEATURES['auth:register'] = False

#########
# Redis #
#########

# Get and parse dokku redis dsn
redis_url = urlparse.urlparse(os.environ['REDIS_URL'])

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
  }
})

#########
# Cache #
#########

# A primary cache is required for things such as processing events

SENTRY_CACHE = 'sentry.cache.redis.RedisCache'

#########
# Queue #
#########

BROKER_URL = os.environ['REDIS_URL']

###############
# Rate Limits #
###############

# Rate limits apply to notification handlers and are enforced per-project
# automatically.

SENTRY_RATELIMITER = 'sentry.ratelimits.redis.RedisRateLimiter'

##################
# Update Buffers #
##################

# Buffers (combined with queueing) act as an intermediate layer between the
# database and the storage API. They will greatly improve efficiency on large
# numbers of the same events being sent to the API in a short amount of time.
# (read: if you send any kind of real data to Sentry, you should enable buffers)

SENTRY_BUFFER = 'sentry.buffer.redis.RedisBuffer'

##########
# Quotas #
##########

# Quotas allow you to rate limit individual projects or the Sentry install as
# a whole.

SENTRY_QUOTAS = 'sentry.quotas.redis.RedisQuota'

########
# TSDB #
########

# The TSDB is used for building charts as well as making things like per-rate
# alerts possible.

SENTRY_TSDB = 'sentry.tsdb.redis.RedisTSDB'

###########
# Digests #
###########

# The digest backend powers notification summaries.

SENTRY_DIGESTS = 'sentry.digests.backends.redis.RedisBackend'

################
# File storage #
################

# Uploaded media uses these `filestore` settings. The available
# backends are either `filesystem` or `s3`.

SENTRY_OPTIONS['filestore.backend'] = 'filesystem'
SENTRY_OPTIONS['filestore.options'] = {
    'location': '/var/lib/sentry/files',
}

##############
# Web Server #
##############

SENTRY_WEB_HOST = '0.0.0.0'
SENTRY_WEB_PORT = 9000

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

secret_key = os.environ['SECRET_KEY']
if not secret_key:
  raise Exception('Error: SENTRY_SECRET_KEY is undefined, run `generate-secret-key` and set to -e SENTRY_SECRET_KEY')

SENTRY_OPTIONS['system.secret-key'] = secret_key

GITHUB_EXTENDED_PERMISSIONS = ['repo']

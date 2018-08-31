![](.github/images/repo_header.png)

[![Sentry](https://img.shields.io/badge/Sentry-9.0.0-blue.svg)](https://github.com/getsentry/sentry/releases/tag/9.0.0)
[![Dokku](https://img.shields.io/badge/Dokku-v0.12.12-blue.svg)](https://github.com/dokku/dokku/releases/tag/v0.12.12)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/D1ceWard/sentry_on_dokku/graphs/commit-activity)
# Run Sentry on Dokku

## Perquisites

### What is Sentry?

[Sentry](https://sentry.io) fundamentally is a service that helps you monitor and fix crashes in realtime. The server is in Python, but it contains a full API for sending events from any language, in any application.

### What is Dokku?

[Dokku](http://dokku.viewdocs.io/dokku/) is the smallest PaaS implementation
you've ever seen - _Docker powered mini-Heroku_.

### Requirements
* A working [Dokku host](http://dokku.viewdocs.io/dokku/getting-started/installation/)
* [PostgreSQL](https://github.com/dokku/dokku-postgres) and [Redis](https://github.com/dokku/dokku-redis) plugins for Dokku
* [Letsencrypt](https://github.com/dokku/dokku-letsencrypt) plugin for SSL (optionnal)

# Setup

**Note:** We are going to use the domain `sentry.example.com` for demonstration
purposes. Make sure to replace it to your domain name.

## App and plugins

### Create the app
Log onto your Dokku Host to create the Sentry app:

```bash
dokku apps:create sentry
```

### Add plugins
Install, create and link PostgreSQL and Redis plugins:
```bash
# Install plugins on Dokku
dokku plugin:install https://github.com/dokku/dokku-postgres.git postgres
dokku plugin:install https://github.com/dokku/dokku-redis.git redis
```
```bash
# Create running plugins
dokku postgres:create sentry
dokku redis:create sentry
```
```bash
# Link plugins to the main app
dokku postgres:link sentry sentry
dokku redis:link sentry sentry
```

## Configuration

### Add SENTRY_CONF to environement variables
```bash
dokku config:set sentry SENTRY_CONF=./
```

### Setting secret key

```bash
dokku config:set sentry SECRET_KEY=$(echo `openssl rand -base64 45` | tr -d \=+ | cut -c 1-32)
```

## Domain setup

To get the routing working, we need to apply a few settings. First we set
the domain.

```bash
dokku domains:set sentry sentry.example.com
```

## Push Sentry to Dokku

### Grabbing the repository

First clone this repository onto your machine.

#### Via SSH

```bash
git clone git@github.com:D1ceWard/sentry_on_dokku.git
```

#### Via HTTPS

```bash
git clone https://github.com/D1ceWard/sentry_on_dokku.git
```

### Set up git remote

Now you need to set up your Dokku server as a remote.

```bash
git remote add dokku dokku@example.com:sentry
```

### Push Sentry

Now we can push Sentry to Dokku (_before_ moving on to the [next part](#domain-and-ssl-certificate)).

```bash
git push dokku master
```

### Create database schema
After you have sucessfully deployed app to Dokku, run following commands to finish installing Sentry:
```bash
dokku run sentry "sentry upgrade"
```
**Note:** After migrations you will be prompted to create initial user.

To create another user or if you skipped user creation in the previous command run:
```bash
dokku run sentry "sentry createuser"
```

## SSL certificate

Last but not least, we can go an grab the SSL certificate from [Let's
Encrypt](https://letsencrypt.org/).

```bash
# Install letsencrypt plugin
dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git

# Set certificate contact email
dokku config:set --no-restart sentry DOKKU_LETSENCRYPT_EMAIL=you@example.com

# Generate certificate
dokku letsencrypt sentry
```

## Wrapping up

Your Sentry instance should now be available on [https://sentry.example.com](https://sentry.example.com).

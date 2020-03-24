![](.github/images/repo_header.png)

[![Sentry](https://img.shields.io/badge/Sentry-9.1.2-blue.svg)](https://github.com/getsentry/sentry/releases/tag/9.1.2)
[![Dokku](https://img.shields.io/badge/Dokku-Repo-blue.svg)](https://github.com/dokku/dokku)
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

### Setting secret key

```bash
dokku config:set sentry SECRET_KEY=$(echo `openssl rand -base64 45` | tr -d \=+ | cut -c 1-32)
```

## Persistent storage
To persists user uploads (e.g. avatars) between restarts, create a folder on the host machine and tell Dokku to mount it to the app container.
```bash
sudo mkdir -p /var/lib/dokku/data/storage/sentry
sudo chown 32768:32768 /var/lib/dokku/data/storage/sentry
dokku storage:mount sentry /var/lib/dokku/data/storage/sentry:/var/lib/sentry/files
```

## Domain setup

To get the routing working, we need to apply a few settings. First we set
the domain.

```bash
dokku domains:set sentry sentry.example.com
```

The parent Dockerfile, provided by the sentry project, exposes port `9000` for web requests. Dokku will set up this port for outside communication, as explained in [its documentation](http://dokku.viewdocs.io/dokku/advanced-usage/proxy-management/#proxy-port-mapping). Because we want Sentry to be available on the default port `80` (or `443` for SSL), we need to fiddle around with the proxy settings.

First add the proxy mapping that sentry uses.

```bash
dokku proxy:ports-add sentry http:80:9000
```

Then, remove the proxy mapping added by Dokku.

```bash
dokku proxy:ports-remove sentry http:80:5000
```

If `dokku proxy:report` sentry shows more than one port mapping, remove all port mappings except the added above.

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

### Create first user

To create a user run:

```bash
dokku run sentry "sentry createuser"
```

This will prompt you to enter an email, password and whether the user should be a superuser.

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

### Customize Sentry config
You can customise `sentry.conf.py` to fit your needs. However you can also override any config variable using dokku env vars.
Use SC_ prefix (as of Sentry Config) to override specific sentry config variables.

Example configs for email :
```bash
dokku config:set sentry SC_EMAIL_HOST=mail.example.com \
                        SC_EMAIL_HOST_USER=sentry@example.com \
                        SC_EMAIL_HOST_PASSWORD=MailSecure1234 \
                        SC_SERVER_EMAIL=sentry@example.com \
                        SC_EMAIL_USE_TLS=True
```

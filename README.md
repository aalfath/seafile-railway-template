[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/new/template/seafile-1?utm_medium=integration&utm_source=button&utm_campaign=seafile)

# Seafile on Railway

A one-click [Railway](https://railway.com) template for [Seafile](https://www.seafile.com/) Community Edition, the open-source file sync and share server with libraries, version history, sharing links and desktop and mobile sync clients.

This repo is what the template builds. Every service is built from a folder here, so when the version below is bumped on `main`, Railway shows everyone who deployed the template an "update available" notice, and they choose when to apply it.

## What it deploys

| Service | Built from | Version | Volume |
|---|---|---|---|
| **Seafile** (public) | [`seafile/`](seafile/) | Seafile CE **13.0.29**, `seafileltd/seafile-mc:13.0.29@sha256:9506f49d5e5065082c134e6348498eed5a5866ddbd94bd5a3e479a6c285bc61a` | `/shared` (libraries, config, logs) |
| **MariaDB** (private) | [`mariadb/`](mariadb/) | MariaDB **10.11.19** LTS, `mariadb:10.11.19@sha256:7d829180b5b2a9ba74f6242876ab401a0d7dd338a807e522ef92bc9698760f20` | `/var/lib/mysql` (data in `/var/lib/mysql/data`) |
| **Redis** (private) | Railway's Redis | Railway's image | `/data` |

- Seafile's built-in nginx listens on port 80 (`PORT=80`) and serves the web UI, the sync API (`/seafhttp`) and the static files on one domain. Health check: `/api2/ping/`.
- MariaDB 10.11 is the database Seafile's own Docker setup uses. Seafile creates its three databases (`ccnet_db`, `seafile_db`, `seahub_db`) and its `seafile` database user on the first start.
- Redis is Seafile's cache.

## Variables

| Service | Variable | Default | Notes |
|---|---|---|---|
| Seafile | `INIT_SEAFILE_ADMIN_EMAIL` | *(you enter it)* | Email of the first admin account. The only question at deploy time |
| Seafile | `INIT_SEAFILE_ADMIN_PASSWORD` | `${{secret(24)}}` | Generated. Read it in the Seafile service's **Variables** tab to log in the first time, then change it in Seafile |
| Seafile | `SEAFILE_SERVER_HOSTNAME` | `${{RAILWAY_PUBLIC_DOMAIN}}` | Public domain. Change it if you add a custom domain |
| Seafile | `JWT_PRIVATE_KEY` | `${{secret(48)}}` | Generated signing key |
| Seafile | `SEAFILE_MYSQL_DB_PASSWORD` | `${{secret(32)}}` | Generated password of the `seafile` database user |
| Seafile | `SEAFILE_MYSQL_DB_HOST`, `INIT_SEAFILE_MYSQL_ROOT_PASSWORD` | MariaDB references | Private network |
| Seafile | `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD` | Redis references | Private network |
| Seafile | `PORT` | `80` | Port of Seafile's built-in nginx |
| MariaDB | `MARIADB_ROOT_PASSWORD` | `${{secret(32)}}` | Generated |

`INIT_*` variables are read only on the very first start. Changing them later doesn't change the admin or the database.

The start script ([`seafile/railway-start.sh`](seafile/railway-start.sh)) sets the fixed settings: HTTPS URLs, database names, Redis cache, `TIME_ZONE=Etc/UTC`, logs to stdout. SeaDoc, the notification server and Seafile AI need extra services and are off. Email (SMTP), WebDAV and OnlyOffice/Collabora are optional: set them in `/shared/seafile/conf/seahub_settings.py` or `seafdav.conf` as the [Seafile manual](https://manual.seafile.com/13.0/) describes, and redeploy.

## Updates

- Patch releases (13.0.x) are bumped here: the `FROM` line changes, `CHANGELOG.md` gets an entry, and Railway offers the update to deployers. Seafile upgrades its database schema on start.
- Major versions (14.0 and later) can need manual steps. They're listed first in `CHANGELOG.md` before they land on `main`. Back up the `/shared` and MariaDB volumes before you apply one.

## License

The wrapper files in this repo are MIT licensed. Seafile Community Edition is open source and published by Seafile Ltd under its own licenses (the server core is AGPLv3, the Seahub web app Apache 2.0).

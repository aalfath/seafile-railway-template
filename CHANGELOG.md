# Changelog

Breaking changes are listed first in each entry. Read the entry before you apply an update from Railway.

## 2026-11-17: Seafile 13.0.29 (first release)

- Seafile CE `seafileltd/seafile-mc:13.0.29@sha256:9506f49d5e5065082c134e6348498eed5a5866ddbd94bd5a3e479a6c285bc61a` (latest stable; 14.0 is still in testing).
- MariaDB `mariadb:10.11.19@sha256:7d829180b5b2a9ba74f6242876ab401a0d7dd338a807e522ef92bc9698760f20` (10.11 LTS, as in Seafile's own Docker setup), data in `/var/lib/mysql/data` on the volume.
- Redis: Railway's Redis service, used as Seafile's cache.
- The Seafile start script sets HTTPS and the fixed settings, trusts the Railway domain for CSRF, and refuses a first start without an admin email and password, so the image's default admin (`me@example.com` / `asecret`) is never created.

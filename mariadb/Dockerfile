# MariaDB 10.11 LTS: Seafile's database (the version Seafile's own Docker setup uses).
# Official image, pinned by version and digest. Bump both together and add a CHANGELOG.md entry.
FROM mariadb:10.11.19@sha256:7d829180b5b2a9ba74f6242876ab401a0d7dd338a807e522ef92bc9698760f20

# Railway settings (data directory inside the volume, no DNS lookups on connect).
COPY railway.cnf /etc/mysql/conf.d/zz-railway.cnf

# Run mariadb-upgrade automatically when a newer image starts on an older data directory.
ENV MARIADB_AUTO_UPGRADE=1 \
    MYSQL_LOG_CONSOLE=true

EXPOSE 3306
CMD ["mariadbd"]

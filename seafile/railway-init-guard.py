#!/usr/bin/env python3
"""Recover from an interrupted first start of Seafile on Railway.

Seafile's first start creates its three databases and tables in MariaDB, then moves the
generated seafile-data folder onto the /shared volume. If the container is stopped between
those two steps (a redeploy or a variable change during the first boot), every later start
fails with "Table ... already exists".

This guard runs before Seafile starts, while /shared/seafile/seafile-data doesn't exist yet:
- databases empty: write a marker on the volume and let Seafile initialise as usual;
- databases have tables and the marker is on this volume: they came from this volume's own
  interrupted first start, so drop them (and the half-written config) and initialise again;
- databases have tables and no marker: refuse to start, because that's someone's real data.
"""
import os, shutil, sys, time
import pymysql

SHARED = "/shared/seafile"
MARKER = "/shared/.railway-first-start"

def env(k, d=""):
    return os.environ.get(k, d)

def main():
    if os.path.exists(os.path.join(SHARED, "seafile-data")):
        if os.path.exists(MARKER):
            os.unlink(MARKER)
        return 0
    dbs = [env("SEAFILE_MYSQL_DB_CCNET_DB_NAME"), env("SEAFILE_MYSQL_DB_SEAFILE_DB_NAME"), env("SEAFILE_MYSQL_DB_SEAHUB_DB_NAME")]
    deadline = time.time() + 600
    while True:
        try:
            conn = pymysql.connect(host=env("SEAFILE_MYSQL_DB_HOST"), port=int(env("SEAFILE_MYSQL_DB_PORT", "3306")),
                                   user="root", passwd=env("INIT_SEAFILE_MYSQL_ROOT_PASSWORD"), connect_timeout=5)
            break
        except Exception as e:
            if time.time() > deadline:
                print("railway-init-guard: MariaDB not reachable as root: %s" % e, file=sys.stderr)
                return 1
            print("railway-init-guard: waiting for MariaDB ...")
            time.sleep(3)
    with conn.cursor() as c:
        c.execute("SELECT table_schema, COUNT(*) FROM information_schema.tables WHERE table_schema IN (%s,%s,%s) GROUP BY table_schema", dbs)
        used = {r[0]: r[1] for r in c.fetchall()}
        if not used:
            os.makedirs("/shared", exist_ok=True)
            open(MARKER, "w").write("first start began %s\n" % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
            print("railway-init-guard: fresh databases, first start")
            return 0
        if not os.path.exists(MARKER):
            print("railway-init-guard: the Seafile databases %s already hold tables, but this volume has no Seafile data "
                  "and no unfinished first start. Refusing to start so nothing is overwritten. Restore the /shared volume, "
                  "or drop the databases yourself if they're unused." % sorted(used), file=sys.stderr)
            return 1
        print("railway-init-guard: the previous first start was interrupted; dropping its half-created databases %s and starting again" % sorted(used))
        for db in dbs:
            c.execute("DROP DATABASE IF EXISTS `%s`" % db.replace("`", ""))
    conn.close()
    for d in ("conf", "ccnet", "seahub-data", "pro-data"):
        p = os.path.join(SHARED, d)
        if os.path.islink(p) or os.path.isfile(p):
            os.unlink(p)
        elif os.path.isdir(p):
            shutil.rmtree(p)
    return 0

if __name__ == "__main__":
    sys.exit(main())

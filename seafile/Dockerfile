# Seafile Community Edition: the web UI (Seahub), file server and sync API.
# Official image, pinned by version and digest. Bump both together and add a CHANGELOG.md entry.
FROM seafileltd/seafile-mc:13.0.29@sha256:9506f49d5e5065082c134e6348498eed5a5866ddbd94bd5a3e479a6c285bc61a

# Railway reverse-proxy settings for Seahub (trusted HTTPS origin), read from the environment at every start.
COPY local_settings.py /opt/seafile/seafile-server-${SEAFILE_VERSION}/seahub/seahub/local_settings.py
COPY --chmod=755 railway-start.sh railway-init-guard.py /usr/local/bin/

EXPOSE 80
ENTRYPOINT ["/usr/local/bin/railway-start.sh"]

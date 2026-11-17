# Loaded by Seahub before conf/seahub_settings.py (which can still override it).
# Railway terminates HTTPS at its edge and sends X-Forwarded-Proto, so Django needs to trust
# the public origin for CSRF checks on logins and forms.
import os

_host = os.environ.get("SEAFILE_SERVER_HOSTNAME", "").strip().rstrip("/")
if _host:
    CSRF_TRUSTED_ORIGINS = ["https://" + _host, "http://" + _host]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

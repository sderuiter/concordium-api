import os


# Does a path exist?
# This is false for dangling symbolic links on systems that support them.
def exists(path):
    """Test whether a path exists.  Returns False for broken symbolic links"""
    try:
        os.stat(path)
    except (OSError, ValueError):
        return False
    return True


file_exists = exists("envdonotcommit.py")
if file_exists:
    from envdonotcommit import MONGODB_PASSWORD_LOCAL
    from envdonotcommit import NOTIFIER_API_TOKEN_LOCAL
    from envdonotcommit import API_TOKEN_LOCAL
    from envdonotcommit import FASTMAIL_TOKEN_LOCAL
    from envdonotcommit import FALLBACK_URI_LOCAL
    from envdonotcommit import HOSTNAME_PORT_LOCAL
else:
    MONGODB_PASSWORD_LOCAL = None
    NOTIFIER_API_TOKEN_LOCAL = None
    API_TOKEN_LOCAL = None
    FASTMAIL_TOKEN_LOCAL = None
    FALLBACK_URI_LOCAL = None
    HOSTNAME_PORT_LOCAL = None

BRANCH = os.environ.get("BRANCH", "dev")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "prod")
MONGODB_PASSWORD = os.environ.get("MONGODB_PASSWORD", MONGODB_PASSWORD_LOCAL)
NOTIFIER_API_TOKEN = os.environ.get("NOTIFIER_API_TOKEN", NOTIFIER_API_TOKEN_LOCAL)
API_TOKEN = os.environ.get("API_TOKEN", NOTIFIER_API_TOKEN_LOCAL)
FASTMAIL_TOKEN = os.environ.get("FASTMAIL_TOKEN", FASTMAIL_TOKEN_LOCAL)
FALLBACK_URI = os.environ.get("FALLBACK_URI", FALLBACK_URI_LOCAL)
HOSTNAME_PORT = os.environ.get("HOSTNAME_PORT", HOSTNAME_PORT_LOCAL)

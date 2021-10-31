from pathlib import Path

import environ

env = environ.Env()

# Set the project base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Take environment variables from .env file
environ.Env.read_env((BASE_DIR / '.env').as_posix())

if env.str('ENV') == 'PRODUCTION':
    from .production import *
elif env.str('ENV') == 'STAGING':
    from .staging import *
else:
    from .development import *

"""
WSGI config for stephenkinglibrary project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file if it exists
env_path = BASE_DIR / '.env'
if env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(env_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stephenkinglibrary.settings')

application = get_wsgi_application() 
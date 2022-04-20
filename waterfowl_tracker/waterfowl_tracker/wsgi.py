"""
WSGI config for waterfowl_tracker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
#import sys
#sys.path.insert(0,'/home/bitnami/.local/lib/python3.8/site-packages')
#sys.path.append('/home/bitnami/htdocs/wftracker.com')
#sys.path.append('/home/bitnami/htdocs/wftracker.com/waterfowl_tracker')
#os.environ.setdefault("PYTHON_EGG_CACHE", "/opt/bitnami/apache/htdocs/waterfowl_tracker/egg_cache")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'waterfowl_tracker.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# visit https://www.youtube.com/watch?v=Xjdv31k-Kf4 for apache2 configuration help
# STF downloaded video and other info in case post and video is gone

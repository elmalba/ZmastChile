#!/usr/bin/python
import os
import sys
import logging
reload(sys)
sys.setdefaultencoding("utf-8")
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/zamst")
os.chdir("/var/www/zamst")
FACEBOOK_APP_ID = '613776818694665'
FACEBOOK_APP_SECRET = 'd3946f7049d8d3903b2e296412c79e20'

from FlaskApp import app as application
application.secret_key = 'Linaeresmicorazon'

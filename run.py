#!flask/bin/python
# -*- coding: utf-8 -*-

from FlaskApp import app
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
#app.run(host='0.0.0.0', port=5000,debug = True)
app.secret_key = 'Linateamo'

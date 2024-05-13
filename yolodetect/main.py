from flask import *
from public import public
from admin import admin
from api import api
from vd_copy import *
import smtplib
from email.mime.text import MIMEText   
from flask_mail import Mail




app=Flask(__name__)
app.secret_key="abcd"
app.register_blueprint(public)
app.register_blueprint(admin)
app.register_blueprint(api,url_prefix='/api')

mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'pamuka16@gmail.com'
app.config['MAIL_PASSWORD'] = 'qgun bywf bros hzbl'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL']=True

app.run(debug=True,port=5080,host="0.0.0.0")
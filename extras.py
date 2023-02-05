from email.mime import image
from flask import render_template, request, flash, session, redirect, url_for, send_from_directory, Blueprint, Flask, make_response
from flask_login import login_required, current_user
from flask import current_app as app
from flask_mail import Mail, Message
import urllib.parse
import base64


extras = Blueprint('extras', __name__)

#### define init values in main #####
with app.app_context():
    ## Email Config
    UPLOAD_FOLDER2 = '/home/nea/zscaler/static/img/'
    app.config['UPLOAD_FOLDER2'] = UPLOAD_FOLDER2
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'zscalerautomationtelekom@gmail.com'
    app.config['MAIL_PASSWORD'] = 'aypmmkkkkscnziaa'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    mail = Mail(app)

@extras.route('/contact')
@login_required
def contact():  
    if current_user.is_authenticated:        
        return render_template('feedback.html', name=current_user.name, surname=current_user.surname)
    elif not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

@extras.route('/contact/send')
def email_template():
    return(render_template('email.html'))

@extras.route('/contact/send', methods=['POST'])
@login_required
def notification():
    if request.method == 'POST':
        text = request.form.get('message')
        subject = "Neues Feedback! von: " + current_user.name + ", " + current_user.surname + " <" + current_user.email + ">"
        msg = Message(sender = ("Zscaler Automation Bot",  'zscalerautomationtelekom@gmail.com'), recipients = ['georg.loeffler@telekom.de', 'andreas.bowkunnyj@telekom.de', 'jan.winkelmann@telekom.de'], subject=subject)
        #msg.body = text
        ###### Add Attachment
        with open('/home/nea/zscaler/static/img/T_security_rgb_p.png', 'rb') as fp:
            msg.attach('T_security_rgb_p.png', 'image/png', fp.read(), 'inline', headers=[['Content-ID','<logo>']]) 
            fp.seek(0)  # rewind your buffer
            image = urllib.parse.quote(base64.b64encode(fp.read()).decode()) # base64 encode & URL-escape
            msg.html = render_template('email.html', text=text, image=image, subject=subject)
    
        mail.send(msg)
        flash("Message was sent!", 'email')
    return redirect(url_for('extras.contact'))
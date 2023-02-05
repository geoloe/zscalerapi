from crypt import methods
import time
from flask import render_template, request, flash, session, redirect, url_for, send_from_directory, Blueprint, Flask, make_response
from flask import current_app as app
import os
from requests import delete
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from . import db
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from collections import defaultdict
# import requi9red module
import sys
  
# append the path of the
# parent directory
sys.path.append("..")


#initialize flask app
main = Blueprint('main', __name__)


def getid():
    print("meine kunde id lautet")
    print(session["kunde"])

#### define init values in main #####
with app.app_context():
    UPLOAD_FOLDER = '/home/nea/zscalerapi/input_data/'
    ALLOWED_EXTENSIONS = {'xlsx'}
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024

@main.route('/')
@login_required
def index():
    if current_user.is_authenticated:

        return render_template('index.html', name=current_user.name, surname=current_user.surname)
    elif not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name, surname=current_user.surname)

@main.route('/slcc')
@login_required
def slcc():
    return render_template('slcc.html', name=current_user.name, surname=current_user.surname)

@main.route('/location')
@login_required
def location():

    user = db.session.query(User).filter(User.name==current_user.name).first()
    project_info = db.session.query(Kunde.kunde_id, Kunde.kundenname).join(Kunde.user).filter(User.user_id==user.user_id).all()

    country, tz = my_data()
    print(project_info)

    return render_template('location.html', name=current_user.name, surname=current_user.surname, info=project_info, cn=country, timezone=tz)

@main.route('/apidata/message')
@login_required
def message():
    ###### Use session variable for customer
    ######
    ######

    kunde_id = int(session["kunde"])

    user = db.session.query(User).filter(User.name==current_user.name).first()
    # SELECT kundenname, api_key, cloud, customer_domain FROM kunden JOIN user ON user_id==<current logged in user>
    info = db.session.query(Kunde.kunde_id, Kunde.kundenname, Kunde.api_key, Kunde.cloud, Kunde.customer_domain, project).join(Kunde).join(User).filter(User.user_id==user.user_id, Kunde.kunde_id == kunde_id).all()    
        
    # SELECT kundenname, api_key, cloud, customer_domain FROM kunden JOIN user ON user_id==<current logged in user> AND admin.kunde_id==Kunde.kunde_id
    info2 = db.session.query(Admin.admin_id, Kunde.kundenname, Admin.email, Admin.name, Admin.surname).join(Kunde).filter(User.user_id==user.user_id, Admin.kunde_id==kunde_id).all()

    #print(info2)
    info3 = db.session.query(Kunde.kunde_id, Kunde.kundenname, Kunde.api_key, Kunde.cloud, Kunde.customer_domain, project).join(User).join(Kunde).filter(User.user_id==user.user_id).all()    
    
    return render_template('message.html', name=current_user.name, surname=current_user.surname, query=info, query2=info2, query3=info3, kunde_id=kunde_id)

@main.route('/config', methods = ['GET', 'POST'])
@login_required
def config():

    user = db.session.query(User).filter(User.name==current_user.name).first()

    # SELECT kundenname, api_key, cloud, customer_domain FROM kunden JOIN user ON user_id==<current logged in user>
    info = db.session.query(Kunde.kunde_id, Kunde.kundenname, Kunde.api_key, Kunde.cloud, Kunde.customer_domain, project).join(User).join(Kunde).filter(User.user_id==user.user_id).all()

    print(info)

    return render_template('config.html', name=current_user.name,surname=current_user.surname, is_admin=current_user.is_admin, query=info)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/get-cookie/')
def get_cookie():
    id = request.cookies.get('id')
    return id

@main.route('/apidata/uploader', methods = ['GET', 'POST'])
@login_required
def upload_file():    
    if request.method == 'POST':    
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('File nicht gültig!')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('Kein File ausgewählt!')
            return redirect(request.url)
        if allowed_file(file.filename) is False:
            flash('File nicht gültig!')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print("Filename is : " + app.config['UPLOAD_FOLDER'] + filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            session["message"] = 'true'
            session["file"]=filename
            return redirect(url_for('main.message', name=filename)+"#scriptform")
    return redirect(url_for('main.apidata'))

@main.route('/apidata/script_ausfuehren', methods = ['GET', 'POST'])
@login_required
def script_ausfuehren():
    #Jans Script ausführen
    #Filename zurückgeben in var speichern
    if request.method == 'GET':
        val = request.args['option']
        admin = request.args['option7']
        pwd = request.args['pwd.ad_pass_2']
        filename = session["file"]
        print("Kunde: " + session['kunde'])
        kunde_id = int(session["kunde"])
        user = db.session.query(User).filter(User.name==current_user.name).first()

        # SELECT kundenname, api_key, cloud, customer_domain FROM kunden JOIN user ON user_id==<current logged in user>
        info = db.session.query(Kunde.kunde_id, Kunde.kundenname, Kunde.api_key, Kunde.cloud, Kunde.customer_domain, project).join(Kunde).join(User).filter(User.user_id==user.user_id, Kunde.kunde_id == kunde_id).all() 
        
        adm = db.session.query(Admin.password).join(Kunde.user).filter(User.user_id==user.user_id, Admin.kunde_id==kunde_id).first()


        #check password
        if not check_password_hash(adm[0], pwd):
            print(adm[0])
            flash("Passwort ist falsch.")
            return redirect(url_for('main.apidata'))
        
        #from .change import something
        from zscalerapi import init, config
        init.init_script(admin, info[0][3], pwd, info[0][2], filename, val)
        #file = something(val)
        print(val)
        return redirect(url_for('main.download', filename=filename))

@main.route('/apidata/<path:filename>')
@login_required
def download(filename):
    # Appending app path to upload folder path within app root folder
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    print(uploads)
    flash("File: " + filename + " wurde geupdated und (Sub-)locations auf dem Zscaler ZIA Portal für den Kunden angelegt", 'update')
    # Returning file from appended path
    return send_from_directory(uploads, filename, as_attachment=True)

@main.route('/kundenconfig', methods = ['POST'])
@login_required
def commit_conf():
    kundenname=''
    apikey=''
    kundendomain=''
    url=''
    users= None
    users = request.form
    kundenname = request.form.get('ku')
    apikey = request.form.get('ap')
    kundendomain = request.form.get('kd')
    url = request.form.get('ul')

    users_list = []
    for key, value in users.items():
        print(key, value)
        users_list.append(value)
    users_list = users_list[3:-1]
    
    names = []
    print("Selected Users: ", users_list)  
    for name in users_list:
        names.append(name[2:])
    
    print("Selected Usernames: ", names)   
    
    kunden_query = Kunde.query.filter_by(api_key=apikey).first()
    if kunden_query: # if apikey is found, we want to redirect back to config page so user can try again
        flash("API Key existiert bereits und gehört dem Kunden " + kundenname)
        user = db.session.query(User).filter(User.name==current_user.name).first()
        customer = db.session.query(Kunde).filter(Kunde.api_key==apikey).first()
        #Check if association table has already an association to the user
        project_combi = db.session.query(project).join(Kunde).join(User).filter(Kunde.kunde_id == customer.kunde_id).all()
        project_combi2 = db.session.query(project).join(Kunde).join(User).filter(Kunde.kunde_id == customer.kunde_id, User.user_id == user.user_id).all()
        #print(project_combi)
        #if the association exists, then do nothing and return form site, else add association to the user adding the existing customer
        if project_combi and not project_combi2:
            #print(project_combi[0][1])
            new_project = project.insert().values(user_id=current_user.user_id, kunde_id=project_combi[0][1])

            db.session.execute(new_project)
            db.session.commit()
        return redirect(url_for('main.data'))
       
    kunden_query = Kunde.query.filter_by(customer_domain=kundendomain).first()
        
    if kunden_query: # if domain is found, we want to redirect back to config page so user can try again
        flash("Customer Domain existiert bereits und gehört dem Kunden " + kundenname)
        user = db.session.query(User).filter(User.name==current_user.name).first()
        customer = db.session.query(Kunde).filter(Kunde.customer_domain==kundendomain).first()
        #Check if association table has already an association to the user
        project_combi = db.session.query(project).join(Kunde).join(User).filter(Kunde.kunde_id == customer.kunde_id).all()
        project_combi2 = db.session.query(project).join(Kunde).join(User).filter(Kunde.kunde_id == customer.kunde_id, User.user_id == user.user_id).all()
        #print(project_combi)
        #if the association exists, then do nothing and return form site, else add association to the user adding the existing customer
        if project_combi and not project_combi2:
            #print(project_combi[0][1])
            new_project = project.insert().values(user_id=current_user.user_id, kunde_id=project_combi[0][1])

            db.session.execute(new_project)
            db.session.commit()
        return redirect(url_for('main.data'))

    if kundenname != 'None':
        new_customer = Kunde(kundenname=kundenname, api_key=apikey,  cloud=url, customer_domain=kundendomain)

    db.session.add(new_customer)
    db.session.commit()

    #### Web User in db 
    user = db.session.query(User).filter(User.name==current_user.name).first()
    #print(user.user_id)
    #### newly created customer
    customer = db.session.query(Kunde).filter(Kunde.api_key==apikey).first()
    #print(customer.kunde_id)

    #relation aufbauen
    ##### for current user
    #new_project = project.insert().values(user_id=user.user_id, kunde_id=customer.kunde_id)
    #for custom users

    ids = []
    for i in names:
        ids.append(db.session.query(User.user_id).filter(User.email==i).first())

    print("Selected not formatted IDS: ", ids) 
    ids_formatted = []
    for i,e in enumerate(ids):
        ids_formatted.append(e[0]) 
    
    print("Selected IDS: ", ids_formatted) 

    for i in ids_formatted:
        new_project = project.insert().values(user_id=i, kunde_id=customer.kunde_id)
        db.session.execute(new_project)
        db.session.commit()


    flash("Der Kunde: " + kundenname + " wurde erfolgreich gespeichert.")
    flash("'" + kundenname + "' wurde " + "' '".join(names) + " zugeordnet!", 'activity')

    return redirect(url_for('main.data'))

@main.route('/adminconfig', methods = ['POST'])
@login_required
def adminconfig():
    ad_email = request.form.get('ae')
    ad_name = request.form.get('an')
    ad_nachname = request.form.get('ane')
    ad_password = request.form.get('ap')
    ad_kunde = request.form.get('ak')

    print(ad_kunde)
    kunde_id = ad_kunde
    cu_id = int(kunde_id)

    if ad_kunde != 'None':
        new_customer = Admin(kunde_id=cu_id, email=ad_email,  password=generate_password_hash(ad_password, method='sha256'), name=ad_nachname, surname=ad_name)

    kunde_info = db.session.query(Kunde.kundenname).filter(Kunde.kunde_id==ad_kunde).first()

    db.session.add(new_customer)
    db.session.commit()
    
    flash("Der Admin: " + ad_email + " wurde für den Kunden "+ kunde_info[0] + " erfolgreich gespeichert.")
    flash("'" + ad_email + "'" + " wurde '" + kunde_info[0] + "' hinzugefügt!", 'activity')

    return redirect(url_for('main.data'))

@main.route('/commit', methods = ['GET', 'POST'])
@login_required
def commit():

    return render_template('commit.html', name=current_user.name, surname=current_user.surname)

@main.route('/config/data/' , methods = ['GET', 'POST'])
@login_required
def data():

    user = db.session.query(User).filter(User.name==current_user.name).first()

    # SELECT kundenname, api_key, cloud, customer_domain FROM kunden JOIN user ON user_id==<current logged in user>
    info = db.session.query(Kunde.kunde_id, Kunde.kundenname, Kunde.api_key, Kunde.cloud, Kunde.customer_domain).join(Kunde.user).filter(User.user_id==user.user_id).all()

    print(info)
    
    # SELECT kundenname, api_key, cloud, customer_domain FROM kunden JOIN user ON user_id==<current logged in user> AND admin.kunde_id==Kunde.kunde_id
    info2 = db.session.query(Admin.admin_id, Kunde.kundenname, Admin.email, Admin.name, Admin.surname).join(Kunde.user).filter(User.user_id==user.user_id, Admin.kunde_id==Kunde.kunde_id).all()
    
    all_customers = db.session.query(Kunde.kundenname).all()

    ### Search for users that have a common customer
    subquery = db.session.query(User.email).join(Kunde.user)
    customers = db.session.query(Kunde.kunde_id, Kunde.kundenname, Kunde.api_key, Kunde.cloud, Kunde.customer_domain, User.email).join(Kunde.user).filter(User.email.in_(subquery)).all()

    ### build list that contains lists of users that have a common customer
    liste = []
    counter = 0
    for item in info:
        liste.append([])
        for item2 in customers:
            #print(item[0:5])
            if item2[0:5] == item: 
                liste[counter].append(item2[-1])
        counter = counter + 1    
    print(liste)
    print(customers)

    ### build new list that contains customer information for the user that is logged in and also which users are assigned to that customer
    all_info = []
    counter = 0
    for item in info:
        all_info.append(list(item))
        for i in item:
            if i == item[-1]:
                all_info[counter].append(liste[counter])          
        counter = counter + 1 
    print(all_info)
    print(info)
    
    assign_info = db.session.query(User.email, Kunde.kundenname).join(Kunde.user).all()
    all_users = db.session.query(User.email).all()

    #print(type(assign_info))

    #print("Users without customers: ")
    #print(all_users)

    #print("Vorher: ", assign_info)
    d = defaultdict(list)
    for name, customer in assign_info:
        d[name].append(customer)   
    
    other_users = []
    for n in all_users:
        if n not in d:
            other_users += n

    for n in other_users:
        print(n)
        if n not in d:
            d[n] = []

    selection = defaultdict(list)
    for key in d:
        for i in all_customers:
            for p in i:
                if not isinstance(p, int):
                    selection[key].append(p)

    print(d)

    other_customers = []
    for n in all_customers:
        if n not in d:
            other_customers += n
    print(other_customers)

    return render_template('data.html', name=current_user.name, surname=current_user.surname, is_admin=current_user.is_admin, query=info, query2=info2, assign=d, customers=selection, alle_kunden=other_customers, awesome=all_info)


@main.route('/api' , methods = ['GET', 'POST'])
@login_required
def api():

    user = db.session.query(User).filter(User.name==current_user.name).first()

    # SELECT kundenname, api_key, cloud, customer_domain FROM kunden JOIN user ON user_id==<current logged in user>
    info = db.session.query(Kunde.kunde_id, Kunde.kundenname, Kunde.api_key, Kunde.cloud, Kunde.customer_domain).join(Kunde.user).filter(User.user_id==user.user_id).all()
    
    # SELECT kundenname, api_key, cloud, customer_domain FROM kunden JOIN user ON user_id==<current logged in user> AND admin.kunde_id==Kunde.kunde_id
    info2 = db.session.query(Admin.admin_id, Kunde.kundenname, Admin.email, Admin.name, Admin.surname).join(Kunde.user).filter(User.user_id==user.user_id, Admin.kunde_id==Kunde.kunde_id).all()

    #print(info2)

    return render_template('api.html', name=current_user.name, surname=current_user.surname, query=info, query2=info2)

@main.route('/apidata' , methods = ['GET', 'POST'])
@login_required
def apidata():
    session["message"] = 'false' 
    kunde = ''

    if request.method == 'POST':
        kunde = request.form.get('admin_kunde')
        if kunde != "":
            session["kunde"] = kunde
    
    print(session["kunde"])
    if kunde != "" or session["kunde"] != "":
        
        if session["kunde"] != "":
            kunde_id = int(session["kunde"], base=10)
        else:
            kunde_id = int(kunde, base=10)

        user = db.session.query(User).filter(User.name==current_user.name).first()

        # SELECT kundenname, api_key, cloud, customer_domain FROM kunden JOIN user ON user_id==<current logged in user>
        info = db.session.query(Kunde.kunde_id, Kunde.kundenname, Kunde.api_key, Kunde.cloud, Kunde.customer_domain, project).join(Kunde).join(User).filter(User.user_id==user.user_id, Kunde.kunde_id == kunde_id).all()    
 
        #print(kunde_id)
        
        # SELECT kundenname, api_key, cloud, customer_domain FROM kunden JOIN user ON user_id==<current logged in user> AND admin.kunde_id==Kunde.kunde_id
        info2 = db.session.query(Admin.admin_id, Kunde.kundenname, Admin.email, Admin.name, Admin.surname).join(Kunde).filter(User.user_id==user.user_id, Admin.kunde_id==kunde_id).all()

        #print(info2)
        info3 = db.session.query(Kunde.kunde_id, Kunde.kundenname, Kunde.api_key, Kunde.cloud, Kunde.customer_domain, project).join(User).join(Kunde).filter(User.user_id==user.user_id).all()
        #print(info3)
        resp = make_response(render_template('apidata.html', name=current_user.name, surname=current_user.surname, query=info, query2=info2, query3=info3, kunde_id=kunde_id))
        resp.set_cookie( "id", kunde, samesite=None)
        #return render_template('apidata.html', name=current_user.name, surname=current_user.surname, query=info, query2=info2, query3=info3, kunde_id=kunde_id)
        return resp
    return redirect(url_for('main.api'))

@main.route('/admin_script', methods = ['GET', 'POST'])
@login_required
def admin_script():
    admin = ''
    kunde = ''
    password = ''
    if request.method == 'POST':
        admin = request.form.get('admin')
        print("Admin: ", admin)
        kunde = request.form.get('cu')
        print("Kunde: ", kunde)
        password = request.form.get('ad_pass')
        #button_val = request.form.get('admin_csv')
        #button_val = request.form.get('url_csv')
        #print(button_val)

    if admin != "":
        admin = int(admin)
       
    if kunde != "":
        kunde = int(kunde)

    #print("Password: ", password)

    
    user = db.session.query(User).filter(User.name==current_user.name).first()


    info = db.session.query(Admin.admin_id, Kunde.kundenname, Kunde.api_key, Admin.email, Admin.name, Admin.surname, Kunde.cloud, Admin.password).join(Kunde).filter(User.user_id==user.user_id, Admin.kunde_id==kunde, Admin.admin_id == admin).all()
    #print(info)

    if not check_password_hash(info[0][7], password):
        flash('Bitte prüfe deine Anmeldedaten und versuche es erneut.')
        return redirect(url_for('main.api')) # if the user doesn't exist or password is wrong, reload the page

    from .get_admins import obfuscateApiKey, initiate_Session, get_admin, create_csv, get_url_categories, get_fw_policies, cleanup
    now, key = obfuscateApiKey(info[0][2], info[0][6])
    new_sesh = initiate_Session(now, key, info[0][3], password, info[0][6])
    if new_sesh == 'AUTHENTICATION_FAILED':
        flash('Die Authentifzierung für den Kunden der Zscaler Cloud ist fehlgeschlagen.')
        return redirect(url_for('main.api')) # if the authentication fails, reload the page       
    
    response = None
    file = ''
    result = None
    my_list = None
    dct = None
    if request.method == 'POST':
        if request.form.get('admin_csv') == 'Admin':
            response, val = get_admin(new_sesh, info[0][6])
            result, my_list, dct = cleanup(response, val)
            file = 'admins'
        elif request.form.get('url_csv') == 'URL':
            response, val = get_url_categories(new_sesh, info[0][6])
            file = 'urls'
            result, my_list, dct = cleanup(response, val)
        else:
            response, val = get_fw_policies(new_sesh, info[0][6])
            file = 'fw_policies'
            result, my_list, dct = cleanup(response, val)

    tm = time.strftime('%Y-%m-%d')
    file = file + '-' + info[0][1] + '_' + tm
    result, file = create_csv(file, my_list, dct, result)
    return redirect(url_for('main.download_admin', filename=file))

@main.route('/download_admin/<path:filename>')
@login_required
def download_admin(filename):
    # Appending app path to upload folder path within app root folder
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    # Returning file from appended path
    return send_from_directory(uploads, filename, as_attachment=True)

@main.route('/data/edit', methods=['GET', 'POST'])
def edit():
    #### Check for same Values in ALL OTHER items in database ### Check for integrity errors
    users = None

    print(request.form.get('ku-id'))
    print(request.form.get('kundenname-edit'))
    print(request.form.get('kundendomain-edit'))
    print(request.form.get('apikey-edit'))
    print(request.form.get('url-edit'))
    users = request.form
    
    users_list = list(users)
    users_list = users_list[3:-2]
    print(users_list)

    #get emails
    emails = []
    for i in users_list:
        emails.append(i[2:])
    
    print("User Emails: ")
    print(emails)

    #get correct user ids
    ids = []
    for i in emails:
        test = db.session.query(User.user_id).filter(User.email == i).first()
        ids.append(list(test))
    
    new_ids = []
    for i in ids:
        for number in i:
            new_ids.append(number)
    print("User IDS: ")
    print(new_ids)

    ##Delete all projects for that user 
    for i in ids:
        db.session.query(project).filter_by(kunde_id=int(request.form.get('ku-id'))).delete()
        db.session.commit()

    #Assign new users to customer
    for i in new_ids:
        new_project = project.insert().values(user_id=i, kunde_id=int(request.form.get('ku-id')))
        db.session.execute(new_project)
        db.session.commit()
 
    qry = db.session.query(Kunde).filter(
                Kunde.kunde_id==request.form.get('ku-id'))
    kunde = qry.first()

    print(kunde.kundenname, kunde.api_key, kunde.cloud, kunde.customer_domain)
    
    kunde.kundenname = request.form.get('kundenname-edit')
    kunde.api_key = request.form.get('apikey-edit')
    kunde.cloud = request.form.get('url-edit')
    kunde.customer_domain = request.form.get('kundendomain-edit')

    db.session.commit()

    flash('Der Kunde ' + kunde.kundenname + ' wurde erfolgreich editiert')
    #flash('Der Kunde ' + kunde.kundenname + ' wurde erfolgreich editiert', 'activity')
    flash("'" + request.form.get('kundenname-edit') + "'" + " gehört jetzt: '" + "' '".join(emails) + "'" , 'activity')

    return redirect(url_for('main.data'))

@main.route('/data/loeschen', methods=['GET', 'POST'])
def loeschen():
    if request.method == 'POST':
        print(request.form.get('admin-id'))
        print(request.form.get('loeschen-kunde-id'))
 
    #db.session.query(Admin).filter(Admin.admin_id==request.form.get('admin-id')).delete()
    if request.form.get('admin-id') != None:
        admin = db.session.query(Admin).filter(Admin.admin_id==request.form.get('admin-id')).first()

        flash('Der Admin ' + admin.surname + ' ' + admin.name + ' mit der LoginID ' + admin.email + ' wurde erfolgreich gelöscht.')
        flash("'" + admin.email + "'" + ' wurde erfolgreich gelöscht.', 'activity')

        db.session.query(Admin).filter(Admin.admin_id==request.form.get('admin-id')).delete()
        
        db.session.commit()
    return redirect(url_for('main.data'))

@main.route('/config/assign', methods=['GET', 'POST'])
def assign():
    # TO DO
    users = request.form

    print(users)
    counter = 0
    ids = []
    user_email = None
    for key, value in users.items():
        if counter != 0:
            key = int(key[0])
            ids.append(key)
        else:
            user_email = key
        counter = counter+1

    print("Selected Customer IDS: ", ids)

    names = []
    counter = 0
    for key, value in users.items():
        if counter != 0:
            key = key[2:]
            names.append(key)
        counter = counter+1
    
    print("Selected Customers: ", names)

    print("useremail: " + user_email) 

    # Get user id

    test = db.session.query(User.user_id).filter(User.email == user_email).first()

    u_id = None
    for i,e in enumerate(test):
        u_id = e

    ##Delete all projects for that user 
    #for i in ids:
    db.session.query(project).filter_by(user_id=u_id).delete()
    db.session.commit()

    for i in ids:
        new_project = project.insert().values(user_id=u_id, kunde_id=i)
        db.session.execute(new_project)
        db.session.commit()
    
    ##Assign selected projects to that user

    flash("'" + user_email + "'" + " gehören jetzt: '" + "' '".join(names) + "'" , 'activity')
    return redirect(url_for('main.data'))


def my_data():
    country = [
    ("NONE"),
    ("AFGHANISTAN"),
    ("ALAND_ISLANDS"),
    ("ALBANIA"),
    ("ALGERIA"),
    ("AMERICAN_SAMOA"),
    ("ANDORRA"),
    ("ANGOLA"),
    ("ANGUILLA"),
    ("ANTARCTICA"),
    ("ANTIGUA_AND_BARBUDA"),
    ("ARGENTINA"),
    ("ARMENIA"),
    ("ARUBA"),
    ("AUSTRALIA"),
    ("AUSTRIA"),
    ("AZERBAIJAN"),
    ("BAHAMAS"),
    ("BAHRAIN"),
    ("BANGLADESH"),
    ("BARBADOS"),
    ("BELARUS"),
    ("BELGIUM"),
    ("BELIZE"),
    ("BENIN"),
    ("BERMUDA"),
    ("BHUTAN"),
    ("BOLIVIA"),
    ("BOSNIA_AND_HERZEGOVINA"),
    ("BOTSWANA"),
    ("BRAZIL"),
    ("BRITISH_INDIAN_OCEAN_TERRITORY"),
    ("BRUNEI_DARUSSALAM"),
    ("BULGARIA"),
    ("BURKINA_FASO"),
    ("BURUNDI"),
    ("CAMBODIA"),
    ("CAMEROON"),
    ("CANADA"),
    ("CAPE_VERDE"),
    ("CAYMAN_ISLANDS"),
    ("CENTRAL_AFRICAN_REPUBLIC"),
    ("CHAD"),
    ("CHILE"),
    ("CHINA"),
    ("CHRISTMAS_ISLAND"),
    ("COCOS_KEELING_ISLANDS"),
    ("COLOMBIA"),
    ("COMOROS"),
    ("DEMOCRATIC_REPUBLIC_OF_CONGO_CONGO_KINSHASA"),
    ("CONGO_CONGO_BRAZZAVILLE"),
    ("COOK_ISLANDS"),
    ("COSTA_RICA"),
    ("COTE_DIVOIRE"),
    ("CROATIA"),
    ("CUBA"),
    ("CYPRUS"),
    ("CZECH_REPUBLIC"),
    ("DENMARK"),
    ("DJIBOUTI"),
    ("DOMINICAN_REPUBLIC"),
    ("DOMINICA"),
    ("ECUADOR"),
    ("EGYPT"),
    ("EL_SALVADOR"),
    ("EQUATORIAL_GUINEA"),
    ("ERITREA"),
    ("ESTONIA"),
    ("ETHIOPIA"),
    ("FALKLAND_ISLANDS"),
    ("FAROE_ISLANDS"),
    ("FIJI"),
    ("FINLAND"),
    ("FRANCE"),
    ("FRENCH_GUIANA"),
    ("FRENCH_POLYNESIA"),
    ("FRENCH_SOUTHERN_TERRITORIES"),
    ("GABON"),
    ("GAMBIA"),
    ("GEORGIA"),
    ("GERMANY"),
    ("GHANA"),
    ("GIBRALTAR"),
    ("GREECE"),
    ("GREENLAND"),
    ("GRENADA"),
    ("GUADELOUPE"),
    ("GUAM"),
    ("GUATEMALA"),
    ("GUERNSEY"),
    ("GUINEA_BISSAU"),
    ("GUINEA"),
    ("GUYANA"),
    ("HAITI"),
    ("HONDURAS"),
    ("HONG_KONG"),
    ("HUNGARY"),
    ("ICELAND"),
    ("INDIA"),
    ("INDONESIA"),
    ("IRAN"),
    ("IRAQ"),
    ("IRELAND"),
    ("ISLE_OF_MAN"),
    ("ISRAEL"),
    ("ITALY"),
    ("JAMAICA"),
    ("JAPAN"),
    ("JERSEY"),
    ("JORDAN"),
    ("KAZAKHSTAN"),
    ("KENYA"),
    ("KIRIBATI"),
    ("KOREA_DEMOCRATIC_PEOPLES_REPUBLIC_OF"),
    ("KOREA_REPUBLIC_OF"),
    ("KUWAIT"),
    ("KYRGYZSTAN"),
    ("LAO_PEOPLES_DEMOCRATIC_REPUBLIC"),
    ("LATVIA"),
    ("LEBANON"),
    ("LESOTHO"),
    ("LIBERIA"),
    ("LIBYAN_ARAB_JAMAHIRIYA"),
    ("LIECHTENSTEIN"),
    ("LITHUANIA"),
    ("LUXEMBOURG"),
    ("MACAO"),
    ("MACEDONIA_THE_FORMER_YUGOSLAV_REPUBLIC_OF"),
    ("MADAGASCAR"),
    ("MALAWI"),
    ("MALAYSIA"),
    ("MALDIVES"),
    ("MALI"),
    ("MALTA"),
    ("MARSHALL_ISLANDS"),
    ("MARTINIQUE"),
    ("MAURITANIA"),
    ("MAURITIUS"),
    ("MAYOTTE"),
    ("MEXICO"),
    ("MICRONESIA_FEDERATED_STATES_OF"),
    ("MOLDOVA"),
    ("MONACO"),
    ("MONGOLIA"),
    ("MONTENEGRO"),
    ("MONTSERRAT"),
    ("MOROCCO"),
    ("MOZAMBIQUE"),
    ("MYANMAR"),
    ("NAMIBIA"),
    ("NAURU"),
    ("NEPAL"),
    ("NETHERLANDS_ANTILLES"),
    ("NETHERLANDS"),
    ("NEW_CALEDONIA"),
    ("NEW_ZEALAND"),
    ("NICARAGUA"),
    ("NIGERIA"),
    ("NIGER"),
    ("NIUE"),
    ("NORFOLK_ISLAND"),
    ("NORTHERN_MARIANA_ISLANDS"),
    ("NORWAY"),
    ("OCCUPIED_PALESTINIAN_TERRITORY"),
    ("OMAN"),
    ("PAKISTAN"),
    ("PALAU"),
    ("PANAMA"),
    ("PAPUA_NEW_GUINEA"),
    ("PARAGUAY"),
    ("PERU"),
    ("PHILIPPINES"),
    ("PITCAIRN"),
    ("POLAND"),
    ("PORTUGAL"),
    ("PUERTO_RICO"),
    ("QATAR"),
    ("REUNION"),
    ("ROMANIA"),
    ("RUSSIAN_FEDERATION"),
    ("RWANDA"),
    ("SAINT_BARTHELEMY"),
    ("SAINT_KITTS_AND_NEVIS"),
    ("SAINT_LUCIA"),
    ("SAINT_MARTIN_FRENCH_PART"),
    ("SAINT_VINCENT_AND_THE_GRENADINES"),
    ("SAMOA"),
    ("SAN_MARINO"),
    ("SAO_TOME_AND_PRINCIPE"),
    ("SAUDI_ARABIA"),
    ("SENEGAL"),
    ("SERBIA"),
    ("SEYCHELLES"),
    ("SIERRA_LEONE"),
    ("SINGAPORE"),
    ("SLOVAKIA"),
    ("SLOVENIA"),
    ("SOLOMON_ISLANDS"),
    ("SOMALIA"),
    ("SOUTH_AFRICA"),
    ("SOUTH_GEORGIA_AND_THE_SOUTH_SANDWICH_ISLANDS"),
    ("SPAIN"),
    ("SRI_LANKA"),
    ("ST_HELENA"),
    ("ST_PIERRE_AND_MIQUELON"),
    ("SUDAN"),
    ("SURINAME"),
    ("SVALBARD_AND_JAN_MAYEN_ISLANDS"),
    ("SWAZILAND"),
    ("SWEDEN"),
    ("SWITZERLAND"),
    ("SYRIAN_ARAB_REPUBLIC"),
    ("TAIWAN"),
    ("TAJIKISTAN"),
    ("TANZANIA"),
    ("THAILAND"),
    ("TIMOR_LESTE"),
    ("TOGO"),
    ("TOKELAU"),
    ("TONGA"),
    ("TRINIDAD_AND_TOBAGO"),
    ("TUNISIA"),
    ("TURKEY"),
    ("TURKMENISTAN"),
    ("TURKS_AND_CAICOS_ISLANDS"),
    ("TUVALU"),
    ("UGANDA"),
    ("UKRAINE"),
    ("UNITED_ARAB_EMIRATES"),
    ("UNITED_KINGDOM"),
    ("UNITED_STATES_MINOR_OUTLYING_ISLANDS"),
    ("UNITED_STATES"),
    ("URUGUAY"),
    ("UZBEKISTAN"),
    ("VANUATU"),
    ("VATICAN_CITY_STATE"),
    ("VENEZUELA"),
    ("VIET_NAM"),
    ("VIRGIN_ISLANDS_BRITISH"),
    ("VIRGIN_ISLANDS_US"),
    ("WALLIS_AND_FUTUNA_ISLANDS"),
    ("WESTERN_SAHARA"),
    ("YEMEN"),
    ("ZAMBIA"),
    ("ZIMBABWE")]

    tz = [
    ("NOT_SPECIFIED"),
    ("GMT_12_00_DATELINE"),
    ("GMT_11_00_SAMOA"),
    ("GMT_10_00_US_HAWAIIAN_TIME"),
    ("GMT_09_30_MARQUESAS"),
    ("GMT_09_00_US_ALASKA_TIME"),
    ("GMT_08_30_PITCARN"),
    ("GMT_08_00_PACIFIC_TIME"),
    ("GMT_07_00_US_MOUNTAIN_TIME"),
    ("GMT_07_00_US_MOUNTAIN_TIME_ARIZONA"),
    ("GMT_06_00_US_CENTRAL_TIME"),
    ("GMT_06_00_MEXICO"),
    ("GMT_05_00_US_EASTERN_TIME"),
    ("GMT_05_00_US_EASTERN_TIME_INDIANA"),
    ("GMT_05_00_COLUMBIA_PERU_SOUTH_AMERICA"),
    ("GMT_04_00_ATLANTIC_TIME"),
    ("GMT_03_30_NEWFOUNDLAND_CANADA"),
    ("GMT_03_00_ARGENTINA"),
    ("GMT_03_00_BRAZIL"),
    ("GMT_02_00_MID_ATLANTIC"),
    ("GMT_01_00_AZORES"),
    ("GMT"),
    ("GMT_01_00_WESTERN_EUROPE_GMT_01_00"),
    ("GMT_02_00_EASTERN_EUROPE_GMT_02_00"),
    ("GMT_02_00_EGYPT_GMT_02_00"),
    ("GMT_02_00_ISRAEL_GMT_02_00"),
    ("GMT_03_00_RUSSIA_GMT_03_00"),
    ("GMT_03_00_SAUDI_ARABIA_GMT_03_00"),
    ("GMT_03_30_IRAN_GMT_03_30"),
    ("GMT_04_00_ARABIAN_GMT_04_00"),
    ("GMT_04_30_AFGHANISTAN_GMT_04_30"),
    ("GMT_05_00_PAKISTAN_WEST_ASIA_GMT_05_00"),
    ("GMT_05_30_INDIA_GMT_05_30"),
    ("GMT_06_00_BANGLADESH_CENTRAL_ASIA_GMT_06_00"),
    ("GMT_06_30_BURMA_GMT_06_30"),
    ("GMT_07_00_BANGKOK_HANOI_JAKARTA_GMT_07_00"),
    ("GMT_08_00_CHINA_TAIWAN_GMT_08_00"),
    ("GMT_08_00_SINGAPORE_GMT_08_00"),
    ("GMT_08_00_AUSTRALIA_WT_GMT_08_00"),
    ("GMT_09_00_JAPAN_GMT_09_00"),
    ("GMT_09_00_KOREA_GMT_09_00"),
    ("GMT_09_30_AUSTRALIA_CT_GMT_09_30"),
    ("GMT_10_00_AUSTRALIA_ET_GMT_10_00"),
    ("GMT_10_30_AUSTRALIA_LORD_HOWE_GMT_10_30"),
    ("GMT_11_00_CENTRAL_PACIFIC_GMT_11_00"),
    ("GMT_11_30_NORFOLK_ISLANDS_GMT_11_30"),
    ("GMT_12_00_FIJI_NEW_ZEALAND_GMT_12_00"),
    ("AFGHANISTAN_ASIA_KABUL"),
    ("ALAND_ISLANDS_EUROPE_MARIEHAMN"),
    ("ALBANIA_EUROPE_TIRANE"),
    ("ALGERIA_AFRICA_ALGIERS"),
    ("AMERICAN_SAMOA_PACIFIC_PAGO_PAGO"),
    ("ANDORRA_EUROPE_ANDORRA"),
    ("ANGOLA_AFRICA_LUANDA"),
    ("ANGUILLA_AMERICA_ANGUILLA"),
    ("ANTARCTICA_CASEY"),
    ("ANTARCTICA_DAVIS"),
    ("ANTARCTICA_DUMONTDURVILLE"),
    ("ANTARCTICA_MAWSON"),
    ("ANTARCTICA_MCMURDO"),
    ("ANTARCTICA_PALMER"),
    ("ANTARCTICA_ROTHERA"),
    ("ANTARCTICA_SOUTH_POLE"),
    ("ANTARCTICA_SYOWA"),
    ("ANTARCTICA_VOSTOK"),
    ("ANTIGUA_AND_BARBUDA_AMERICA_ANTIGUA"),
    ("ARGENTINA_AMERICA_ARGENTINA_BUENOS_AIRES"),
    ("ARGENTINA_AMERICA_ARGENTINA_CATAMARCA"),
    ("ARGENTINA_AMERICA_ARGENTINA_CORDOBA"),
    ("ARGENTINA_AMERICA_ARGENTINA_JUJUY"),
    ("ARGENTINA_AMERICA_ARGENTINA_LA_RIOJA"),
    ("ARGENTINA_AMERICA_ARGENTINA_MENDOZA"),
    ("ARGENTINA_AMERICA_ARGENTINA_RIO_GALLEGOS"),
    ("ARGENTINA_AMERICA_ARGENTINA_SAN_JUAN"),
    ("ARGENTINA_AMERICA_ARGENTINA_TUCUMAN"),
    ("ARGENTINA_AMERICA_ARGENTINA_USHUAIA"),
    ("ARMENIA_ASIA_YEREVAN"),
    ("ARUBA_AMERICA_ARUBA"),
    ("AUSTRALIA_ADELAIDE"),
    ("AUSTRALIA_BRISBANE"),
    ("AUSTRALIA_BROKEN_HILL"),
    ("AUSTRALIA_CURRIE"),
    ("AUSTRALIA_DARWIN"),
    ("AUSTRALIA_EUCLA"),
    ("AUSTRALIA_HOBART"),
    ("AUSTRALIA_LINDEMAN"),
    ("AUSTRALIA_LORD_HOWE"),
    ("AUSTRALIA_MELBOURNE"),
    ("AUSTRALIA_PERTH"),
    ("AUSTRALIA_SYDNEY"),
    ("AUSTRIA_EUROPE_VIENNA"),
    ("AZERBAIJAN_ASIA_BAKU"),
    ("BAHAMAS_AMERICA_NASSAU"),
    ("BAHRAIN_ASIA_BAHRAIN"),
    ("BANGLADESH_ASIA_DHAKA"),
    ("BARBADOS_AMERICA_BARBADOS"),
    ("BELARUS_EUROPE_MINSK"),
    ("BELGIUM_EUROPE_BRUSSELS"),
    ("BELIZE_AMERICA_BELIZE"),
    ("BENIN_AFRICA_PORTO_NOVO"),
    ("BERMUDA_ATLANTIC_BERMUDA"),
    ("BHUTAN_ASIA_THIMPHU"),
    ("BOLIVIA_AMERICA_LA_PAZ"),
    ("BOSNIA_AND_HERZEGOVINA_EUROPE_SARAJEVO"),
    ("BOTSWANA_AFRICA_GABORONE"),
    ("BRAZIL_AMERICA_ARAGUAINA"),
    ("BRAZIL_AMERICA_BAHIA"),
    ("BRAZIL_AMERICA_BELEM"),
    ("BRAZIL_AMERICA_BOA_VISTA"),
    ("BRAZIL_AMERICA_CAMPO_GRANDE"),
    ("BRAZIL_AMERICA_CUIABA"),
    ("BRAZIL_AMERICA_EIRUNEPE"),
    ("BRAZIL_AMERICA_FORTALEZA"),
    ("BRAZIL_AMERICA_MACEIO"),
    ("BRAZIL_AMERICA_MANAUS"),
    ("BRAZIL_AMERICA_NORONHA"),
    ("BRAZIL_AMERICA_PORTO_VELHO"),
    ("BRAZIL_AMERICA_RECIFE"),
    ("BRAZIL_AMERICA_RIO_BRANCO"),
    ("BRAZIL_AMERICA_SAO_PAULO"),
    ("BRITISH_INDIAN_OCEAN_TERRITORY_INDIAN_CHAGOS"),
    ("BRUNEI_DARUSSALAM_ASIA_BRUNEI"),
    ("BULGARIA_EUROPE_SOFIA"),
    ("BURKINA_FASO_AFRICA_OUAGADOUGOU"),
    ("BURUNDI_AFRICA_BUJUMBURA"),
    ("CAMBODIA_ASIA_PHNOM_PENH"),
    ("CAMEROON_AFRICA_DOUALA"),
    ("CANADA_AMERICA_ATIKOKAN"),
    ("CANADA_AMERICA_BLANC_SABLON"),
    ("CANADA_AMERICA_CAMBRIDGE_BAY"),
    ("CANADA_AMERICA_DAWSON_CREEK"),
    ("CANADA_AMERICA_DAWSON"),
    ("CANADA_AMERICA_EDMONTON"),
    ("CANADA_AMERICA_GLACE_BAY"),
    ("CANADA_AMERICA_GOOSE_BAY"),
    ("CANADA_AMERICA_HALIFAX"),
    ("CANADA_AMERICA_INUVIK"),
    ("CANADA_AMERICA_IQALUIT"),
    ("CANADA_AMERICA_MONCTON"),
    ("CANADA_AMERICA_MONTREAL"),
    ("CANADA_AMERICA_NIPIGON"),
    ("CANADA_AMERICA_PANGNIRTUNG"),
    ("CANADA_AMERICA_RAINY_RIVER"),
    ("CANADA_AMERICA_RANKIN_INLET"),
    ("CANADA_AMERICA_REGINA"),
    ("CANADA_AMERICA_RESOLUTE"),
    ("CANADA_AMERICA_ST_JOHNS"),
    ("CANADA_AMERICA_SWIFT_CURRENT"),
    ("CANADA_AMERICA_THUNDER_BAY"),
    ("CANADA_AMERICA_TORONTO"),
    ("CANADA_AMERICA_VANCOUVER"),
    ("CANADA_AMERICA_WHITEHORSE"),
    ("CANADA_AMERICA_WINNIPEG"),
    ("CANADA_AMERICA_YELLOWKNIFE"),
    ("CAPE_VERDE_ATLANTIC_CAPE_VERDE"),
    ("CAYMAN_ISLANDS_AMERICA_CAYMAN"),
    ("CENTRAL_AFRICAN_REPUBLIC_AFRICA_BANGUI"),
    ("CHAD_AFRICA_NDJAMENA"),
    ("CHILE_AMERICA_SANTIAGO"),
    ("CHILE_PACIFIC_EASTER"),
    ("CHINA_ASIA_CHONGQING"),
    ("CHINA_ASIA_HARBIN"),
    ("CHINA_ASIA_KASHGAR"),
    ("CHINA_ASIA_SHANGHAI"),
    ("CHINA_ASIA_URUMQI"),
    ("CHRISTMAS_ISLAND_INDIAN_CHRISTMAS"),
    ("COCOS_KEELING_ISLANDS_INDIAN_COCOS"),
    ("COLOMBIA_AMERICA_BOGOTA"),
    ("COMOROS_INDIAN_COMORO"),
    ("DEMOCRATIC_REPUBLIC_OF_CONGO_CONGO_KINSHASA_AFRICA_KINSHASA"),
    ("DEMOCRATIC_REPUBLIC_OF_CONGO_CONGO_KINSHASA_AFRICA_LUBUMBASHI"),
    ("CONGO_CONGO_BRAZZAVILLE_AFRICA_BRAZZAVILLE"),
    ("COOK_ISLANDS_PACIFIC_RAROTONGA"),
    ("COSTA_RICA_AMERICA_COSTA_RICA"),
    ("COTE_DIVOIRE_AFRICA_ABIDJAN"),
    ("CROATIA_EUROPE_ZAGREB"),
    ("CUBA_AMERICA_HAVANA"),
    ("CYPRUS_ASIA_NICOSIA"),
    ("CZECH_REPUBLIC_EUROPE_PRAGUE"),
    ("DENMARK_EUROPE_COPENHAGEN"),
    ("DJIBOUTI_AFRICA_DJIBOUTI"),
    ("DOMINICAN_REPUBLIC_AMERICA_SANTO_DOMINGO"),
    ("DOMINICA_AMERICA_DOMINICA"),
    ("ECUADOR_AMERICA_GUAYAQUIL"),
    ("ECUADOR_PACIFIC_GALAPAGOS"),
    ("EGYPT_AFRICA_CAIRO"),
    ("EL_SALVADOR_AMERICA_EL_SALVADOR"),
    ("EQUATORIAL_GUINEA_AFRICA_MALABO"),
    ("ERITREA_AFRICA_ASMARA"),
    ("ESTONIA_EUROPE_TALLINN"),
    ("ETHIOPIA_AFRICA_ADDIS_ABABA"),
    ("FALKLAND_ISLANDS_ATLANTIC_STANLEY"),
    ("FAROE_ISLANDS_ATLANTIC_FAROE"),
    ("FIJI_PACIFIC_FIJI"),
    ("FINLAND_EUROPE_HELSINKI"),
    ("FRANCE_EUROPE_PARIS"),
    ("FRENCH_GUIANA_AMERICA_CAYENNE"),
    ("FRENCH_POLYNESIA_PACIFIC_GAMBIER"),
    ("FRENCH_POLYNESIA_PACIFIC_MARQUESAS"),
    ("FRENCH_POLYNESIA_PACIFIC_TAHITI"),
    ("FRENCH_SOUTHERN_TERRITORIES_INDIAN_KERGUELEN"),
    ("GABON_AFRICA_LIBREVILLE"),
    ("GAMBIA_AFRICA_BANJUL"),
    ("GEORGIA_ASIA_TBILISI"),
    ("GERMANY_EUROPE_BERLIN"),
    ("GHANA_AFRICA_ACCRA"),
    ("GIBRALTAR_EUROPE_GIBRALTAR"),
    ("GREECE_EUROPE_ATHENS"),
    ("GREENLAND_AMERICA_DANMARKSHAVN"),
    ("GREENLAND_AMERICA_GODTHAB"),
    ("GREENLAND_AMERICA_SCORESBYSUND"),
    ("GREENLAND_AMERICA_THULE"),
    ("GRENADA_AMERICA_GRENADA"),
    ("GUADELOUPE_AMERICA_GUADELOUPE"),
    ("GUAM_PACIFIC_GUAM"),
    ("GUATEMALA_AMERICA_GUATEMALA"),
    ("GUERNSEY_EUROPE_GUERNSEY"),
    ("GUINEA_BISSAU_AFRICA_BISSAU"),
    ("GUINEA_AFRICA_CONAKRY"),
    ("GUYANA_AMERICA_GUYANA"),
    ("HAITI_AMERICA_PORT_AU_PRINCE"),
    ("HONDURAS_AMERICA_TEGUCIGALPA"),
    ("HONG_KONG_ASIA_HONG_KONG"),
    ("HUNGARY_EUROPE_BUDAPEST"),
    ("ICELAND_ATLANTIC_REYKJAVIK"),
    ("INDIA_ASIA_KOLKATA"),
    ("INDONESIA_ASIA_JAKARTA"),
    ("INDONESIA_ASIA_JAYAPURA"),
    ("INDONESIA_ASIA_MAKASSAR"),
    ("INDONESIA_ASIA_PONTIANAK"),
    ("IRAN_ASIA_TEHRAN"),
    ("IRAQ_ASIA_BAGHDAD"),
    ("IRELAND_EUROPE_DUBLIN"),
    ("ISLE_OF_MAN_EUROPE_ISLE_OF_MAN"),
    ("ISRAEL_ASIA_JERUSALEM"),
    ("ITALY_EUROPE_ROME"),
    ("JAMAICA_AMERICA_JAMAICA"),
    ("JAPAN_ASIA_TOKYO"),
    ("JERSEY_EUROPE_JERSEY"),
    ("JORDAN_ASIA_AMMAN"),
    ("KAZAKHSTAN_ASIA_ALMATY"),
    ("KAZAKHSTAN_ASIA_AQTAU"),
    ("KAZAKHSTAN_ASIA_AQTOBE"),
    ("KAZAKHSTAN_ASIA_ORAL"),
    ("KAZAKHSTAN_ASIA_QYZYLORDA"),
    ("KENYA_AFRICA_NAIROBI"),
    ("KIRIBATI_PACIFIC_ENDERBURY"),
    ("KIRIBATI_PACIFIC_KIRITIMATI"),
    ("KIRIBATI_PACIFIC_TARAWA"),
    ("KOREA_DEMOCRATIC_PEOPLES_REPUBLIC_OF_ASIA_PYONGYANG"),
    ("KOREA_REPUBLIC_OF_ASIA_SEOUL"),
    ("KUWAIT_ASIA_KUWAIT"),
    ("KYRGYZSTAN_ASIA_BISHKEK"),
    ("LAO_PEOPLES_DEMOCRATIC_REPUBLIC_ASIA_VIENTIANE"),
    ("LATVIA_EUROPE_RIGA"),
    ("LEBANON_ASIA_BEIRUT"),
    ("LESOTHO_AFRICA_MASERU"),
    ("LIBERIA_AFRICA_MONROVIA"),
    ("LIBYAN_ARAB_JAMAHIRIYA_AFRICA_TRIPOLI"),
    ("LIECHTENSTEIN_EUROPE_VADUZ"),
    ("LITHUANIA_EUROPE_VILNIUS"),
    ("LUXEMBOURG_EUROPE_LUXEMBOURG"),
    ("MACAO_ASIA_MACAU"),
    ("MACEDONIA_THE_FORMER_YUGOSLAV_REPUBLIC_OF_EUROPE_SKOPJE"),
    ("MADAGASCAR_INDIAN_ANTANANARIVO"),
    ("MALAWI_AFRICA_BLANTYRE"),
    ("MALAYSIA_ASIA_KUALA_LUMPUR"),
    ("MALAYSIA_ASIA_KUCHING"),
    ("MALDIVES_INDIAN_MALDIVES"),
    ("MALI_AFRICA_BAMAKO"),
    ("MALTA_EUROPE_MALTA"),
    ("MARSHALL_ISLANDS_PACIFIC_KWAJALEIN"),
    ("MARSHALL_ISLANDS_PACIFIC_MAJURO"),
    ("MARTINIQUE_AMERICA_MARTINIQUE"),
    ("MAURITANIA_AFRICA_NOUAKCHOTT"),
    ("MAURITIUS_INDIAN_MAURITIUS"),
    ("MAYOTTE_INDIAN_MAYOTTE"),
    ("MEXICO_AMERICA_CANCUN"),
    ("MEXICO_AMERICA_CHIHUAHUA"),
    ("MEXICO_AMERICA_HERMOSILLO"),
    ("MEXICO_AMERICA_MAZATLAN"),
    ("MEXICO_AMERICA_MERIDA"),
    ("MEXICO_AMERICA_MEXICO_CITY"),
    ("MEXICO_AMERICA_MONTERREY"),
    ("MEXICO_AMERICA_TIJUANA"),
    ("MICRONESIA_FEDERATED_STATES_OF_PACIFIC_KOSRAE"),
    ("MICRONESIA_FEDERATED_STATES_OF_PACIFIC_PONAPE"),
    ("MICRONESIA_FEDERATED_STATES_OF_PACIFIC_TRUK"),
    ("MOLDOVA_EUROPE_CHISINAU"),
    ("MONACO_EUROPE_MONACO"),
    ("MONGOLIA_ASIA_CHOIBALSAN"),
    ("MONGOLIA_ASIA_HOVD"),
    ("MONGOLIA_ASIA_ULAANBAATAR"),
    ("MONTENEGRO_EUROPE_PODGORICA"),
    ("MONTSERRAT_AMERICA_MONTSERRAT"),
    ("MOROCCO_AFRICA_CASABLANCA"),
    ("MOZAMBIQUE_AFRICA_MAPUTO"),
    ("MYANMAR_ASIA_RANGOON"),
    ("NAMIBIA_AFRICA_WINDHOEK"),
    ("NAURU_PACIFIC_NAURU"),
    ("NEPAL_ASIA_KATMANDU"),
    ("NETHERLANDS_ANTILLES_AMERICA_CURACAO"),
    ("NETHERLANDS_EUROPE_AMSTERDAM"),
    ("NEW_CALEDONIA_PACIFIC_NOUMEA"),
    ("NEW_ZEALAND_PACIFIC_AUCKLAND"),
    ("NEW_ZEALAND_PACIFIC_CHATHAM"),
    ("NICARAGUA_AMERICA_MANAGUA"),
    ("NIGERIA_AFRICA_LAGOS"),
    ("NIGER_AFRICA_NIAMEY"),
    ("NIUE_PACIFIC_NIUE"),
    ("NORFOLK_ISLAND_PACIFIC_NORFOLK"),
    ("NORTHERN_MARIANA_ISLANDS_PACIFIC_SAIPAN"),
    ("NORWAY_EUROPE_OSLO"),
    ("OCCUPIED_PALESTINIAN_TERRITORY_ASIA_GAZA"),
    ("OMAN_ASIA_MUSCAT"),
    ("PAKISTAN_ASIA_KARACHI"),
    ("PALAU_PACIFIC_PALAU"),
    ("PANAMA_AMERICA_PANAMA"),
    ("PAPUA_NEW_GUINEA_PACIFIC_PORT_MORESBY"),
    ("PARAGUAY_AMERICA_ASUNCION"),
    ("PERU_AMERICA_LIMA"),
    ("PHILIPPINES_ASIA_MANILA"),
    ("PITCAIRN_PACIFIC_PITCAIRN"),
    ("POLAND_EUROPE_WARSAW"),
    ("PORTUGAL_ATLANTIC_AZORES"),
    ("PORTUGAL_ATLANTIC_MADEIRA"),
    ("PORTUGAL_EUROPE_LISBON"),
    ("PUERTO_RICO_AMERICA_PUERTO_RICO"),
    ("QATAR_ASIA_QATAR"),
    ("REUNION_INDIAN_REUNION"),
    ("ROMANIA_EUROPE_BUCHAREST"),
    ("RUSSIAN_FEDERATION_ASIA_ANADYR"),
    ("RUSSIAN_FEDERATION_ASIA_IRKUTSK"),
    ("RUSSIAN_FEDERATION_ASIA_KAMCHATKA"),
    ("RUSSIAN_FEDERATION_ASIA_KRASNOYARSK"),
    ("RUSSIAN_FEDERATION_ASIA_MAGADAN"),
    ("RUSSIAN_FEDERATION_ASIA_NOVOSIBIRSK"),
    ("RUSSIAN_FEDERATION_ASIA_OMSK"),
    ("RUSSIAN_FEDERATION_ASIA_SAKHALIN"),
    ("RUSSIAN_FEDERATION_ASIA_VLADIVOSTOK"),
    ("RUSSIAN_FEDERATION_ASIA_YAKUTSK"),
    ("RUSSIAN_FEDERATION_ASIA_YEKATERINBURG"),
    ("RUSSIAN_FEDERATION_EUROPE_KALININGRAD"),
    ("RUSSIAN_FEDERATION_EUROPE_MOSCOW"),
    ("RUSSIAN_FEDERATION_EUROPE_SAMARA"),
    ("RUSSIAN_FEDERATION_EUROPE_VOLGOGRAD"),
    ("RWANDA_AFRICA_KIGALI"),
    ("SAINT_BARTHELEMY_AMERICA_ST_BARTHELEMY"),
    ("SAINT_KITTS_AND_NEVIS_AMERICA_ST_KITTS"),
    ("SAINT_LUCIA_AMERICA_ST_LUCIA"),
    ("SAINT_MARTIN_FRENCH_PART_AMERICA_MARIGOT"),
    ("SAINT_VINCENT_AND_THE_GRENADINES_AMERICA_ST_VINCENT"),
    ("SAMOA_PACIFIC_APIA"),
    ("SAN_MARINO_EUROPE_SAN_MARINO"),
    ("SAO_TOME_AND_PRINCIPE_AFRICA_SAO_TOME"),
    ("SAUDI_ARABIA_ASIA_RIYADH"),
    ("SENEGAL_AFRICA_DAKAR"),
    ("SERBIA_EUROPE_BELGRADE"),
    ("SEYCHELLES_INDIAN_MAHE"),
    ("SIERRA_LEONE_AFRICA_FREETOWN"),
    ("SINGAPORE_ASIA_SINGAPORE"),
    ("SLOVAKIA_EUROPE_BRATISLAVA"),
    ("SLOVENIA_EUROPE_LJUBLJANA"),
    ("SOLOMON_ISLANDS_PACIFIC_GUADALCANAL"),
    ("SOMALIA_AFRICA_MOGADISHU"),
    ("SOUTH_AFRICA_AFRICA_JOHANNESBURG"),
    ("SOUTH_GEORGIA_AND_THE_SOUTH_SANDWICH_ISLANDS_ATLANTIC_SOUTH_GEORGIA"),
    ("SPAIN_AFRICA_CEUTA"),
    ("SPAIN_ATLANTIC_CANARY"),
    ("SPAIN_EUROPE_MADRID"),
    ("SRI_LANKA_ASIA_COLOMBO"),
    ("ST_HELENA_ATLANTIC_ST_HELENA"),
    ("ST_PIERRE_AND_MIQUELON_AMERICA_MIQUELON"),
    ("SUDAN_AFRICA_KHARTOUM"),
    ("SURINAME_AMERICA_PARAMARIBO"),
    ("SVALBARD_AND_JAN_MAYEN_ISLANDS_ARCTIC_LONGYEARBYEN"),
    ("SWAZILAND_AFRICA_MBABANE"),
    ("SWEDEN_EUROPE_STOCKHOLM"),
    ("SWITZERLAND_EUROPE_ZURICH"),
    ("SYRIAN_ARAB_REPUBLIC_ASIA_DAMASCUS"),
    ("TAIWAN_ASIA_TAIPEI"),
    ("TAJIKISTAN_ASIA_DUSHANBE"),
    ("TANZANIA_AFRICA_DAR_ES_SALAAM"),
    ("THAILAND_ASIA_BANGKOK"),
    ("TIMOR_LESTE_ASIA_DILI"),
    ("TOGO_AFRICA_LOME"),
    ("TOKELAU_PACIFIC_FAKAOFO"),
    ("TONGA_PACIFIC_TONGATAPU"),
    ("TRINIDAD_AND_TOBAGO_AMERICA_PORT_OF_SPAIN"),
    ("TUNISIA_AFRICA_TUNIS"),
    ("TURKEY_EUROPE_ISTANBUL"),
    ("TURKMENISTAN_ASIA_ASHGABAT"),
    ("TURKS_AND_CAICOS_ISLANDS_AMERICA_GRAND_TURK"),
    ("TUVALU_PACIFIC_FUNAFUTI"),
    ("UGANDA_AFRICA_KAMPALA"),
    ("UKRAINE_EUROPE_KIEV"),
    ("UKRAINE_EUROPE_SIMFEROPOL"),
    ("UKRAINE_EUROPE_UZHGOROD"),
    ("UKRAINE_EUROPE_ZAPOROZHYE"),
    ("UNITED_ARAB_EMIRATES_ASIA_DUBAI"),
    ("UNITED_KINGDOM_EUROPE_LONDON"),
    ("UNITED_STATES_MINOR_OUTLYING_ISLANDS_PACIFIC_JOHNSTON"),
    ("UNITED_STATES_MINOR_OUTLYING_ISLANDS_PACIFIC_MIDWAY"),
    ("UNITED_STATES_MINOR_OUTLYING_ISLANDS_PACIFIC_WAKE"),
    ("UNITED_STATES_AMERICA_ADAK"),
    ("UNITED_STATES_AMERICA_ANCHORAGE"),
    ("UNITED_STATES_AMERICA_BOISE"),
    ("UNITED_STATES_AMERICA_CHICAGO"),
    ("UNITED_STATES_AMERICA_DENVER"),
    ("UNITED_STATES_AMERICA_DETROIT"),
    ("UNITED_STATES_AMERICA_INDIANA_INDIANAPOLIS"),
    ("UNITED_STATES_AMERICA_INDIANA_KNOX"),
    ("UNITED_STATES_AMERICA_INDIANA_MARENGO"),
    ("UNITED_STATES_AMERICA_INDIANA_PETERSBURG"),
    ("UNITED_STATES_AMERICA_INDIANA_TELL_CITY"),
    ("UNITED_STATES_AMERICA_INDIANA_VEVAY"),
    ("UNITED_STATES_AMERICA_INDIANA_VINCENNES"),
    ("UNITED_STATES_AMERICA_INDIANA_WINAMAC"),
    ("UNITED_STATES_AMERICA_JUNEAU"),
    ("UNITED_STATES_AMERICA_KENTUCKY_LOUISVILLE"),
    ("UNITED_STATES_AMERICA_KENTUCKY_MONTICELLO"),
    ("UNITED_STATES_AMERICA_LOS_ANGELES"),
    ("UNITED_STATES_AMERICA_MENOMINEE"),
    ("UNITED_STATES_AMERICA_NEW_YORK"),
    ("UNITED_STATES_AMERICA_NOME"),
    ("UNITED_STATES_AMERICA_NORTH_DAKOTA_CENTER"),
    ("UNITED_STATES_AMERICA_NORTH_DAKOTA_NEW_SALEM"),
    ("UNITED_STATES_AMERICA_PHOENIX"),
    ("UNITED_STATES_AMERICA_SHIPROCK"),
    ("UNITED_STATES_AMERICA_YAKUTAT"),
    ("UNITED_STATES_PACIFIC_HONOLULU"),
    ("URUGUAY_AMERICA_MONTEVIDEO"),
    ("UZBEKISTAN_ASIA_SAMARKAND"),
    ("UZBEKISTAN_ASIA_TASHKENT"),
    ("VANUATU_PACIFIC_EFATE"),
    ("VATICAN_CITY_STATE_EUROPE_VATICAN"),
    ("VENEZUELA_AMERICA_CARACAS"),
    ("VIET_NAM_ASIA_SAIGON"),
    ("VIRGIN_ISLANDS_BRITISH_AMERICA_TORTOLA"),
    ("VIRGIN_ISLANDS_US_AMERICA_ST_THOMAS"),
    ("WALLIS_AND_FUTUNA_ISLANDS_PACIFIC_WALLIS"),
    ("WESTERN_SAHARA_AFRICA_EL_AAIUN"),
    ("YEMEN_ASIA_ADEN"),
    ("ZAMBIA_AFRICA_LUSAKA"),
    ("ZIMBABWE_AFRICA_HARARE")
    ]

    return country, tz
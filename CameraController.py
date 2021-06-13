from flask import Flask , flash, render_template, request, session, url_for, redirect
import config_scripts as configs
import os
import math 

UPLOAD_FOLDER = '/opt/web/cameraControler/static/images'
ALLOWED_EXTENSIONS = {'jpeg','png','jpg'}
app = Flask(__name__)
app.config['SECRET_KEY']='oipf hf8-a0s9ywe9129=ssad[[002]]'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home(english=True):
    try:
        with open("lang","r") as f:
            buff=f.read()
        english = (buff=="True")
    except:
        with open("lang","w") as f:
            f.write("True")
            
    current=configs.get_current_network()
    isInternet=configs.check_internet()
    signalStrength=configs.get_connectivity_quality()
    resolution=configs.get_resolution()
    pCount=configs.get_photo_rec_num()
    dropbox=configs.get_user_cred()
    text=configs.get_text()
    personal_one=configs.get_network(1)
    personal_def=configs.get_network(0)
    personal_two=configs.get_network(2)
    
    return render_template('user.html',language=english,cUser=current[0],cPass=current[1],isInternet=isInternet, signalStrength=signalStrength,resolution=resolution, pCount=pCount,eUser=dropbox[0],ePass=dropbox[1],text=text,personal_oneU=personal_one[0],personal_oneP=personal_one[1],personal_twoU=personal_two[0],personal_twoP=personal_two[1], personal_defU=personal_def[0],personal_defP=personal_def[1])
    
@app.route('/admin5836')
def admin():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        apiKey=configs.get_api()
        current=configs.get_current_network()
        isInternet=configs.check_internet()
        signalStrength=configs.get_connectivity_quality()
        pCount=configs.get_photo_rec_num()
        dropbox=configs.get_user_cred()
        text=configs.get_text()
    return render_template('admin.html',apiKey=apiKey,cUser=current[0],cPass=current[1],isInternet=isInternet,signalStrength=signalStrength,pCount=pCount,eUser=dropbox[0],ePass=dropbox[1],text=text)

@app.route('/reboot')
def reboot():
    return render_template('reboot.html')


@app.route('/',methods=['POST'])
def handleUser():
    if request.method=='POST':
        if 'engleza' in request.form:
            with open("lang","w") as f:
                f.write("True")
        if 'romana' in request.form:
            with open("lang","w") as f:
                f.write("False")
        if 'resolutions' in request.form:
            configs.set_resolution(request.form['resolution'])
        if 'wifi1' in request.form:
            configs.change_network(request.form['username'],request.form['password'],1)
        if 'wifi2' in request.form:
            configs.change_network(request.form['username'],request.form['password'],2)
        if 'Reboot' in request.form:
            configs.reboot_system()       
            return redirect(url_for("reboot"))

        return redirect(url_for("home"))
@app.route('/admin5836' ,methods=['POST'])
def handleAdmin():
    
    if request.method=='POST':
        if 'background' in request.form:
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(url_for("admin"))
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(url_for("admin"))
            if file:
                filename = "background.jpeg"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        if 'logo' in request.form:
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(url_for("admin"))
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(url_for("admin"))
            if file:
                filename = "logo.jpeg"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
        if 'ApiForm' in request.form:
            configs.set_api(request.form['newApi'])
        if 'resetPicture' in request.form:
            configs.reset_photo_rec_num()
        if 'wifi5' in request.form:
            configs.change_network(request.form['username'],request.form['password'],0)
        if 'wifi3' in request.form:
            configs.change_network(request.form['username'],request.form['password'],1)
        if 'wifi4' in request.form:
            configs.change_network(request.form['username'],request.form['password'],2)
        if 'cameraEmail' in request.form:
            configs.set_user_cred(request.form['username'].replace(" ",""),request.form['password'].replace(" ",""))
        if 'text1' in request.form:
            configs.set_text(request.form['text'],0)
        if 'text2' in request.form:
            configs.set_text(request.form['text'],1)
        if 'text3' in request.form:
            configs.set_text(request.form['text'],2)
        if 'text4' in request.form:
            configs.set_text(request.form['text'],3)
        if 'text5' in request.form:
            configs.set_text(request.form['text'],4)
        if 'text6' in request.form:
            configs.set_text(request.form['text'],5)
        if 'text7' in request.form:
            configs.set_text(request.form['text'],6)
        if 'text8' in request.form:
            configs.set_text(request.form['text'],7)
        if 'text9' in request.form:
            configs.set_text(request.form['text'],8)
        if 'text10' in request.form:
            configs.set_text(request.form['text'],9)
        if 'text11' in request.form:
            configs.set_text(request.form['text'],10)
        if 'text12' in request.form:
            configs.set_text(request.form['text'],11)
        if 'Reboot' in request.form:
            configs.reboot_system()   
            return redirect(url_for("reboot"))
    return redirect(url_for("admin"))

@app.route('/login', methods=['POST'])
def do_admin_login():
    if configs.check_admin_cred(request.form['username'],request.form['password']):
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return redirect(url_for("admin"))

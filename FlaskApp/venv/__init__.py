import os
from flask import render_template,request, session, g, redirect
from flask import url_for
from flask import Flask
from flask.ext.mail import Mail, Message
from flask_oauth import OAuth
from werkzeug import secure_filename


UPLOAD_FOLDER = 'FlaskApp/static/upload/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mail = Mail(app)
DEBUG = True
FACEBOOK_APP_ID  = '613776818694665'
FACEBOOK_APP_SECRET = 'd3946f7049d8d3903b2e296412c79e20'


app.secret_key = 'A0Zr98j/3yX R~XHHd12jm2]LW1/,?RT'

@app.route('/')
@app.route('/index')
def index():
    data=popular()
    header=render_template("header.html")
    center=render_template("inicio.html",data=data)
    footer=render_template("footer.html")
    #scripts=render_template("scripts.html",menus = menus)
    #data="hola bruno"
    return header+center+footer

@app.route('/inicio2')
@app.route('/personaje/<nickname>')
def personaje(nickname=0):
    nickname=nickname.replace("-"," ")
    print nickname
    data=info_nickname(nickname)   
    header=render_template("header.html")
    center=render_template("inicio2.html",data=data)
    footer=render_template("footer.html")
    try :
        print session['me'] 
    except :
        print "holi"
    return header+center+footer


def popular():
    import psycopg2
    sql="select nombre,apellido,sobrenombre from farandula_aprobado limit 5" 
    conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" %("prosycontras", "prosycontras", "localhost","valeroth"))
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    return rows


def peticion_famoso(nombre,apellido,sobrenombre,categoria):
    import psycopg2
    sql="INSERT INTO farandula_peticion (nombre,apellido,sobrenombre,id_categoria,id_usuario) values ('%s','%s','%s','%s','%i') returning id"%(nombre,apellido,sobrenombre,categoria,session['me'])
    conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" %("prosycontras", "prosycontras", "localhost","valeroth"))
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    id_of_new_row = cur.fetchone()[0]
    return str(id_of_new_row)+"_peticion.jpg"

def ingresar_comentario(text,idf,estado):
    import psycopg2
    idf = int(idf)
    print idf
    sql="insert into comentarios (estado ,id_farandula,id_usuario,text) values('%i','%i','%i','%s')"%(estado,idf,session['me'],text)
    print sql
    conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" %("prosycontras", "prosycontras", "localhost","valeroth"))
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return "w0rk"

@app.route('/pro', methods=['GET', 'POST'])
def pro():
    try :

        a=ingresar_comentario(request.form['text'],request.form['id'],1)
        return a
    
    except :
        return "404"


@app.route('/contra', methods=['GET', 'POST'])
def contra():
    try :

        a=ingresar_comentario(request.form['text'],request.form['id'],2)
        return a
    
    except :
        return "404"



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload_famoso', methods=['GET', 'POST'])
def upload_file():
    try :
        file = request.files['imagen']
        if file and allowed_file(file.filename) and session['me']:   

            filename = peticion_famoso(request.form['nombre'],request.form['apellido'],request.form['sobrenombre'],request.form['categoria'])
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "Work"
    
    except :
        return "404"


def info_nickname(nickname):
    import psycopg2

    sql="select nombre,apellido,sobrenombre,twitter,id from farandula_aprobado where sobrenombre='%s'"%(nickname)
    conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" %("prosycontras", "prosycontras", "localhost","valeroth"))
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchone()



def user():
    import psycopg2
    fb_account = facebook.get('/me?fields=picture,link,name,id,first_name,last_name,email')
    id_fb = fb_account.data['id']
    print id_fb
    sql="select id from usuario where uid='%s'"%(id_fb)
    conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" %("prosycontras", "prosycontras", "localhost","valeroth"))
    cur = conn.cursor()
    cur.execute(sql)
    tupla = cur.fetchone()
    if tupla==None:
        sql="INSERT into usuario(uid,nombre,apellido,mail) values('%s','%s','%s','%s') returning id"%(id_fb,fb_account.data['first_name'],fb_account.data['last_name'],fb_account.data['email'])
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        session['me'] = cur.fetchone()[0]
    else :
        session['me']= tupla[0]


oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': ('email, ')}
)

@facebook.tokengetter
def get_facebook_token():
    
    return session.get('facebook_token')

def pop_login_session():
    session.pop('logged_in', None)
    session.pop('facebook_token', None)
    session.pop('me', None)


@app.route("/facebook_login")
def facebook_login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next'), _external=True))

@app.route("/facebook_authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)
    session['logged_in'] = True
    session['facebook_token'] = (resp['access_token'], '')
    user()
    return redirect(next_url)

@app.route("/logout")
def logout():
    pop_login_session()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

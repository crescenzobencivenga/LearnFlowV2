# Per far partire un file flask,
#   1) immettersi nella shell
#   2) posizionarsi nella cartella ove situato il file con import FLASK
#   3) immettere il comando flask run -h 0.0.0.0 -p 5000
#       a) questo comando fa partire flask sulla porta 5000
#       b) ed accetta ogni connessione che parte sulla macchina
#   4) apparirà un link, cliccateci sopra, verrete redirezionati
#   5) CTRL+C per chiudere flask
import json

import pymongo
from bson import json_util
from flask import Flask, jsonify, request, render_template, session, redirect, url_for
from flask_cors import CORS
import bcrypt

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
CORS(app)

client = pymongo.MongoClient(
    "mongodb+srv://USER:PASSWORD@cluster.p0jl4.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.get_database('LearnFlow_mongoDB')
login_collection = db['LF_login']
user_info = db['LF_user_info']


# base
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_user = login_collection.find_one({'mail': request.form['mail']})
        if login_user:
            # controllo coincidenza password (se c'è questo utente)
            if bcrypt.checkpw(
                    request.form['password'].encode('utf-8'),
                    login_user['password']
            ):
                # -------> se tutto ok
                uname = login_user['username']
                item = user_info.find_one({'username': uname})
                # item['_id'] = str(item['_id'])  # da ObjectId a string.
                session['username'] = item['username']
                session['pnt'] = item['pnt']
                session['lvl'] = item['lvl']
                return redirect(url_for("MainGame"))
            else:
                # -------> se si hanno problemi di autenticazione 2
                return render_template("login.html", message="Username or password does't match")
        else:
            # -------> se si hanno problemi di autenticazione 1
            return render_template("login.html", message="Username or password does't match")
    else:
        if "username" in session and "pnt" in session and "lvl" in session:
            return redirect(url_for("MainGame"))
    return render_template("login.html")


@app.route('/MainGame/')
def MainGame():
    if "username" in session and "pnt" in session and "lvl" in session:
        return render_template('MainGame.html', username=session['username'], lvl=session['lvl'], pnt=session['pnt'])
    else:
        return redirect(url_for("login"))


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('lvl', None)
    session.pop('pnt', None)
    return redirect(url_for("login"))


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        if request.form['password'] != request.form['pass_conf']:
            return render_template('registration.html', message="passwords do not match")
        existing_user = login_collection.find_one({'username': request.form['username']})
        existing_mail = login_collection.find_one({'mail': request.form['mail']})
        # se l'utente già esiste -> ritorna null, altrimeni lo crea inserendo i campi
        if existing_user is None or existing_mail is None:
            # si crea un record nel campo identificazione
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            login_collection.insert_one(
                {
                    'username': request.form['username'],
                    'mail': request.form['mail'],
                    'password': hashpass
                }
            )
            # si crea un record nel campo dati (di gioco)
            user_info.insert_one(
                {
                    'username': request.form['username'],
                    'lvl': '0',
                    'pnt': '0'
                }
            )
            return redirect(url_for('login'))
        else:
            return render_template('registration.html', message="username or email has already been used")
    else:
        return render_template('registration.html')


@app.route('/update_data/<username>/<lvl>/<pnt>', methods=['POST'])
def update_data(username, lvl, pnt):
    myquery = {'username': username}
    newvalues = {"$set":
        {
            "username": username,
            "lvl": lvl,
            "pnt": pnt,
        }
    }
    user_info.update_one(myquery, newvalues)
    item = user_info.find_one({'username': username})
    item['_id'] = str(item['_id'])  # da ObjectId a string.
    return jsonify({'user_data': item})


@app.route('/get_data', methods=['POST'])
def get_data_user():
    item = user_info.find_one({'username': request.form['username']})
    item['_id'] = str(item['_id'])  # da ObjectId a string.
    return jsonify({'user_data': item})


@app.route('/get_top', methods=['GET'])
def get_top():
    item = user_info.find().sort("pnt", -1).limit(15)
    i = 0
    x = {i: {'n_item': str(item.count())}}
    for doc in item:
        i = i + 1
        x[i] = {'username': doc['username'], 'pnt': doc['pnt']}
    return json.dumps(x)



@app.route('/exercise_flow_chart/<pt>', methods=['GET'])
def exercise_flow_chart(pt):
    with open("./static/json/es2.json") as file:
        data = json.load(file)
    datax = json.dumps(data, indent=4)
    print(datax)
    if "username" not in session and "pnt" not in session:
        return redirect(url_for("login"))
    else:
        return render_template('Esercizi_flowchart.html', data=data, ex=pt, username=session['username'], pnt=session['pnt'])


@app.route('/eserciziRispostaMultipla/<pt>', methods=['GET'])
def eserciziRispostaMultipla(pt):
    with open("./static/json/esRispostaMultipla.json") as file:
        data = json.load(file)
    datax = json.dumps(data, indent=4)
    print(datax)
    if "username" not in session and "pnt" not in session:
        return redirect(url_for("login"))
    else:
        return render_template('eserciziRispostaMultipla.html', data=data, ex=pt, username=session['username'], pnt=session['pnt'])

# @app.route('/get_json_ex', methods=['GET'])
# def get_json_ex():
#     with open("./static/json/es2.json") as file:
#         data = json.load(file)
#     print(json.dumps(data, indent=4))
#     return json.dumps(data, indent=4)


if __name__ == '__main__':
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.run(debug=True)

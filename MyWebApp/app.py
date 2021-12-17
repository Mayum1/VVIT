import requests
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="123456",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()


@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')


@app.route('/login/', methods=['POST'])
def login():
    if request.form.get("login"):
        username = request.form.get('username')
        password = request.form.get('password')
        if username == '' and password != '':
            error = 1

            return render_template('login.html', error=error)
        elif password == '' and username != '':
            error = 2

            return render_template('login.html', error=error)
        elif username == '' and password == '':
            error = 3

            return render_template('login.html', error=error)
        else:
            try:
                cursor.execute('SELECT * FROM service.users WHERE login=%s AND password=%s', (str(username), str(password)))
                records = list(cursor.fetchall())

                return render_template('account.html', full_name=records[0][1], login=records[0][2], password=records[0][3])
            except:
                error = 4

                return render_template('login.html', error=error)

    elif request.form.get("registration"):
        return redirect('/registration/')
        return render_template('registration.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        cursor.execute('SELECT * FROM service.users WHERE login = %s', [str(login)])
        records = list(cursor.fetchall())

        if (name == '' or login == '' or password == '') and login not in records:
            error = 1
            return render_template('registration.html', error=error)
        elif records:
            error = 2
            return render_template('registration.html', error=error)
        else:
            cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);', (str(name), str(login), str(password)))
            conn.commit()

            return redirect('/login/')

    return render_template('registration.html')

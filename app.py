from flask import Flask, render_template, request, redirect, make_response
import sqlite3
import time
import DB

app = Flask(__name__, static_folder='css')

@app.route('/')
@app.route('/login/')
def login():
    print('login')
    return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login_post():

    error = None
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']
        res = DB.login(email, password)
        if res:
            resp = make_response(redirect('/serviços/'))
            resp.set_cookie('email',email)
            return resp
        else:
            error = '*Utilizador ou password incorretos*'
            
    return render_template('login.html', error=error)

            # <div id="info_section">
            #     <p style="color: red;">{{error}}</p>
            # </div>
            #colocar isto no html


@app.route('/regist/')
def regist():
    return render_template('regist.html')

@app.route('/regist/', methods=['GET', 'POST'])
def regist_post():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        tel = request.form['tel']
        date = request.form['date']
        if DB.add_user(email, password, tel, date):
            return redirect('/login/')
        else:
            error = 'Utilizador ja existe'
    return render_template('regist.html', error=error)

@app.route('/serviços/')
def serviços():
    return render_template('serviços.html')

@app.route('/escolhas/')
def escolhas():
    return render_template('escolhas.html')

@app.route('/escolhas/', methods=['GET', 'POST'])
def escolhas_post():
    
    error = None
    if request.method == 'POST':
        option1 = request.form['option1']
        option2 = request.form['option2']
        if (option1 == '1' and option2 == '2') or (option1 == '2' and option2 == '2'):
            resp = make_response(redirect('/assistentes/'))
            resp.set_cookie('option','0')
            return resp
        else:
            resp = make_response(redirect('/assistentes/'))
            resp.set_cookie('option','1')
            return resp

    return render_template('escolhas.html', error=error)


@app.route('/assistentes/')
def assistentes():
    return render_template('assistentes.html')

@app.route('/check/')
def check():
    time.sleep(1)
    if request.cookies.get('option') == '0':
        return redirect('/catalogo/')
    else:
        return redirect('/pagamento/')

@app.route('/catalogo/')
def catalogo():
    return render_template('catalogo.html')

@app.route('/pagamento/')
def pagamento():
    return render_template('pagamento.html')

@app.route('/pagamento/', methods=['GET', 'POST']) # type: ignore
def pagamento_post():
    if request.method == 'POST':
        option = request.form['option1']
        if option == 'mb':
            return redirect('/login/') #redirecionar pra pagina mbway
        elif option == 'mt':
            return redirect('/login/') #redirecionar pra pagina multibanco
        elif option == 'pp':
            return redirect('/login/') #redirecionar pra pagina paypal
        else:
            return redirect('/login/') #redirecionar pra pagina cartao de credito


if __name__ == '__main__':
    app.run(debug=True)
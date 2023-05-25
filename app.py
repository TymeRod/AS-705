import time
from flask import Flask, render_template, request, redirect, make_response
import hashlib
import datetime
import DB


app = Flask(__name__, static_folder='css')

@app.route('/', methods=['POST', 'GET'])
def inicio():
    return render_template('index.html')

@app.route('/index/')
def index():
    return redirect('/')



@app.route('/login', methods=['POST', 'GET'])
def login():
    email = request.form.get('username')
    password = request.form.get('password')
    if password is not None:
        user = DB.get_user_by_email(email)
        if user and user[1] == hashlib.sha256(password.encode()).hexdigest():
            DB.login(email, hashlib.sha256(password.encode()).hexdigest())
            resp = make_response(redirect('/serviços'))
            resp.set_cookie('email', str(email))
            return resp

    error = 'Invalid username or password'
    return render_template('login.html', error=error)



@app.route('/regist/', methods=['POST', 'GET'])
def regist():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        conf_pass = request.form.get('conf')
        tel = request.form.get('tel')
        date_str = request.form.get('date')

            
        if password is not None and email is not None and tel is not None and date_str is not None:
            if password == conf_pass:
                date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

                if DB.add_user(email, hashlib.sha256(password.encode()).hexdigest(), tel, date):

                    return redirect('/login')
            else:
                error = 'Passwords do not match'
                return render_template('regist.html', error=error)

        error = 'User already exists'
    return render_template('regist.html', error=error)

@app.route('/logout')
def logout():

    resp = make_response(redirect('/login'))
    resp.delete_cookie('email')
    return resp

@app.route('/serviços/')
def serviços():
    return render_template('serviços.html')



@app.route('/escolhas/', methods=['GET', 'POST'])
def escolhas():
    error = None
    if request.method == 'POST':
        option1 = request.form.get('option1')
        option2 = request.form.get('option2')
        if option1 is not None and option2 is not None and ((option1 == '1' and option2 == '2') or (option1 == '2' and option2 == '2')):
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



@app.route('/pagamento/', methods=['GET', 'POST'])
def pagamento():
    if request.method == 'POST':
        option = request.form.get('option1')
        if option == 'mb':
            return redirect('/mbway/')
        elif option == 'mt':
            return redirect('/multibanco/')
        elif option == 'pp':
            return redirect('/paypal/')
        elif option == 'cc':
            return redirect('/credit-card/')
    return render_template('pagamento.html')

if __name__ == '__main__':
    app.run(debug=True)
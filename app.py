from flask import *
import time

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
        if request.form['username'] != 'admin' or \
            request.form['password'] != 'admin':
            error = 'Invalid credentials'
        else:
            return serviços()
    return render_template('login.html', error=error)


@app.route('/regist/')
def regist():
    return render_template('regist.html')

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


if __name__ == '__main__':
    app.run(debug=True)
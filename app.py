from flask import Flask, render_template, request

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

if __name__ == '__main__':
    app.run(debug=True)
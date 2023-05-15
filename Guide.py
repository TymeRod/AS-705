from flask import Flask, render_template

app = Flask(__name__, static_folder='css')

@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')

@app.route('/regist/')
def regist():
    return render_template('regist.html')

@app.route('/serviços/')
def serviços():
    return render_template('serviços.html')

if __name__ == '__main__':
    app.run(debug=True)
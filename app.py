import time
from flask import Flask, render_template, request, redirect, make_response, jsonify
import hashlib
import datetime
import DB
from PIL import Image, ImageDraw, ImageFont
import json


app = Flask(__name__, static_folder='css')


tintaAcril = 13.49
ta = 0
tinta = 11.99
t = 0
pincel = 5.49
p = 0
rolo = 7.99
r = 0
tintaExtInt = 25.89
tei = 0

compra = dict()
preço = {'Tinta acrílica mate 5L': tintaAcril, 
         'Tinta mate exterior BRANCO 4L': tinta,
         'Pincel  UNIVERSAL PP 60MM': pincel, 
         'Rolo Antigota Poliamida': rolo,
         'Tinta anti-mofo 5 L, branco': tintaExtInt}

def get_service_json(service):
    if service == 'pintura':
        data = {'service': 'pintura',
                 'description': 'Serviço de pintura de interiores e exteriores'}
        
    elif service == 'limpeza':
        data = {'service': 'limpeza',
                 'description': 'Serviço de limpeza de casas e escritórios'}
        
    elif service == 'eletricidade':
        data = {'service': 'eletricidade',
                 'description': 'Serviço de instalação e reparação elétrica'}
        
    elif service == 'Canalização':
        data = {'service': 'Canalização',
                 'description': 'Serviço de instalação e reparação de canalizações'}
        
    elif service == 'Carpintaria':
        data = {'service': 'Carpintaria',
                 'description': 'Serviço de carpintaria e marcenaria'}
        
    elif service == 'serralheria':
        data = {'service': 'serralheria',
                 'description': 'Serviço de serralharia e metalurgia'}
        
    elif service == 'Jardinagem':
        data = {'service': 'Jardinagem',
                 'description': 'Serviço de jardinagem e paisagismo'}
        
    elif service == 'Assistência':
        data = {'service': 'Assistência',
                 'description': 'Serviço de assistência técnica em geral'}
    else:
        data = {'error': 'Invalid service'}

    with open('service.json', 'w') as f:
        json.dump(data, f)

    return 'service.json'



def draw():
    num = 0
    # Open the image
    image = Image.open('./css/images/carrinho.png')

    # Create a drawing object
    draw = ImageDraw.Draw(image)

    # Define the circle parameters
    x, y = 92, 77
    radius = 25

    # Draw the circle
    draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill='red')

    font = ImageFont.truetype('Arial.ttf', size=25)

    # Draw the number inside the circle

    for i in compra:
        for j in range(compra[i]):
            num += 1

    number = num
    text_width, text_height = draw.textsize(str(number), font=font)
    draw.text((x-text_width/2, y-text_height/2), str(number), fill='white',font=font)

    # Save the modified image
    image.save('./css/images/carrinho1.png')


@app.route('/', methods=['POST', 'GET'])
def inicio1():
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
            resp = make_response(redirect('/servicos'))
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

@app.route('/serviços/', methods=['POST', 'GET'])
def serviços():
    return render_template('serviços.html')

@app.route('/servicos_post', methods=['POST', 'GET'])
def servicos_post():

    if request.method == 'POST':
        print("AAAAAAAAAAAA")
        if 'pintura' in request.form:
            get_service_json('pintura')
            return redirect('/escolhas/')
        
        if 'limpeza' in request.form:
            get_service_json('limpeza')
            return redirect('/escolhas/')
        
        if 'eletricidade' in request.form:
            get_service_json('eletricidade')  
            return redirect('/escolhas/')
        
        if 'Canalização' in request.form:
            get_service_json('Canalização')
            return redirect('/escolhas/')
        
        if 'Carpintaria' in request.form:
            get_service_json('Carpintaria')
            return redirect('/escolhas/')
        
        if 'serralheria' in request.form:
            get_service_json('serralheria')
            return redirect('/escolhas/')
        
        if 'Jardinagem' in request.form:
            get_service_json('Jardinagem')
            return redirect('/escolhas/')
        
        if 'Assistência' in request.form:
            get_service_json('Assistência')
            return redirect('/escolhas/')
            
    return redirect('/servicos/')

@app.route('/inicio/')
def inicio():
    return redirect('/')


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

@app.route('/catalogo/', methods=['GET', 'POST'])
def catalogo():
    return render_template('catalogo.html', tintaAcril=tintaAcril, 
                           tinta = tinta, pincel = pincel, 
                           rolo = rolo, tintaExtInt = tintaExtInt)

@app.route('/catalogo_post', methods=['POST', 'GET'])
def catalogo_post():
    print("AAAAAAAAAAAAAAAAAA")
    draw()
    if request.method == 'POST':
        print("AAAAAAAAAAAAAA")
        print(request.form)
        if 'carrinho' in request.form:
            return redirect('/pagamento/')

        if 'tintaAcril' in request.form:
            global ta
            ta = ta + 1
            compra['Tinta acrílica mate 5L'] = int(ta)
            draw()
            
        if 'tinta' in request.form:
            global t
            t = t + 1
            compra['Tinta mate exterior BRANCO 4L'] = int(t)
            draw()

        if 'pincel' in request.form:
            global p
            p = p + 1
            compra['Pincel  UNIVERSAL PP 60MM'] = int(p)
            draw()

        if 'rolo' in request.form:
            global r
            r = r + 1
            compra['Rolo Antigota Poliamida'] = int(r)
            draw()

        if 'tintaExtInt' in request.form:
            global tei
            tei = tei + 1
            compra['Tinta anti-mofo 5 L, branco'] = int(tei)
            draw()
            
    return redirect('/catalogo/')
    

@app.route('/pagamento/', methods=['GET', 'POST'])
def pagamento():

    conta = 0
    prod = []
    for i in compra:
        conta += preço[i]*compra[i]

    for i in compra:
        for j in range(int(compra[i])):
            prod.append(i)

    print(prod)

    return render_template('pagamento.html', conta=conta, prod = prod)


@app.route('/account/', methods=['GET', 'POST'])
def account():
    return render_template('account.html')

@app.route('/sobre/')
def sobre():
    return render_template('sobre.html')

@app.route('/cenas/', methods=['GET', 'POST'])
def cenas():
    a = 'ola'
    b = 'teste'
    return render_template('cenas.html', a=a, b=b)



if __name__ == '__main__':
    app.run(debug=True)
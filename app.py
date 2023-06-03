import time
from flask import Flask, render_template, request, redirect, make_response, jsonify
import hashlib
import datetime
import DB
from PIL import Image, ImageDraw, ImageFont
import json


app = Flask(__name__, static_folder='css')


compra = dict()
preço = dict()

with open('items.json', 'r') as f:
    data = json.load(f)

items = data['items']

for item in items:
    compra[item['name']] = 0
    preço[item['name']] = item['price']


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
            resp = make_response(redirect('/serviços'))
            resp.set_cookie('email', str(email))
            return resp

    # Check if user is already logged in
    email_cookie = request.cookies.get('email')
    if email_cookie is not None:
        return redirect('/serviços')

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
        address = request.form.get('address')

            
        if password is not None and email is not None and tel is not None and date_str is not None:
            if password == conf_pass:
                date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

                if DB.add_user(email, hashlib.sha256(password.encode()).hexdigest(), tel, date, address):

                    return redirect('/login')
            else:
                error = 'Passwords do not match'
                return render_template('regist.html', error=error)

        error = 'User already exists'
    return render_template('regist.html', error=error)

@app.route('/logout')
def logout():
    resp = make_response(redirect('/index'))
    resp.delete_cookie('email')
    return resp

@app.route('/serviços/', methods=['POST', 'GET'])
def serviços():
    email_cookie = request.cookies.get('email')
    if email_cookie is None:
        return redirect('/login')
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
    email_cookie = request.cookies.get('email')
    if email_cookie is None:
        return redirect('/login')
    return render_template('escolhas.html')

@app.route('/escolhas_post', methods=['POST', 'GET'])
def escolhas_post():
    print("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC")
    if request.method == 'POST':
        print("AAAAAAAAAAAAAAAAAAAAAa")
        print('request:', request)
        option1 = request.form.get('option1')
        option2 = request.form.get('option2')
        print('option1:', option1)
        print('option2:', option2)
        if  ((option1 == '1' and option2 == '2')):
            resp = make_response(redirect('/tutoriais/'))
            resp.set_cookie('option','1')
            return resp
        elif  ((option1 == '2' and option2 == '2')):
            resp = make_response(redirect('/assistentes/'))
            resp.set_cookie('option','1')
            return resp
        elif  ((option1 == '1' and option2 == '1')):
            resp = make_response(redirect('/tutoriais/'))
            resp.set_cookie('option','0')
            return resp
        elif  ((option1 == '2' and option2 == '1')):
            resp = make_response(redirect('/assistentes/'))
            resp.set_cookie('option','0')
            return resp
    return redirect('/escolhas/')


@app.route('/assistentes/')
def assistentes():
    email_cookie = request.cookies.get('email')
    if email_cookie is None:
        return redirect('/login')
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
    draw()
    email_cookie = request.cookies.get('email')
    if email_cookie is None:
        return redirect('/login')
    return render_template('catalogo.html', item=items)

@app.route('/catalogo_post', methods=['POST', 'GET'])
def catalogo_post():
    print("AAAAAAAAAAAAAAAAAA")
    
    if request.method == 'POST':
        print("AAAAAAAAAAAAAA")
        print(request.form)

        if 'carrinho' in request.form:
            return redirect('/pagamento/')
        
        for i in request.form:
            
            for item in items:
                if item['name'] == i:
                    compra[item['name']] = compra[item['name']] + 1
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


    email_cookie = request.cookies.get('email')
    if email_cookie is None:    
        return redirect('/login')

    return render_template('pagamento.html', conta=conta, prod = prod)

@app.route('/pagamento_post', methods=['POST', 'GET'])
def pagamento_post():
    if request.method == 'POST':
        for i in compra:
            compra[i] = 0

        with open('service.json', 'r') as f:
            task = json.load(f)
        
        service = task['service']
        email_cookie = request.cookies.get('email')
        #get todays date
        today = datetime.date.today()
        DB.add_task(email_cookie, service, today, 'pendente')

        return redirect('/index/')
    return redirect('/pagamento/')


@app.route('/account/', methods=['GET', 'POST'])
def account():
    email_cookie = request.cookies.get('email')
    if email_cookie is None:
        return redirect('/login')
    
    email,tel,date, morada = DB.get_user_info(email_cookie)

    task = DB.get_tasks(email_cookie)

    return render_template('account.html', morada=morada, email=email, tel=tel, bir=date, task=task)

@app.route('/account_post', methods=['POST', 'GET'])
def account_post():
    email = request.form.get('email')
    tel = request.form.get('phone')
    date_str = request.form.get('birth')
    address = request.form.get('lastname')
    if request.method == 'POST':
        if 'Mudar' in request.form:
            DB.update_user(email, tel, date_str, address)
            return redirect('/account/')
        if 'Eliminar' in request.form:
            DB.delete_user(email)
            resp = make_response(redirect('/index'))
            resp.delete_cookie('email')
            return resp

    return redirect('/account/')

@app.route('/tutoriais/', methods=['GET', 'POST'])
def tutoriais():

    if request.method == 'POST':
        return redirect('/assistentes/')

    email_cookie = request.cookies.get('email')
    if email_cookie is None:
        return redirect('/login')
    return render_template('tutoriaispintura.html')


@app.route('/sobre/')
def sobre():
    email_cookie = request.cookies.get('email')
    if email_cookie is None:
        return redirect('/login')
    return render_template('sobre.html')

@app.route('/cenas/', methods=['GET', 'POST'])
def cenas():
    a = 'ola'
    b = 'teste'
    return render_template('cenas.html', a=a, b=b)



if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
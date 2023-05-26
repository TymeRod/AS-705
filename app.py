import time
from flask import Flask, render_template, request, redirect, make_response
import hashlib
import datetime
import DB
from PIL import Image, ImageDraw, ImageFont


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

def catalogo_post():
    draw()
    if request.method == 'POST':
        if 'carrinho' in request.form:
            return redirect('/pagamento/')
<<<<<<< HEAD
        
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
=======
        if 'tintaAcril' in request.form:         
            compra.append('Tinta mate exterior BRANCO 5L')
            draw()
        if 'tinta' in request.form:
            compra.append('Tinta mate exterior BRANCO 4L')
            draw()
        if 'pincel' in request.form:
            compra.append('Pincel  UNIVERSAL PP 60MM')
            draw()
        if 'rolo' in request.form:
            compra.append('Rolo Antigota Poliamida')
            draw()
        if 'tintaExtInt' in request.form:
            compra.append('Tinta anti-mofo 5 L, branco')
            draw()
    return render_template('catalogo.html')


>>>>>>> aacc3af603b93cff6617f61e5e03a520a93305d3

    return render_template('catalogo.html', tintaAcril=tintaAcril, 
                           tinta = tinta, pincel = pincel, 
                           rolo = rolo, tintaExtInt = tintaExtInt
                           )


@app.route('/pagamento/', methods=['GET', 'POST'])
def pagamento():
<<<<<<< HEAD
    conta = 0
    prod = []
    for i in compra:
        conta += preço[i]*compra[i]

    for i in compra:
        for j in range(int(compra[i])):
            prod.append(i)

    print(prod)

    return render_template('pagamento.html', conta=conta, prod = prod)
=======
    for i in compra:
        print(i)
    return render_template('pagamento.html', compra=compra)
>>>>>>> aacc3af603b93cff6617f61e5e03a520a93305d3

if __name__ == '__main__':
    app.run(debug=True)
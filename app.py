from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('sitio/index.html')

@app.route('/Numeros')
def numeros():
    return render_template('sitio/Numeros.html')

@app.route('/vocales')
def vocales():
    return render_template('sitio/vocales.html')

if __name__ == '__main__':
    app.run(port = 3000,debug=True)
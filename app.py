from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

CONFIG = {
  "apiKey": "AIzaSyBZRsmG7fmpaDN5p0svagIUBsDjTqS1w3w",
  "authDomain": "hackathon-3971c.firebaseapp.com",
  "databaseURL": "https://hackathon-3971c-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "hackathon-3971c",
  "storageBucket": "hackathon-3971c.appspot.com",
  "messagingSenderId": "498367814246",
  "appId": "1:498367814246:web:7a0c64806c6d7588406ba7"
}

firebase = pyrebase.initialize_app(CONFIG)
auth = firebase.auth()
db = firebase.database()

@app.route('/', methods=['GET', 'POST'])
def index():
  return render_template("index.html")

@app.route('/signup/<musician>', methods=['GET', 'POST'])
def signup(musician):
  error = ""
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']
    if musician:
      experience = request.form['experience']
      pay = request.form['pay']
      user = {"email": email, "password": password, "username" : request.form['Username'], "experience": experience, "pay": pay}
    else:
      address = request.form['address']
      budget = request.form['budget']
      user = {"email": email, "password": password, "username" : request.form['Username'], "address": address, "budget": budget}
    try:
      login_session['user'] = auth.create_user_with_email_and_password(email, password)
      db.child('Users').child(login_session['user']['localId']).set(user)
      return render_template("home.html")
    except:
      error = "Authentication failed"
      print (error)
  return render_template("signup.html", musician=musician)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
  error = ""
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']
    try:
      login_session['user'] = auth.sign_in_with_email_and_password(email, password)
      return render_template("home.html")
    except Exception as e:
      error = "Authentication failed"
      print (e)
  return render_template("signin.html")


@app.route('/home', methods=['GET', 'POST'])
def home():
  return render_template('home.html')

@app.route("/signout")
def signout():
  login_session['user'] = None
  auth.current_user = None
  return redirect(url_for('signin'))


if __name__ == '__main__':
  app.run(debug=True)

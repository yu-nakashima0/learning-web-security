from flask import Flask, request, render_template ,redirect, url_for, session
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('userpage'))
    return render_template('login.html')

@app.route('/userpage')
def userpage():
    if 'username' in session:
        print(f"Hello, {session['username']}! You are logged in.")
        return render_template('userpage.html')
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
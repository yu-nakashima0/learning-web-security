from flask import Flask, request, render_template ,redirect, url_for, session
from config import Config
import sqlite3
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
app.config.from_object(Config)

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    print("user registerd")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_pw = generate_password_hash(password)
        conn = get_db()
        cur = conn.cursor()
        
        try:
            
            cur.execute(
                "INSERT INTO users(username, password) VALUES (?, ?)",
                (username, hashed_pw)
            )
            conn.commit()
            print("user registerd")
        except sqlite3.IntegrityError:
            conn.close()
            return "Username already exists"

        conn.close()
        return redirect(url_for('login')) 
    
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'login':
            username = request.form['username']
            password = request.form['password']

            conn = get_db()
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cur.fetchone()
            conn.close()
            
            if user and check_password_hash(user["password"], password):
                session['username'] = username
                return redirect(url_for('userpage'))
            else:
                return render_template('login.html', error="Login failed")
            
        elif action == 'register':
            return redirect(url_for('register'))
        
    return render_template('login.html')


@app.route('/userpage')
def userpage():
    if 'username' in session:
        print(f"Hello, {session['username']}! You are logged in.")
        return render_template('userpage.html')
    else:
        return redirect(url_for('login'))

@app.route('/userpage', methods=['POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('login'))
    else:
        return redirect(url_for('userpage'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
from flask import Flask, request, render_template ,redirect, url_for, session
from config import Config
import sqlite3
from werkzeug.security import generate_password_hash,check_password_hash
from flask_socketio import SocketIO, emit



app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app) #socket



"""
databank
"""
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

"""
start page
"""
@app.route('/')
def home():
    return redirect(url_for('login'))


"""
register page
"""
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


"""
login page
"""
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


"""
userpage
"""
@app.route('/userpage', methods=['GET', 'POST'])
def userpage():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Logout with POST
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('login'))

    # Only pass username to template
    return render_template('userpage.html', username=session['username'])

"""
chat message
"""
@socketio.on("chat_message")
def handle_chat(data):
    emit("chat_message", data, broadcast=True)



"""
start app
"""
if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000,debug=True)
    socketio.run(app, host='0.0.0.0', port= 5000, debug= True)
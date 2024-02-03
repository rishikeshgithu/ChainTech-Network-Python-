# app.py
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# SQLite database setup
conn = sqlite3.connect('data.db')
conn.execute('CREATE TABLE IF NOT EXISTS submissions (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT)')
conn.close()

@app.route('/')
def home():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('index.html', current_time=current_time)

@app.route('/', methods=['POST'])
def form_submission():
    if request.method == 'POST':
        user_name = request.form['name']
        user_email = request.form['email']
        
        # Store data in the database
        conn = sqlite3.connect('data.db')
        conn.execute('INSERT INTO submissions (name, email) VALUES (?, ?)', (user_name, user_email))
        conn.commit()
        conn.close()

        return redirect(url_for('confirmation'))
    return render_template('index.html')

@app.route('/confirmation')
def confirmation():
    # Retrieve and display stored data
    conn = sqlite3.connect('data.db')
    cursor = conn.execute('SELECT name, email FROM submissions')
    submissions = cursor.fetchall()
    conn.close()
    
    return render_template('confirmation.html', submissions=submissions)

@app.route('/database')
def database():
    # Directly display the database page with stored data
    conn = sqlite3.connect('data.db')
    cursor = conn.execute('SELECT name, email FROM submissions')
    submissions = cursor.fetchall()
    conn.close()

    return render_template('database.html', submissions=submissions)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

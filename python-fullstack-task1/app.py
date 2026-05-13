from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, 
                 name TEXT, email TEXT)''')
    count = conn.execute(
        'SELECT COUNT(*) FROM users').fetchone()[0]
    if count == 0:
        sample_users = [
            ('Rahul Sharma', 'rahul.sharma@gmail.com'),
            ('Priya Patel', 'priya.patel@gmail.com'),
            ('Arjun Kumar', 'arjun.kumar@gmail.com'),
            ('Sneha Reddy', 'sneha.reddy@gmail.com'),
            ('Vikram Singh', 'vikram.singh@gmail.com'),
            ('Anita Nair', 'anita.nair@gmail.com'),
            ('Ravi Verma', 'ravi.verma@gmail.com'),
            ('Pooja Mehta', 'pooja.mehta@gmail.com'),
        ]
        conn.executemany(
            'INSERT INTO users (name, email) VALUES (?, ?)',
            sample_users
        )
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        conn.execute(
            'INSERT INTO users (name, email) VALUES (?, ?)',
            (name, email)
        )
        conn.commit()
        conn.close()
        return redirect('/')
    users = conn.execute(
        'SELECT * FROM users').fetchall()
    conn.close()
    return render_template('index.html', users=users)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
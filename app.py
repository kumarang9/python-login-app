from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

HTML = """
<h2>Login Page</h2>
<form method="POST">
Username: <input type="text" name="username"><br><br>
Password: <input type="password" name="password"><br><br>
<input type="submit">
</form>
"""

def init_db():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT,
        password TEXT
    )
    ''')

    cur.execute("INSERT INTO users VALUES ('admin','admin123')")

    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cur.fetchone()
        conn.close()

        if user:
            return "Login Success"
        else:
            return "Invalid Credentials"

    return render_template_string(HTML)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
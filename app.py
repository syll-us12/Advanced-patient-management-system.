from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change to something secure

# ---------------------------
# 1. Initialize Database & Admin
# ---------------------------
def init_db():
    conn = sqlite3.connect('apms.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0
    )
    ''')
    
    # Patients table
    c.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT NOT NULL,
        age INTEGER,
        diagnosis TEXT,
        treatment TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')
    
    # Create default admin if not exists
    c.execute('SELECT * FROM users WHERE username = ?', ('admin',))
    if not c.fetchone():
        hashed_pw = generate_password_hash('admin123')
        c.execute('INSERT INTO users (username, password, is_admin) VALUES (?, ?, 1)', ('admin', hashed_pw))
    
    conn.commit()
    conn.close()
    print("Database and tables created successfully!")

init_db()

# ---------------------------
# 2. Routes
# ---------------------------

# ---- Login ----
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('apms.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()
        
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['is_admin'] = user[3]
            if session['is_admin']:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')

# ---- Register ----
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_pw = generate_password_hash(password)
        
        conn = sqlite3.connect('apms.db')
        c = conn.cursor()
        try:
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_pw))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return "Username already exists."
        conn.close()
        return redirect(url_for('login'))
    
    return render_template('register.html')

# ---- User Dashboard ----
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('is_admin') == 1:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('apms.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM patients WHERE user_id = ?', (session['user_id'],))
    patients = c.fetchall()
    conn.close()
    
    return render_template('dashboard.html', patients=patients, username=session['username'])

# ---- Add Patient ----
@app.route('/add', methods=['POST'])
def add_patient():
    if 'user_id' not in session or session.get('is_admin') == 1:
        return redirect(url_for('login'))
    
    name = request.form['name']
    age = request.form['age']
    diagnosis = request.form['diagnosis']
    treatment = request.form['treatment']
    
    conn = sqlite3.connect('apms.db')
    c = conn.cursor()
    c.execute('INSERT INTO patients (user_id, name, age, diagnosis, treatment) VALUES (?, ?, ?, ?, ?)',
              (session['user_id'], name, age, diagnosis, treatment))
    conn.commit()
    conn.close()
    
    return redirect(url_for('dashboard'))

# ---- Delete Patient ----
@app.route('/delete/<int:id>')
def delete_patient(id):
    if 'user_id' not in session or session.get('is_admin') == 1:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('apms.db')
    c = conn.cursor()
    c.execute('DELETE FROM patients WHERE id = ? AND user_id = ?', (id, session['user_id']))
    conn.commit()
    conn.close()
    
    return redirect(url_for('dashboard'))

# ---- Admin Dashboard ----
@app.route('/admin')
def admin_dashboard():
    if 'user_id' not in session or session.get('is_admin') != 1:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('apms.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # All users
    c.execute('SELECT id, username, is_admin FROM users')
    users = c.fetchall()
    
    # All patients
    c.execute('SELECT p.id, p.name, p.age, p.diagnosis, p.treatment, u.username FROM patients p JOIN users u ON p.user_id = u.id')
    patients = c.fetchall()
    
    conn.close()
    return render_template('admin_dashboard.html', users=users, patients=patients)

# ---- Admin Delete User ----
@app.route('/admin/delete_user/<int:id>')
def delete_user(id):
    if 'user_id' not in session or session.get('is_admin') != 1:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('apms.db')
    c = conn.cursor()
    
    # Delete all patients of the user first
    c.execute('DELETE FROM patients WHERE user_id = ?', (id,))
    # Delete the user
    c.execute('DELETE FROM users WHERE id = ?', (id,))
    
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))

# ---- Logout ----
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ---------------------------
# 3. Run the app
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True)

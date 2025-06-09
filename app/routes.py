from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
import sqlite3

bp = Blueprint('main', __name__)


def get_db():
    return sqlite3.connect(current_app.config['DATABASE'])


def check_login(username: str, password: str) -> bool:
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT id FROM users WHERE username=? AND password=?', (username, password))
    user = cur.fetchone()
    conn.close()
    if user:
        session['user_id'] = user[0]
        session['username'] = username
        return True
    return False


def get_orders(user_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT item FROM orders WHERE user_id=?', (user_id,))
    orders = [row[0] for row in cur.fetchall()]
    conn.close()
    return orders


@bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_login(username, password):
            return redirect(url_for('main.dashboard'))
        error = 'Credenciais inválidas'
    return render_template('login.html', error=error)


@bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    return render_template('dashboard.html', username=session.get('username'))


@bp.route('/pedidos')
def pedidos():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    orders = get_orders(session['user_id'])
    return render_template('pedidos.html', orders=orders)

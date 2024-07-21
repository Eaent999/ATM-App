from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# ฟังก์ชันสำหรับการเชื่อมต่อกับฐานข้อมูล
def connect_db():
    return sqlite3.connect('atm.db')

# สร้างตารางบัญชีในฐานข้อมูลถ้ายังไม่มี
def init_db():
    with connect_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                account_number TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                balance REAL NOT NULL
            )
        ''')
    print("Database initialized!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        account_number = request.form['account_number']
        username = request.form['username']
        balance = float(request.form['balance'])
        with connect_db() as conn:
            conn.execute('INSERT INTO accounts (account_number, username, balance) VALUES (?, ?, ?)',
                         (account_number, username, balance))
        return redirect(url_for('index'))
    return render_template('create_account.html')

@app.route('/view_balance', methods=['GET', 'POST'])
def view_balance():
    if request.method == 'POST':
        account_number = request.form['account_number']
        with connect_db() as conn:
            account = conn.execute('SELECT * FROM accounts WHERE account_number = ?', (account_number,)).fetchone()
            if account:
                return render_template('view_balance.html', account=account)
            else:
                return "Account not found"
    return render_template('view_balance.html')

@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if request.method == 'POST':
        account_number = request.form['account_number']
        amount = float(request.form['amount'])
        with connect_db() as conn:
            conn.execute('UPDATE accounts SET balance = balance + ? WHERE account_number = ?', (amount, account_number))
        return redirect(url_for('index'))
    return render_template('deposit.html')

@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if request.method == 'POST':
        account_number = request.form['account_number']
        amount = float(request.form['amount'])
        with connect_db() as conn:
            conn.execute('UPDATE accounts SET balance = balance - ? WHERE account_number = ?', (amount, account_number))
        return redirect(url_for('index'))
    return render_template('withdraw.html')

@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    if request.method == 'POST':
        account_number = request.form['account_number']
        with connect_db() as conn:
            conn.execute('DELETE FROM accounts WHERE account_number = ?', (account_number,))
        return redirect(url_for('index'))
    return render_template('delete_account.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

    # สมาชิกกลุ่ม
    # นาย กิติภูมิ บิลมาศ เลขที่ 3 รหัส 6749010003
    # นางสาว จิราวรรณ กมลทิพย์สุคนธ์ เลขที่ 4 รหัส 6749010004
    # นาย ชัชวาลย์ เมฆารักษ์กุล เลขที่ 6 รหัส 6749010006
    # นางสาว วริศรา สมนึก เลขที่ 17 รหัส 6749010017

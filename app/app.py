import os
import logging
from flask import Flask, request, render_template_string
import psycopg2
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'db'),
        database=os.environ.get('DB_NAME', 'crm_db'),
        user=os.environ.get('DB_USER', 'crm_user'),
        password=os.environ.get('DB_PASS', 'Crm@StrongPass#2026!')
    )

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            contact VARCHAR(100) NOT NULL,
            interaction_history TEXT
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Hệ thống CRM - DTC245200320</title></head>
<body style="font-family: Arial; max-width: 800px; margin: 40px auto;">
    <h2>Hệ thống Quản lý Khách hàng (CRM) - SV: DTC245200320</h2>
    <form method="POST" action="/add" style="margin-bottom: 20px;">
        <input type="text" name="name" placeholder="Tên khách hàng" required style="padding: 8px;">
        <input type="text" name="contact" placeholder="SĐT / Email" required style="padding: 8px;">
        <input type="text" name="history" placeholder="Lịch sử tương tác" required style="padding: 8px;">
        <button type="submit" style="padding: 8px 15px;">Thêm mới</button>
    </form>
    <hr>
    <h3>Danh sách khách hàng & Tương tác</h3>
    <ul>
    {% for c in customers %}
        <li style="margin-bottom: 8px;"><b>{{ c[1] }}</b> | Liên hệ: {{ c[2] }} | Tương tác: {{ c[3] }}</li>
    {% endfor %}
    </ul>
</body>
</html>
'''

@app.route('/')
def index():
    init_db()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM customers ORDER BY id DESC;')
    customers = cur.fetchall()
    cur.close()
    conn.close()
    app.logger.info("ACTION=VIEW_HOME STATUS=SUCCESS")
    return render_template_string(HTML_TEMPLATE, customers=customers)

@app.route('/add', methods=['POST'])
def add_customer():
    name = request.form['name']
    contact = request.form['contact']
    history = request.form['history']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO customers (name, contact, interaction_history) VALUES (%s, %s, %s)',
                (name, contact, history))
    conn.commit()
    cur.close()
    conn.close()
    app.logger.info(f"ACTION=ADD_CUSTOMER NAME={name} CONTACT={contact} STATUS=SUCCESS")
    return '<script>window.location.href="/";</script>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

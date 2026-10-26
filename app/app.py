import os
import logging
from datetime import datetime
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
            interaction_history TEXT,
            status VARCHAR(50) DEFAULT 'Khách hàng mới',
            created_at VARCHAR(50) DEFAULT '26/10/2026'
        );
    ''')
    cur.execute("ALTER TABLE customers ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'Khách hàng mới';")
    cur.execute("ALTER TABLE customers ADD COLUMN IF NOT EXISTS created_at VARCHAR(50) DEFAULT '26/10/2026';")
    conn.commit()
    cur.close()
    conn.close()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Hệ thống CRM - DTC245200320</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css" rel="stylesheet">
    <style>
        body { background-color: #f4f6f9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .navbar { background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); }
        .card { border: none; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); }
        .stat-card { border-left: 5px solid #2a5298; }
    </style>
</head>
<body>
    <nav class="navbar navbar-dark mb-4 shadow-sm">
        <div class="container">
            <span class="navbar-brand mb-0 h1">
                <i class="fa-solid fa-users-gear me-2"></i>HỆ THỐNG CRM CHĂM SÓC KHÁCH HÀNG
            </span>
            <span class="badge bg-light text-dark fs-6">Mã SV: DTC245200320</span>
        </div>
    </nav>

    <div class="container">
        <div class="row mb-4">
            <div class="col-md-4">
                <div class="card stat-card p-3 bg-white">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h6 class="text-muted mb-1">Tổng số khách hàng</h6>
                            <h3 class="fw-bold mb-0 text-primary">{{ customers|length }}</h3>
                        </div>
                        <i class="fa-solid fa-user-check fa-2x text-primary opacity-50"></i>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card stat-card p-3 bg-white" style="border-left-color: #198754;">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h6 class="text-muted mb-1">Trạng thái Database</h6>
                            <h5 class="fw-bold mb-0 text-success">PostgreSQL Connected</h5>
                        </div>
                        <i class="fa-solid fa-database fa-2x text-success opacity-50"></i>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card stat-card p-3 bg-white" style="border-left-color: #fd7e14;">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h6 class="text-muted mb-1">Giám sát & Bảo mật</h6>
                            <h5 class="fw-bold mb-0 text-warning">Prometheus + Loki Active</h5>
                        </div>
                        <i class="fa-solid fa-shield-halved fa-2x text-warning opacity-50"></i>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-md-4 mb-4">
                <div class="card p-4 bg-white">
                    <h5 class="fw-bold mb-3 text-secondary"><i class="fa-solid fa-user-plus me-2"></i>Thêm Khách Hàng Mới</h5>
                    <form method="POST" action="/add">
                        <div class="mb-3">
                            <label class="form-label fw-semibold">Họ và tên khách hàng</label>
                            <input type="text" name="name" class="form-control" placeholder="VD: Nguyễn Văn A" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-semibold">Thông tin liên hệ (SĐT / Email)</label>
                            <input type="text" name="contact" class="form-control" placeholder="VD: 0912345678 / email@..." required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-semibold">Trạng thái chăm sóc</label>
                            <select name="status" class="form-select">
                                <option value="Khách hàng mới">Khách hàng mới</option>
                                <option value="Đang tư vấn">Đang tư vấn</option>
                                <option value="Đã chốt hợp đồng">Đã chốt hợp đồng</option>
                                <option value="Cần hỗ trợ kỹ thuật">Cần hỗ trợ kỹ thuật</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-semibold">Lịch sử tương tác chi tiết</label>
                            <textarea name="history" class="form-control" rows="3" placeholder="Ghi chú nội dung cuộc gọi, yêu cầu của khách..." required></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary w-100 fw-semibold">
                            <i class="fa-solid fa-floppy-disk me-2"></i>Lưu Hồ Sơ Khách Hàng
                        </button>
                    </form>
                </div>
            </div>

            <div class="col-md-8">
                <div class="card p-4 bg-white">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h5 class="fw-bold mb-0 text-secondary"><i class="fa-solid fa-list-check me-2"></i>Danh Sách & Lịch Sử Tương Tác</h5>
                        <span class="text-muted small">Cập nhật: Thời gian thực</span>
                    </div>
                    <div class="table-responsive">
                        <table class="table table-hover align-middle">
                            <thead class="table-light">
                                <tr>
                                    <th>Mã KH</th>
                                    <th>Khách hàng</th>
                                    <th>Liên hệ</th>
                                    <th>Trạng thái</th>
                                    <th>Lịch sử tương tác</th>
                                    <th>Thao tác</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for c in customers %}
                                <tr>
                                    <td><span class="badge bg-secondary">#{{ c[0] }}</span></td>
                                    <td class="fw-bold text-dark">{{ c[1] }}<br><small class="text-muted fw-normal">{{ c[5] }}</small></td>
                                    <td><i class="fa-solid fa-phone-volume text-muted me-1"></i>{{ c[2] }}</td>
                                    <td>
                                        {% if c[4] == 'Đã chốt hợp đồng' %}
                                            <span class="badge bg-success">{{ c[4] }}</span>
                                        {% elif c[4] == 'Cần hỗ trợ kỹ thuật' %}
                                            <span class="badge bg-danger">{{ c[4] }}</span>
                                        {% else %}
                                            <span class="badge bg-info text-dark">{{ c[4] }}</span>
                                        {% endif %}
                                    </td>
                                    <td>{{ c[3] }}</td>
                                    <td>
                                        <form method="POST" action="/delete/{{ c[0] }}" style="display:inline;">
                                            <button type="submit" class="btn btn-sm btn-outline-danger"><i class="fa-solid fa-trash"></i></button>
                                        </form>
                                    </td>
                                </tr>
                                {% else %}
                                <tr>
                                    <td colspan="6" class="text-center text-muted py-4">Chưa có dữ liệu khách hàng. Hãy thêm khách hàng đầu tiên ở khung bên trái!</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    init_db()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name, contact, interaction_history, status, created_at FROM customers ORDER BY id DESC;')
    customers = cur.fetchall()
    cur.close()
    conn.close()
    app.logger.info("ACTION=VIEW_DASHBOARD STATUS=SUCCESS")
    return render_template_string(HTML_TEMPLATE, customers=customers)

@app.route('/add', methods=['POST'])
def add_customer():
    name = request.form['name']
    contact = request.form['contact']
    history = request.form['history']
    status = request.form.get('status', 'Khách hàng mới')
    now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO customers (name, contact, interaction_history, status, created_at) VALUES (%s, %s, %s, %s, %s)',
                (name, contact, history, status, now_str))
    conn.commit()
    cur.close()
    conn.close()
    app.logger.info(f"ACTION=ADD_CUSTOMER NAME={name} CONTACT={contact} STATUS={status}")
    return '<script>window.location.href="/";</script>'

@app.route('/delete/<int:cid>', methods=['POST'])
def delete_customer(cid):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM customers WHERE id = %s', (cid,))
    conn.commit()
    cur.close()
    conn.close()
    app.logger.warning(f"ACTION=DELETE_CUSTOMER ID={cid} STATUS=DELETED")
    return '<script>window.location.href="/";</script>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

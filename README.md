# Đề 4: Hệ thống CRM Chăm sóc Khách hàng - SV: DTC245200320

## 1. Thành phần hệ thống
- **Ứng dụng CRM**: Python Flask + Gunicorn (`crm_app`)
- **Cơ sở dữ liệu**: PostgreSQL 15 (`crm_db`) & pgAdmin 4 (`crm_pgadmin`)
- **Reverse Proxy**: Nginx (`crm_nginx`)
- **Giám sát**: Prometheus + Grafana + cAdvisor + Postgres Exporter
- **Quản lý Log**: Loki + Promtail

## 2. Lệnh khởi chạy hệ thống
```bash
docker compose up -d --build

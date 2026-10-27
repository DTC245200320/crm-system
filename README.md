[README.md](https://github.com/user-attachments/files/33992622/README.md)
# Hệ thống CRM chăm sóc khách hàng

**Học phần:** Triển khai và Quản trị Hệ thống Phần mềm  
**Sinh viên:** Phan Hà Thái Vinh  
**Mã sinh viên:** DTC245200320  
**Đề tài:** Đề 4 – Hệ thống CRM Chăm sóc Khách hàng

Repository: https://github.com/DTC245200320/crm-system

## 1. Giới thiệu

Đây là ứng dụng CRM dạng web dùng để lưu trữ và theo dõi thông tin khách hàng ở mức cơ bản. Ứng dụng cho phép xem danh sách khách hàng, thêm hồ sơ mới, ghi nhận thông tin liên hệ, lịch sử tương tác và trạng thái chăm sóc; đồng thời hỗ trợ xóa hồ sơ.

Dự án được đóng gói bằng Docker Compose. Nginx làm reverse proxy cho ứng dụng Flask/Gunicorn; PostgreSQL lưu dữ liệu; Prometheus, Grafana, cAdvisor và Postgres Exporter phục vụ giám sát; Loki và Promtail tập trung log container.

> **Lưu ý:** Đây là dự án thực hành. Phiên bản hiện tại chưa có đăng nhập/phân quyền, chưa cấu hình HTTPS và chưa tự động tạo datasource/dashboard Grafana. Không nên đưa hệ thống trực tiếp ra Internet trước khi xử lý các hạn chế bảo mật được nêu bên dưới.

## 2. Công nghệ sử dụng

| Thành phần | Vai trò |
|---|---|
| Python 3.11, Flask | Xử lý yêu cầu web và nghiệp vụ CRM |
| Gunicorn | Chạy ứng dụng Flask |
| PostgreSQL 15 | Lưu hồ sơ khách hàng |
| pgAdmin 4 | Giao diện quản trị PostgreSQL |
| Docker Compose | Khởi chạy và kết nối các dịch vụ |
| Nginx | Reverse proxy, chuyển tiếp yêu cầu đến ứng dụng |
| Prometheus | Thu thập metrics |
| Grafana | Trực quan hóa metrics và truy vấn log |
| cAdvisor | Thu thập metrics container |
| Postgres Exporter | Cung cấp metrics PostgreSQL cho Prometheus |
| Loki, Promtail | Lưu trữ và chuyển tiếp log container |

## 3. Kiến trúc tổng quan

```text
Trình duyệt
    |
    v
Nginx :80
    |
    v
Flask + Gunicorn :5000 ------> PostgreSQL :5432
    |                              |
    +----------> Prometheus <--- Postgres Exporter
                      ^
                      |
                  cAdvisor

Docker container logs --> Promtail --> Loki --> Grafana
```

Docker Compose khai báo ba mạng `frontend_net`, `backend_net` và `monitor_net`. Mạng `backend_net` được đánh dấu `internal: true`. PostgreSQL không công bố cổng trực tiếp ra host trong cấu hình hiện tại.

## 4. Yêu cầu

- Git
- Docker Engine hoặc Docker Desktop
- Docker Compose plugin (lệnh `docker compose`)
- Trình duyệt web

## 5. Cài đặt và khởi chạy

### Bước 1: Tải mã nguồn

```bash
git clone https://github.com/DTC245200320/crm-system.git
cd crm-system
```

### Bước 2: Kiểm tra thông tin xác thực trước khi chạy

**Không dùng nguyên cấu hình công khai cho môi trường thật.** Trong phiên bản hiện tại, các mật khẩu dịch vụ còn được khai báo trực tiếp trong `docker-compose.yml`; ứng dụng cũng có giá trị dự phòng cho mật khẩu cơ sở dữ liệu trong `app/app.py`.

Trước khi sử dụng, hãy thay các mật khẩu này bằng giá trị riêng, không dùng lại mật khẩu đã được đẩy lên GitHub. Nên chuyển thông tin nhạy cảm sang biến môi trường hoặc secret manager và bổ sung `.env.example` cùng `.gitignore` phù hợp. Không commit tệp chứa mật khẩu thật.

### Bước 3: Khởi động các dịch vụ

Tại thư mục gốc của dự án, chạy:

```bash
docker compose up -d --build
```

### Bước 4: Kiểm tra trạng thái

```bash
docker compose ps
docker compose logs --tail=100 crm_app
docker compose logs --tail=100 nginx
docker compose logs --tail=100 db
docker compose logs --tail=100 prometheus
docker compose logs --tail=100 loki
docker compose logs --tail=100 promtail
```

Nếu một dịch vụ chưa khởi động, đọc log của dịch vụ đó trước khi thử chạy lại.

## 6. Địa chỉ truy cập

Khi các container đang chạy trên cùng máy, những địa chỉ được ánh xạ trong `docker-compose.yml` là:

| Dịch vụ | Địa chỉ | Ghi chú |
|---|---|---|
| CRM qua Nginx | http://localhost | HTTP; chưa có HTTPS |
| pgAdmin 4 | http://localhost:5050 | Công cụ quản trị PostgreSQL |
| Prometheus | http://localhost:9090 | Kiểm tra trạng thái các scrape target |
| Grafana | http://localhost:3000 | Kiểm tra thông tin đăng nhập và cấu hình hiện tại |
| Loki | http://localhost:3101 | Cổng host được ánh xạ tới cổng 3100 trong container |

Thông tin đăng nhập pgAdmin và Grafana được cấu hình trong `docker-compose.yml`. Hãy đổi mật khẩu trước khi sử dụng và không đưa thông tin xác thực vào tài liệu hoặc ảnh chụp màn hình.

## 7. Kiểm tra chức năng CRM

1. Mở http://localhost.
2. Nhập tên khách hàng, thông tin liên hệ, trạng thái chăm sóc và lịch sử tương tác.
3. Gửi biểu mẫu để lưu hồ sơ.
4. Kiểm tra hồ sơ mới xuất hiện trong danh sách.
5. Thử thao tác xóa với dữ liệu thử nghiệm và xác nhận hồ sơ được gỡ khỏi danh sách.

Các chức năng hiện có chủ yếu là xem danh sách, thêm và xóa hồ sơ. Chưa có đăng nhập, phân quyền, chỉnh sửa hồ sơ hay tìm kiếm nâng cao.

## 8. Kiểm tra giám sát và log

### Prometheus

Mở http://localhost:9090, vào **Status → Targets** và kiểm tra các job đã khai báo trong `prometheus/prometheus.yml`, gồm:

- `prometheus`
- `crm_web_app`
- `postgres_db`
- `docker_containers`

Target cần ở trạng thái **UP**. Nếu target ở trạng thái **DOWN**, kiểm tra tên dịch vụ, mạng Docker, cổng exporter và log của container liên quan.

### Grafana

Mở http://localhost:3000. Cấu hình datasource Prometheus bằng URL nội bộ `http://prometheus:9090` khi Grafana và Prometheus có thể phân giải tên dịch vụ trên mạng chung. Cấu hình Loki bằng URL nội bộ `http://loki:3100`.

Repository hiện chưa cung cấp cấu hình provisioning datasource/dashboard; các datasource và dashboard cần được cấu hình trong Grafana hoặc bổ sung thành tệp provisioning.

### Loki / LogQL

Trong Grafana, mở **Explore**, chọn datasource Loki và kiểm tra nhãn thực tế được Promtail thu thập. Ví dụ:

```logql
{container="crm_app"}
```

Lọc các bản ghi thao tác xóa khách hàng:

```logql
{container="crm_app"} |= "DELETE_CUSTOMER"
```

Tìm log có dấu hiệu lỗi:

```logql
{container="crm_app"} |~ "(?i)error|exception|traceback"
```

Nếu không có kết quả, kiểm tra nhãn trong Explore và log của Promtail/Loki; selector phải khớp với nhãn thực tế.

## 9. Một số lệnh vận hành

Xem trạng thái container:

```bash
docker compose ps
```

Theo dõi log trực tiếp:

```bash
docker compose logs -f crm_app
```

Kiểm tra cấu hình Compose sau khi phân tích biến môi trường:

```bash
docker compose config
```

Dừng các dịch vụ:

```bash
docker compose down
```

Lệnh `docker compose down -v` sẽ xóa cả volume dữ liệu được Compose quản lý; không dùng nếu cần giữ dữ liệu PostgreSQL.

## 10. Hạn chế và việc cần làm tiếp

- Chuyển mật khẩu đang hard-code sang biến môi trường/secret manager; thay các mật khẩu đã công khai.
- Bổ sung xác thực, phân quyền và bảo vệ CSRF cho các thao tác thay đổi dữ liệu.
- Thêm kiểm tra dữ liệu phía máy chủ và xử lý lỗi cơ sở dữ liệu rõ ràng.
- Cấu hình HTTPS và kiểm tra lại các security headers.
- Giới hạn truy cập các cổng quản trị/giám sát và bảo vệ endpoint `/stub_status`.
- Đánh giá quyền truy cập Docker socket của Promtail và các mount hệ thống của cAdvisor.
- Bổ sung healthcheck, kiểm thử tự động, sao lưu/khôi phục PostgreSQL và cấu hình provisioning cho Grafana.
- Cân nhắc ghim phiên bản image thay vì dùng tag `latest` để dễ tái lập môi trường.

## 11. Tài liệu tham khảo

- Docker Compose: https://docs.docker.com/compose/
- Flask: https://flask.palletsprojects.com/
- PostgreSQL: https://www.postgresql.org/docs/
- Nginx: https://nginx.org/en/docs/
- Prometheus: https://prometheus.io/docs/
- Grafana: https://grafana.com/docs/
- Loki / LogQL: https://grafana.com/docs/loki/latest/


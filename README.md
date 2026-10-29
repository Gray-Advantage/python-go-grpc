# python_go_grpc

Практическая работа № 4 по дисциплине «Инструменты девопс» (РТУ МИРЭА).
Андреев С.Н., ЭФБО-01-24.

Сервис «бросок кубика»: клиент на Python (Django) вызывает сервер на Go по gRPC
с взаимной TLS-аутентификацией (mTLS) — напрямую и через nginx.

```
браузер ──► Django-клиент :8000 ──mTLS──► Go-сервер :8443
                         └──mTLS──► nginx :9448 ──h2c──► Go-сервер :50051
```

## Запуск (Ubuntu 24.04)

```bash
sudo apt install golang nginx protobuf-compiler golang-cfssl python3-venv
sh certs.sh                                  # CA, сертификаты сервера и клиента
python3 -m venv venv && source venv/bin/activate
pip install grpcio grpcio-tools django
go mod tidy
go run server/server.go &
nginx -p $(pwd) -c nginx.conf
python manage.py runserver                   # http://127.0.0.1:8000
```

Несколько клиентов: `python manage.py runserver 8001`, `python manage.py runserver 8002`.

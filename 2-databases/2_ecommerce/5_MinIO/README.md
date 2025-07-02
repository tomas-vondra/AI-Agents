# Install

https://hub.docker.com/r/minio/minio

```bash
docker volume create minio_data

docker run -d --name minio -p 9000:9000 -p 9001:9001 \
  -e "MINIO_ROOT_USER=admin" \
  -e "MINIO_ROOT_PASSWORD=password123" \
  -v minio_data:/data \
  quay.io/minio/minio server /data --console-address ":9001"
```

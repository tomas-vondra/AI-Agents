# Run

```bash
docker volume create mongo_data

docker run -d --name mongodb -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=secret -v mongo_data:/data/db mongo
```

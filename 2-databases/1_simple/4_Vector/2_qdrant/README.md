```bash
docker volume create qdrant_data

docker run -d --name qdrant -v qdrant_data:/data -p 6333:6333 qdrant/qdrant
```

UI - `http://localhost:6333/dashboard`

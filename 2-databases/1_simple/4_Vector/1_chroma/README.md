```bash
docker volume create chroma_data

docker run -d --name chromadb -v chroma_data:/data -p 8100:8000 chromadb/chroma
```

```python
import chromadb
chroma_client = chromadb.HttpClient(host='localhost', port=8000)
```

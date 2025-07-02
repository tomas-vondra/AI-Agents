# Install

```bash
docker volume create elastic_data

docker run -d \
  --name elasticsearch \
  -p 9200:9200 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  -v elastic_data:/usr/share/elasticsearch/data \
  docker.elastic.co/elasticsearch/elasticsearch:8.12.2
```

# UI

Kibana

```bash
docker volume create kibana_data

docker run -d \
  --name kibana \
  -p 5601:5601 \
  -e "ELASTICSEARCH_HOSTS=http://host.docker.internal:9200" \
  -v kibana_data:/usr/share/kibana/data \
  docker.elastic.co/kibana/kibana:8.12.2
```

Open `http://localhost:5601`

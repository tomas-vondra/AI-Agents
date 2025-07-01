# Qdrant Vector Database Service

This service provides AI-powered product recommendations and semantic search using Qdrant vector database.

## Features

- **Vector Similarity Search**: Find similar products using AI embeddings
- **Personalized Recommendations**: User-based recommendations using preference vectors
- **Semantic Search**: Natural language product search
- **Multiple Algorithms**: Hybrid, category-based, and price-based recommendations

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Start Qdrant database:
```bash
# From project root
docker-compose up -d qdrant
```

3. Populate database with embeddings:
```bash
uv run scripts/populate_data.py
```

4. Start API service:
```bash
uv run api/main.py
```

## API Endpoints

### Health Check
- `GET /health` - Service health status
- `GET /status` - Detailed database status

### Product Similarity
- `GET /similar/{product_id}` - Find similar products
  - Query params: `limit`, `category_filter`, `min_price`, `max_price`

### Personalized Recommendations
- `POST /recommendations/{user_id}` - Get user recommendations
  - Body: `{"algorithm": "hybrid", "limit": 10, "category_filter": "Electronics"}`
  - Algorithms: `hybrid`, `category_based`, `price_based`

### Semantic Search
- `POST /search/semantic` - Natural language search
  - Body: `{"query": "comfortable running shoes", "limit": 10}`

### Database Info
- `GET /collections/info` - Collection statistics

## Technology Stack

- **Qdrant**: Vector database for similarity search
- **SentenceTransformers**: AI model for generating embeddings
- **FastAPI**: REST API framework
- **Pydantic**: Data validation

## Database Schema

### Product Embeddings Collection
- **Vectors**: 384-dimensional embeddings from product descriptions
- **Metadata**: Product ID, name, category, brand, price, rating, features
- **Indexes**: Category, price, in_stock for fast filtering

### User Preference Embeddings Collection  
- **Vectors**: User preference embeddings from purchase history
- **Metadata**: User ID, premium status, spending patterns, preferences

## Example Usage

```bash
# Find similar products
curl http://localhost:8004/similar/1?limit=5

# Get personalized recommendations
curl -X POST http://localhost:8004/recommendations/1 \
  -H "Content-Type: application/json" \
  -d '{"algorithm": "hybrid", "limit": 10}'

# Semantic search
curl -X POST http://localhost:8004/search/semantic \
  -H "Content-Type: application/json" \
  -d '{"query": "wireless headphones for gaming", "limit": 5}'

# Check database status
curl http://localhost:8004/status
```

## Performance Notes

- Initial embedding generation takes 5-10 minutes for 1000 products
- Similarity search is sub-millisecond for collections up to 100K vectors
- User embeddings are generated from purchase history and preferences
- Vectors are 384-dimensional using all-MiniLM-L6-v2 model
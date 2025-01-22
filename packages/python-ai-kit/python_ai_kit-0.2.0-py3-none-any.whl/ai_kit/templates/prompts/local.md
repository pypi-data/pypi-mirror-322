---
name: local
description: Local document search and management
args:
  - command  # search, index, status
  - "--model (optional): Choose embedding model (text-embedding-3-small or text-embedding-3-large)"
  - "--force (optional): Force reindex all documents"
  - "--top-k (optional): Number of results to return for search"
---

# Using the local script

The local script provides semantic search capabilities over your local documents using OpenAI embeddings and BM25 ranking. Documents are automatically chunked into paragraphs for more precise search results.

## Basic Usage

```bash
# Search documents
ai-kit run local search "How does this work?" --top-k 5

# Reindex documents
ai-kit run local index

# Force reindex with different model
ai-kit run local index --force --model text-embedding-3-large

# Check index status
ai-kit run local status
```

## Commands

### search
Search through indexed documents using semantic search and BM25 ranking.
```bash
ai-kit run local search "your query here" --model text-embedding-3-small --top-k 5
```

### index
Index or reindex documents in the .ai/local directory.
```bash
ai-kit run local index --force --model text-embedding-3-small
```

### status
Show statistics about the current index.
```bash
ai-kit run local status
```

## Tips for best results

1. Place text files (.txt) in `.ai/local/` directory
2. Use natural language queries for best semantic matching
3. Reindex when you add new documents
4. Use `--force` when switching embedding models
5. Try both models to see which works better for your content

## Features

- Hybrid search combining semantic similarity and BM25 text matching
- Automatic paragraph chunking for precise results
- Embedding caching to avoid redundant API calls
- Multiple embedding model support
- Detailed status reporting 
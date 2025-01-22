# Documentation Crawler

This script crawls documentation websites and saves them as markdown files locally.

## Usage

```bash
# Basic usage - crawl a documentation site
aik run crawler https://docs.example.com

# Force re-crawl even if docs exist locally
aik run crawler https://docs.example.com --force

# Limit number of pages to crawl
aik run crawler https://docs.example.com --max-pages 100
```

## Features

- Automatically detects documentation sites
- Saves pages as markdown with proper structure
- Maintains local cache with timestamped versions
- Handles common documentation frameworks (Docusaurus, MkDocs, Sphinx)
- Preserves navigation and sections
- Creates README with documentation tree

## Examples

1. Crawl API documentation:
```
aik run crawler https://api.example.com/docs
```

2. Re-crawl updated documentation:
```
aik run crawler https://docs.example.com --force
```

3. Quick test with limited pages:
```
aik run crawler https://docs.example.com --max-pages 5
```

## Notes

- The script creates a directory named after the domain (e.g., "example-com" for example.com)
- Each crawl is saved in a timestamped subdirectory
- Use --force to ignore cached versions
- The script attempts to detect if a site is documentation before crawling 
---
name: search
description: Search the web using DuckDuckGo
args:
  - query
  - "--max-results/-n (optional): Maximum number of results to return (default: 10)"
---

# Using the search script

The search script uses DuckDuckGo to perform web searches and returns formatted results.
It's designed for quick research and information gathering directly from your terminal.

## Basic Usage

```bash
# Simple search
aik run search "What is Python programming?"

# Limit results
aik run search --max-results 5 "Best Python web frameworks"
aik run search -n 3 "How to handle async in Python"
```

## When to use search

- Quick research on programming topics
- Finding documentation and tutorials
- Exploring technical solutions
- Gathering reference material
- Fact-checking technical details
- Finding code examples and best practices

## When not to use search

- When you need AI-powered analysis (use reason instead)
- For accessing private or internal documentation
- When you need very recent information
- For accessing paywalled content
- When you need interactive debugging help

## Tips for best results

1. **Be specific** in your queries:
   ```bash
   # Good
   aik run search "Python asyncio event loop explanation"
   # Better than
   aik run search "Python async"
   ```

2. **Use max-results wisely**:
   - Default (10): Good for broad research
   - Lower (3-5): When you need quick, focused answers
   - Higher: When gathering comprehensive information

3. **Format your queries effectively**:
   - Include relevant keywords
   - Use quotes for exact phrases
   - Specify programming language/framework when relevant
   - Include version numbers when version-specific

4. **Combine with other tools**:
   ```bash
   # Search then analyze results
   aik run search "Python async patterns" | aik run reason "Analyze these patterns:"
   ```

## Example Workflows

1. **Research a new technology**:
   ```bash
   aik run search -n 5 "FastAPI vs Flask comparison 2024"
   ```

2. **Find specific documentation**:
   ```bash
   aik run search "Python requests library SSL verification docs"
   ```

3. **Debug an error**:
   ```bash
   aik run search "Python RuntimeError: Event loop is closed"
   ```

4. **Find best practices**:
   ```bash
   aik run search "Python asyncio best practices production"
   ``` 
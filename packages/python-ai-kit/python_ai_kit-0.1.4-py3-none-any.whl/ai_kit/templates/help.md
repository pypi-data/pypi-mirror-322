# AI Kit

AI Kit is the first CLI thats not designed for you. Its for your agent.

Designed to integrate with a text editor like Cursor or Windsurf (or any environment with a shell), it creates an .ai directory that both you and your agent have control over.

## Only one command for you
`init`
Initialize or reset AI Kit in your project. Optionally updates your .cursorrules file with a system prompt for your agent.
```bash
ai-kit init        # First-time setup
ai-kit init -f     # Force reset
```

## Commands For Your Agent

`local`
Search and manage your local documents
```bash
ai-kit local search "query"     # Search documents
ai-kit local index             # Index documents
ai-kit local status           # Show index info
```

`reason`
Get AI assistance with code and architecture
```bash
ai-kit reason "What does this code do?"
ai-kit reason --model o1-preview "Complex analysis"
```

`search`
Search the web using DuckDuckGo
```bash
ai-kit search "query"
ai-kit search -n 5 "specific query"
```

`crawler`
Download documentation for offline use
```bash
ai-kit crawler https://docs.example.com
ai-kit crawler --force --max-pages 50 https://docs.example.com
```

`reload`
Reset AI Kit while preserving your data
```bash
ai-kit reload      # Interactive reset
ai-kit reload -y   # Force reset
```

## Tips
- Place text files in `.ai/local/` for local search
- Use natural language for queries
- Reference files in reason queries with `{{file.py}}`
- Set `OPENAI_API_KEY` in `.env` for AI features 
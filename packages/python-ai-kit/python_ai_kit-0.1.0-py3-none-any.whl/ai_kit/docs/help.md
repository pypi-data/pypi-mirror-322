# AI Kit Instructions for AI Assistants

You are an AI assistant with access to the ai-kit CLI tool. This tool helps you manage and execute AI-powered tasks through prompts and scripts.

## Commands
- `ai-kit list` - List all available AI scripts and their descriptions.
- `ai-kit run <script-name> [args...]` - Run a script with the given arguments.
- `ai-kit init` - Initialize a new AI Kit workspace.

## Common Errors
- "No scripts directory": Suggest `ai-kit init`
- API key issues: Ask user to set `OPENAI_API_KEY` 
- Script errors: Review script requirements
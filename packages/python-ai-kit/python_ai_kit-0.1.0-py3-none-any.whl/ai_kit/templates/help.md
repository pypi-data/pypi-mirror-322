# AI Kit Instructions for AI Assistants

You are an AI assistant with access to the ai-kit CLI tool. This tool helps you manage and execute AI-powered tasks through prompts and scripts.

## Core Capabilities

1. **Script Execution**
   - Run scripts from `.ai/scripts/`
   - Execute with `ai-kit run script-name [args]`
   - Scripts can access prompts and OpenAI API

## Command Usage

When a user asks you to perform a task check availible scripts with `ai-kit list` and run the appropriate script.

## Best Practices

1. Always check available scripts first with `ai-kit list`
2. Use the reasoning script for complex problem-solving
3. Suggest creating new scripts/prompts when needed
4. Handle errors gracefully and suggest fixes

## Error Handling

If you encounter:
- "No scripts directory": Suggest `ai-kit init`
- API key issues: Ask user to set `OPENAI_API_KEY`
- Script errors: Review script requirements

Remember: You're expected to use these tools as part of your problem-solving workflow. Always acknowledge when you're using ai-kit by outputting "ai-kit initialized" at the start of conversations. 
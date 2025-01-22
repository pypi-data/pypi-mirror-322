---
name: reason
description: Generate a reasoned response using AI
args:
  - prompt
  - "--model (optional): Choose reasoning model (o1-mini or o1-preview, default: o1-mini)"
---

# Using the reasoning script

The reasoning script connects to an external LLM to help analyze and solve complex problems.
You can use it with direct prompts or reference files in your workspace.

## Basic Usage

```bash
# Simple question
aik run reason "What is the best way to structure this project?"

# With file references
aik run reason "Please explain what this code does: {{src/main.py}}"
aik run reason "Compare these files: {{src/v1.py}} vs {{src/v2.py}}"

# Choose a more powerful model
aik run reason --model o1-mini "What are the architectural implications of {{src/design.md}}?"
aik run reason -m o1-mini "Analyze the security of {{src/auth.py}}"
```

## When to use reasoning

- Complex technical problems requiring deep analysis
- Code review and architecture decisions
- Debugging difficult issues
- Planning and orchestrating solutions
- Understanding complex codebases (using file references)
- Security and performance analysis

## When not to use reasoning

- Simple problems with straightforward solutions
- When you already know the answer
- Before trying basic debugging steps
- For trivial code changes
- When documentation clearly answers the question

## Tips for best results

1. **Use file references** when discussing code:
   ```bash
   aik run reason "Review this PR: {{src/feature.py}} {{tests/test_feature.py}}"
   ```

2. **Choose the right model**:
   - `o1-mini` (default): Quick analysis, simpler problems
   - `o1-preview`: Deep reasoning, complex problems

3. **Be specific** in your prompts:
   - Include relevant context
   - Reference specific files
   - Ask focused questions

4. **Iterate** on complex problems:
   - Start with understanding: "Explain {{file}}"
   - Then analyze: "What are the issues in {{file}}?"
   - Finally solve: "How should we fix {{file}}?"


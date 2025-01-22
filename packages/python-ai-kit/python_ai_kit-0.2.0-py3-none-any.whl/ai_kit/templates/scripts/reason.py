"""
Reason about a prompt using AI.

This script takes a prompt as input and uses OpenAI's API to generate a reasoned response.
The prompt can contain file references using {{filename}} syntax, which will be replaced
with the contents of those files.

Usage:
    # Direct prompt
    ai-kit run reason "What is the purpose of life?"
    
    # With file references
    ai-kit run reason "Please explain this code: {{src/main.py}}"
    
    # Load prompt from file
    ai-kit run reason "{{prompts/deep_question.txt}}"
    
    # Specify model (o1-mini or o1-preview, defaults to o1-mini)
    ai-kit run reason --model o1-mini "What is the meaning of life?"
    ai-kit run reason -m o1-mini "What is the meaning of life?"
"""
from ai_kit.core.llms.openai_client import OpenAIClient, SUPPORTED_REASONING_MODELS
from ai_kit.utils.prompts import process_file_references
import asyncio
import argparse
import shlex

async def reason(prompt: str, model: str = "o1-mini") -> str:
    """Execute the reasoning request.
    
    Args:
        prompt: The question/task to reason about, may contain {{file}} references
        model: The reasoning model to use (o1-mini or o1-preview)
    """
    client = OpenAIClient(reasoning_model=model)
    
    # Process any {{file}} references in the prompt
    prompt_with_files = process_file_references(prompt)
    
    res = await client.reason(prompt_with_files)
    return res

def parse_args(args) -> tuple[str, str]:
    """Parse command line arguments.
    
    Handles both direct Python execution and aik run execution.
    Supports both --model/-m flag and positional prompt arguments.
    
    Args:
        args: Command line arguments (either as list[str] or tuple[str])
        
    Returns:
        tuple[str, str]: (model, prompt)
    """
    parser = argparse.ArgumentParser(description="Reason about a prompt using AI")
    parser.add_argument("--model", "-m", choices=SUPPORTED_REASONING_MODELS, 
                       default="o1-mini", help="Reasoning model to use")
    parser.add_argument("prompt", nargs="+", help="The prompt text (joined if multiple parts)")
    
    # Convert args to list and parse
    args_list = list(args) if isinstance(args, tuple) else args
    
    # Handle quoted arguments in strings (for aik run case)
    if len(args_list) == 1 and isinstance(args_list[0], str):
        args_list = shlex.split(args_list[0])
    
    # Parse only the known args, allowing for both - and -- prefix
    parsed_args, _ = parser.parse_known_args(args_list)
    
    # Join prompt parts
    prompt = " ".join(parsed_args.prompt)
    
    return parsed_args.model, prompt

def main(*args, **kwargs):
    """Run the reasoning script.
    
    Supports both:
    - Direct Python execution: python reason.py --model o1-mini "prompt"
    - aik run execution: aik run reason --model o1-mini "prompt"
    
    Args:
        *args: Command line arguments
        **kwargs: Additional keyword arguments (unused)
    """
    # Parse arguments
    model, prompt = parse_args(args)
    
    # Run the prompt
    res = asyncio.run(reason(prompt, model=model))
    print(res) # must print to stdout for aik run
    return res
    
if __name__ == "__main__":
    import sys
    sys.exit(main(*sys.argv[1:]))
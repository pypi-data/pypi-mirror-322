"""
Search the web using DuckDuckGo.

This script takes a search query as input and uses DuckDuckGo to search the web,
returning formatted results.

Usage:
    # Direct search
    ai-kit run search "What is Python?"
    
    # Specify max results
    ai-kit run search --max-results 5 "What is Python?"
    ai-kit run search -n 5 "What is Python?"
"""
from duckduckgo_search import DDGS
from typing import Dict, Any
import argparse
import shlex
import asyncio

async def search(query: str, max_results: int = 10) -> Dict[str, Any]:
    """Execute the web search request.
    
    Args:
        query: The search query to look up
        max_results: Maximum number of results to return
        
    Returns:
        Dict containing raw results and formatted results string
    """
    ddgs = DDGS()
    results = ddgs.text(query, max_results=max_results)
    res = {
        "raw_results": results,
        "results_string": "## Search Results\n\n"
        + "\n\n".join(f"[{r['title']}]({r['href']})\n{r['body']}" for r in results),
    }
    print(res) # must print to stdout for aik run
    return res

def validate_positive_int(value: str) -> int:
    """Validate that the input is a positive integer.
    
    Args:
        value: String value to validate
        
    Returns:
        Parsed positive integer
        
    Raises:
        ValueError: If value is not a positive integer
    """
    ivalue = int(value)
    if ivalue <= 0:
        raise ValueError(f"{value} is not a positive integer")
    return ivalue

def parse_args(args) -> tuple[str, int]:
    """Parse command line arguments.
    
    Handles both direct Python execution and aik run execution.
    Supports both --max-results/-n flag and positional query arguments.
    
    Args:
        args: Command line arguments (either as list[str] or tuple[str])
        
    Returns:
        tuple[str, int]: (query, max_results)
    """
    parser = argparse.ArgumentParser(description="Search the web using DuckDuckGo")
    parser.add_argument("--max-results", "-n", type=validate_positive_int, default=10,
                       help="Maximum number of results to return (must be positive)")
    parser.add_argument("query", nargs="+", help="The search query (joined if multiple parts)")
    
    # Convert args to list and parse
    args_list = list(args) if isinstance(args, tuple) else args
    
    # Handle quoted arguments in strings (for aik run case)
    if len(args_list) == 1 and isinstance(args_list[0], str):
        args_list = shlex.split(args_list[0])
    
    # Parse only the known args, allowing for both - and -- prefix
    parsed_args, _ = parser.parse_known_args(args_list)
    
    # Join query parts
    query = " ".join(parsed_args.query)
    
    return query, parsed_args.max_results

def main(*args, **kwargs):
    """Run the search script.
    
    Supports both:
    - Direct Python execution: python search.py --max-results 5 "query"
    - aik run execution: aik run search --max-results 5 "query"
    
    Args:
        *args: Command line arguments
        **kwargs: Additional keyword arguments (unused)
    """
    # Parse arguments
    query, max_results = parse_args(args)
    
    # Run the search
    res = asyncio.run(search(query, max_results=max_results))
    print(res["results_string"])
    return res
    
if __name__ == "__main__":
    import sys
    sys.exit(main(*sys.argv[1:]))
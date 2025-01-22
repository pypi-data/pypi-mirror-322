import click
import os
import sys
import shutil
import importlib.util
import importlib.resources
from pathlib import Path
from typing import Tuple, Optional
from dotenv import load_dotenv
from .config import get_default_config, save_config, load_config, ConfigNotFoundError, load_prompt_content, ROOT_DIR
from .utils.fs import remove_tree
from .core.local.index import LocalSearchIndex
from .core.llms.openai_client import OpenAIEmbeddingClient
import inspect
import asyncio
from rich.console import Console, Group
from rich.panel import Panel
from rich.markdown import Markdown
from rich.text import Text
from ai_kit.core.logging import configure_logging

# Constants for local search
DEFAULT_TOP_K = 5

def load_environment():
    """Load environment variables from .env files."""
    # Try loading from user's home directory first
    home_env = Path.home() / '.env'
    if home_env.exists():
        load_dotenv(home_env)
    
    # Then load from current directory, allowing it to override home settings
    local_env = Path('.env')
    if local_env.exists():
        load_dotenv(local_env, override=True)
    
    # Finally load from root directory if it exists
    ai_env = Path(ROOT_DIR) / '.env'
    if ai_env.exists():
        load_dotenv(ai_env, override=True)

def copy_templates(dest_dir: Path, force: bool = False) -> None:
    """Copy all template files to the destination directory."""
    pkg_root = importlib.resources.files('ai_kit')
    templates_dir = pkg_root / 'templates'
    if not templates_dir.is_dir():
        return

    # Copy scripts
    scripts_dir = templates_dir / 'scripts'
    if scripts_dir.is_dir():
        dest_scripts = dest_dir / 'scripts'
        for script in scripts_dir.glob('*.py'):
            dest_file = dest_scripts / script.name
            if force or not dest_file.exists():
                shutil.copy2(script, dest_scripts)

    # Copy prompts
    prompts_dir = templates_dir / 'prompts'
    if prompts_dir.is_dir():
        dest_prompts = dest_dir / 'prompts'
        for prompt in prompts_dir.glob('*.md'):
            dest_file = dest_prompts / prompt.name
            if force or not dest_file.exists():
                shutil.copy2(prompt, dest_prompts)
                
    # Copy .env.example
    env_example = templates_dir / '.env.example'
    if env_example.exists():
        dest_env = dest_dir / '.env.example'
        if force or not dest_env.exists():
            shutil.copy2(env_example, dest_env)
            console = Console()
            console.print("[green]✓ Created .env.example template[/green]")
            console.print("[dim]  Tip: Copy this to .env and customize your settings[/dim]")

def get_script_description(script_path: Path) -> str:
    """Extract the full docstring from a script file."""
    try:
        spec = importlib.util.spec_from_file_location("module", script_path)
        if spec is None or spec.loader is None:
            return "No description available"
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Get the module's docstring
        doc = inspect.getdoc(module)
        return doc if doc else "No description available"
    except Exception:
        return "No description available"

def get_help_content() -> str:
    """Get the help documentation from the package."""
    pkg_root = importlib.resources.files('ai_kit')
    help_path = pkg_root / 'templates' / 'help.md'
    try:
        with help_path.open('r') as f:
            return f.read()
    except Exception:
        return "Error: Could not load help documentation."

def get_docs() -> str:
    """Get the help documentation, always reading from the package."""
    return get_help_content()

def copy_help_doc(ai_dir: Path) -> None:
    """Copy help documentation to the .ai directory."""
    pkg_root = importlib.resources.files('ai_kit')
    help_path = pkg_root / 'templates' / 'help.md'
    dest_help = ai_dir / 'help.md'
    try:
        if help_path.is_file():
            shutil.copy2(help_path, dest_help)
    except Exception:
        pass

def update_cursorrules() -> None:
    """Update .cursorrules file with entry point text if it doesn't exist."""
    pkg_root = importlib.resources.files('ai_kit')
    entry_point_path = pkg_root / 'ai-kit-system-prompt.txt'
    
    try:
        if not entry_point_path.is_file():
            return
            
        entry_point_text = entry_point_path.read_text()
        cursorrules_path = Path('.cursorrules')
        
        # Check if entry point text already exists in .cursorrules
        if cursorrules_path.exists():
            current_content = cursorrules_path.read_text()
            if entry_point_text in current_content:
                return
            
            # Ask for confirmation with rich styling
            console = Console(stderr=True)
            console.print("\n[yellow]Found .cursorrules file.[/yellow]")
            response = console.input(
                "\n[blue]Would you like to add AI Kit instructions to .cursorrules? [green][Y/n][/green] [/blue]"
            ).strip().lower()
            
            # Default to yes if empty or 'y'
            if response in ['', 'y', 'yes']:
                # Append entry point text at the end
                with cursorrules_path.open('a') as f:
                    f.write('\n\n' + entry_point_text)
                console.print("[green]✓ Updated .cursorrules with AI Kit instructions[/green]")
            else:
                console.print("[yellow]Skipped updating .cursorrules[/yellow]")
        else:
            # For new files, still ask
            console = Console(stderr=True)
            response = console.input(
                "\n[blue]Would you like to create .cursorrules with AI Kit instructions? [green][Y/n][/green] [/blue]"
            ).strip().lower()
            
            if response in ['', 'y', 'yes']:
                cursorrules_path.write_text(entry_point_text)
                console.print("[green]✓ Created .cursorrules with AI Kit instructions[/green]")
            else:
                console.print("[yellow]Skipped creating .cursorrules[/yellow]")
            
    except Exception as e:
        console = Console(stderr=True)
        console.print(f"[red]Error updating .cursorrules: {e}[/red]")

def get_embedding_client(model: Optional[str] = None) -> OpenAIEmbeddingClient:
    """Get embedding client with configured model."""
    config = load_config()
    if model is None:
        model = config['models']['embeddings']['default']
    elif model not in config['models']['embeddings']['supported']:
        supported = config['models']['embeddings']['supported']
        raise click.BadParameter(
            f"Model {model} not supported. Choose from: {', '.join(supported)}"
        )
    return OpenAIEmbeddingClient(model)

def get_search_index(client: OpenAIEmbeddingClient) -> LocalSearchIndex:
    """Initialize LocalSearchIndex with standard paths."""
    return LocalSearchIndex(
        embedding_client=client,
        text_dir=".ai/local",
        index_path=".ai/local/faiss.idx",
        mapping_path=".ai/local/mapping.json",
        embedding_cache_path=".ai/local/embedding_cache.json",
        bm25_cache_path=".ai/local/bm25_corpus.json"
    )

def copy_system_prompt(ai_dir: Path) -> None:
    """Copy AI Kit system prompt to the .ai directory."""
    pkg_root = importlib.resources.files('ai_kit')
    prompt_path = pkg_root / 'ai-kit-system-prompt.txt'
    dest_prompt = ai_dir / 'ai-kit-system-prompt.txt'
    try:
        if prompt_path.is_file():
            shutil.copy2(prompt_path, dest_prompt)
            console = Console()
            console.print("[green]✓ Copied system prompt[/green]")
    except Exception as e:
        console = Console(stderr=True)
        console.print(f"[red]Error copying system prompt: {e}[/red]")

@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--log-level', type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR'], case_sensitive=False), default='ERROR', help='Set logging level')
def main(ctx, log_level):
    """AI development toolkit for managing prompts and scripts."""
    configure_logging(level=log_level.upper())
    
    # Load environment variables before any command execution
    load_environment()
    
    if ctx.invoked_subcommand is None:
        # Show help by default
        console = Console()
        docs = get_docs()
        console.print(Markdown(docs))

@main.command()
@click.option('--force', '-f', is_flag=True, help='Overwrite existing configuration and files')
def init(force: bool):
    """Initialize a new .ai directory structure."""
    console = Console()
    ai_dir = Path(ROOT_DIR)
    
    # If force is true and root dir exists, remove it entirely
    if force and ai_dir.exists():
        try:
            remove_tree(ai_dir)
            console.print(f"[yellow]Removed existing {ROOT_DIR} directory[/yellow]")
        except Exception as e:
            error_console = Console(stderr=True)
            error_console.print(f"[red]Error removing directory: {e}[/red]")
            sys.exit(1)
    
    # Create root directory and subdirectories
    try:
        os.makedirs(ai_dir / 'scripts', exist_ok=True)
        os.makedirs(ai_dir / 'prompts', exist_ok=True)
        os.makedirs(ai_dir / 'local', exist_ok=True)  # Create local storage directory
        
        # Create or update config file
        config_path = ai_dir / 'config.yaml'
        if force or not config_path.exists():
            config = get_default_config()
            save_config(config, ROOT_DIR)
            console.print("[green]✓ Created default configuration[/green]")
        
        # Copy template files
        copy_templates(ai_dir, force)
        console.print("[green]✓ Initialized directory structure with templates[/green]")
        
        # Copy help documentation
        copy_help_doc(ai_dir)
        console.print("[green]✓ Created help documentation[/green]")
        
        # Copy system prompt
        copy_system_prompt(ai_dir)
        
        # Update .cursorrules if it exists
        update_cursorrules()
        
    except Exception as e:
        error_console = Console(stderr=True)
        error_console.print(f"[red]Error creating directory structure: {e}[/red]")
        sys.exit(1)
    
    console.print("\n[bold green]✨ AI Kit initialization complete![/bold green]")

@main.command(context_settings={
    "ignore_unknown_options": True,
    "allow_extra_args": True
})
@click.argument('script_name')
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def run(script_name: str, args: Tuple[str, ...]):
    """Run a script from the scripts directory.
    
    SCRIPT_NAME is the name of the script to run (without .py extension)
    ARGS are any additional arguments to pass to the script, including flags
    """
    # Ensure root directory exists
    if not os.path.exists(ROOT_DIR):
        click.echo(f"Error: {ROOT_DIR} directory not found. Run 'ai-kit init' first.", err=True)
        sys.exit(1)

    # Build script path
    script_path = Path(ROOT_DIR) / 'scripts' / f"{script_name}.py"
    if not script_path.exists():
        click.echo(f"Error: Script '{script_name}.py' not found in {ROOT_DIR}/scripts/", err=True)
        sys.exit(1)

    try:
        # Import and run the script
        spec = importlib.util.spec_from_file_location(script_name, script_path)
        if spec is None or spec.loader is None:
            click.echo(f"Error: Could not load script '{script_name}.py'", err=True)
            sys.exit(1)
            
        module = importlib.util.module_from_spec(spec)
        sys.modules[script_name] = module
        spec.loader.exec_module(module)
        
        # Look for and call main() function if it exists
        if hasattr(module, 'main'):
            module.main(*args)
        else:
            click.echo("Warning: No main() function found in script", err=True)
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"Error running script: {str(e)}", err=True)
        sys.exit(1)

@main.command()
def list():
    """List all available AI scripts and their descriptions."""
    try:
        config = load_config()
    except ConfigNotFoundError:
        click.echo("No configuration found. Run 'ai init' to create one.")
        return
    
    console = Console()
    
    # Header
    console.print("\n[bold blue]🛠  AI Kit Scripts[/bold blue]")
    console.print("[dim]Run scripts using: ai-kit run <script-name> [args...][/dim]\n")
    
    for script_name, script_info in sorted(config['scripts'].items()):
        # Panel title
        title = f"[bold green]{script_info['name']}[/bold green]"
        
        # Build usage string
        if script_info['args']:
            args_str = ' '.join(f'<{arg}>' for arg in script_info['args'])
            usage = f"Usage:\n  ai-kit run {script_info['name']} {args_str}"
        else:
            usage = f"Usage:\n  ai-kit run {script_info['name']}"
        
        # Load prompt content from markdown file
        prompt_content = load_prompt_content(script_name)
        
        # Build all content as Rich renderables
        panel_content = [
            Text.from_markup(script_info['description']),  # description
            Text.from_markup(usage),                       # usage with dimmed style
            Markdown(prompt_content),                      # prompt from markdown file
        ]
        
        # Use Group to display multiple renderables in one Panel
        panel = Panel(
            Group(*panel_content),
            title=title,
            border_style="blue",
            padding=(1, 2),
            title_align="left",
            expand=False
        )

        console.print(panel)
        console.print("")  # extra spacing
    
    # Footer with total count
    script_count = len(config['scripts'])
    console.print(f"[dim]Found {script_count} available script{'s' if script_count != 1 else ''}[/dim]\n")

@main.command()
def help():
    """Display comprehensive AI Kit documentation."""
    console = Console()
    docs = get_docs()
    console.print(Markdown(docs))

@main.group()
def local():
    """Local document search and management."""
    # Ensure root directory exists
    if not os.path.exists(ROOT_DIR):
        click.echo(f"Error: {ROOT_DIR} directory not found. Run 'ai-kit init' first.", err=True)
        sys.exit(1)

@local.command()
@click.argument('query')
@click.option('--model', help='Embedding model to use')
@click.option('--top-k', default=DEFAULT_TOP_K, help='Number of results to return')
def search(query: str, model: Optional[str], top_k: int):
    """Search through indexed documents."""
    try:
        client = get_embedding_client(model)
        index = get_search_index(client)
        
        # Run async search in event loop
        results = asyncio.run(index.search(query, top_k=top_k))
        
        if not results:
            click.echo("No results found. Have you indexed any documents?")
            return
            
    except Exception as e:
        raise click.ClickException(str(e))

@local.command()
@click.option('--force', is_flag=True, help='Force reindex all documents')
@click.option('--model', help='Embedding model to use')
def index(force: bool, model: Optional[str]):
    """Reindex all documents."""
    try:
        client = get_embedding_client(model)
        index = get_search_index(client)
        
        click.echo("Indexing documents...")
        # Run async reindex in event loop
        asyncio.run(index.reindex_texts(force_reindex=force))
        click.echo("Indexing complete!")
        
    except Exception as e:
        raise click.ClickException(str(e))

@local.command()
def status():
    """Show index statistics."""
    try:
        # Use default model for status check
        client = get_embedding_client()
        index = get_search_index(client)
        
        # Load index and mapping
        index.load_faiss_index()
        index.load_mapping()
        
        # Gather stats
        total_vectors = index.index.ntotal if index.index else 0
        total_files = len(set(m['filename'] for m in index.mapping.values()))
        total_chunks = len(index.mapping)
        
        click.echo("\nLocal Search Index Status")
        click.echo("=======================")
        click.echo(f"Total files indexed: {total_files}")
        click.echo(f"Total text chunks: {total_chunks}")
        click.echo(f"Total vectors: {total_vectors}")
        click.echo(f"Index dimension: {index.dimension}")
        click.echo(f"\nPaths:")
        click.echo(f"  Text directory: {index.text_dir}")
        click.echo(f"  FAISS index: {index.index_path}")
        click.echo(f"  Mapping file: {index.mapping_path}")
        click.echo(f"  Embedding cache: {index.embedding_cache_path}")
        click.echo(f"  BM25 cache: {index.bm25_cache_path}")
        
    except Exception as e:
        raise click.ClickException(str(e))

@main.command()
@click.option('--yes', '-y', is_flag=True, help='Skip confirmation prompt')
def reload(yes: bool):
    """Reinitialize AI Kit, preserving .env and local/ directory."""
    console = Console()
    ai_dir = Path(ROOT_DIR)
    
    if not yes:
        console.print("\n[yellow]Warning: This will reset all AI Kit files except .env and local/ directory.[/yellow]")
        response = console.input(
            "\n[blue]Are you sure you want to continue? [green][y/N][/green] [/blue]"
        ).strip().lower()
        
        if response not in ['y', 'yes']:
            console.print("[yellow]Reload cancelled.[/yellow]")
            return

    try:
        # Save paths to preserve
        env_file = ai_dir / '.env'
        local_dir = ai_dir / 'local'
        
        # Temporarily move preserved files if they exist
        preserved_files = []
        if env_file.exists():
            temp_env = env_file.with_suffix('.env.temp')
            shutil.move(env_file, temp_env)
            preserved_files.append((temp_env, env_file))
            
        if local_dir.exists():
            temp_local = local_dir.with_suffix('.local.temp')
            shutil.move(local_dir, temp_local)
            preserved_files.append((temp_local, local_dir))
        
        # Remove everything in .ai directory
        if ai_dir.exists():
            remove_tree(ai_dir)
            console.print("[yellow]Removed existing configuration[/yellow]")
        
        # Create fresh directory structure
        os.makedirs(ai_dir / 'scripts', exist_ok=True)
        os.makedirs(ai_dir / 'prompts', exist_ok=True)
        os.makedirs(ai_dir / 'local', exist_ok=True)
        
        # Create fresh config
        config = get_default_config()
        save_config(config, ROOT_DIR)
        console.print("[green]✓ Created fresh configuration[/green]")
        
        # Copy template files
        copy_templates(ai_dir, force=True)
        console.print("[green]✓ Restored templates[/green]")
        
        # Copy help documentation
        copy_help_doc(ai_dir)
        console.print("[green]✓ Restored help documentation[/green]")
        
        # Copy system prompt
        copy_system_prompt(ai_dir)
        
        # Update .cursorrules
        update_cursorrules()
        
        # Restore preserved files
        for temp_path, original_path in preserved_files:
            if temp_path.exists():
                shutil.move(temp_path, original_path)
        
        console.print("\n[bold green]✨ AI Kit reloaded successfully![/bold green]")
        
    except Exception as e:
        error_console = Console(stderr=True)
        error_console.print(f"[red]Error reloading AI Kit: {e}[/red]")
        
        # Attempt to restore preserved files in case of error
        for temp_path, original_path in preserved_files:
            if temp_path.exists():
                shutil.move(temp_path, original_path)
        
        sys.exit(1)

if __name__ == '__main__':
    main() 
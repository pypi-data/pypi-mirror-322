import click
import os
import sys
import shutil
import importlib.util
import importlib.resources
from pathlib import Path
from typing import Tuple
from .config import get_default_config, save_config, load_config, ConfigNotFoundError
from .utils.fs import remove_tree
import inspect
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

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
    entry_point_path = pkg_root / 'entry_point.txt'
    
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

@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    """AI development toolkit for managing prompts and scripts."""
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
    ai_dir = Path('.ai')
    
    # If force is true and .ai exists, remove it entirely
    if force and ai_dir.exists():
        try:
            remove_tree(ai_dir)
            console.print("[yellow]Removed existing .ai directory[/yellow]")
        except Exception as e:
            error_console = Console(stderr=True)
            error_console.print(f"[red]Error removing directory: {e}[/red]")
            sys.exit(1)
    
    # Create .ai directory and subdirectories
    try:
        os.makedirs(ai_dir / 'scripts', exist_ok=True)
        os.makedirs(ai_dir / 'prompts', exist_ok=True)
        
        # Create or update config file
        config_path = ai_dir / 'config.json'
        if force or not config_path.exists():
            config = get_default_config()
            save_config(config, '.ai')
            console.print("[green]✓ Created default configuration[/green]")
        
        # Copy template files
        copy_templates(ai_dir, force)
        console.print("[green]✓ Initialized .ai directory structure with templates[/green]")
        
        # Create help documentation
        copy_help_doc(ai_dir)
        console.print("[green]✓ Created help documentation[/green]")
        
        # Update .cursorrules if it exists
        update_cursorrules()
        
    except Exception as e:
        error_console = Console(stderr=True)
        error_console.print(f"[red]Error creating directory structure: {e}[/red]")
        sys.exit(1)
    
    console.print("\n[bold green]✨ AI Kit initialization complete![/bold green]")

@main.command()
@click.argument('script_name')
@click.argument('args', nargs=-1)
def run(script_name: str, args: Tuple[str, ...]):
    """Run a script from the .ai/scripts directory.
    
    SCRIPT_NAME is the name of the script to run (without .py extension)
    ARGS are any additional arguments to pass to the script
    """
    # Ensure .ai directory exists
    if not os.path.exists('.ai'):
        click.echo("Error: .ai directory not found. Run 'ai-kit init' first.", err=True)
        sys.exit(1)

    # Build script path
    script_path = Path('.ai/scripts') / f"{script_name}.py"
    if not script_path.exists():
        click.echo(f"Error: Script '{script_name}.py' not found in .ai/scripts/", err=True)
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
        # Create a markdown panel for each script
        title = f"[bold green]{script_info['name']}[/bold green]"
        
        # Build description sections
        sections = []
        
        # Description
        sections.append(script_info['description'])
        
        # Usage
        if script_info['args']:
            args_str = ' '.join(f'<{arg}>' for arg in script_info['args'])
            usage = f"[bold yellow]Usage:[/bold yellow]\n  ai-kit run {script_info['name']} {args_str}"
            sections.append(usage)
        else:
            usage = f"[bold yellow]Usage:[/bold yellow]\n  ai-kit run {script_info['name']}"
            sections.append(usage)
        
        # When to use
        sections.append(f"[bold yellow]When to use:[/bold yellow]\n  {script_info['when_to_use']}")
        
        # Join sections with spacing
        content = "\n\n".join(sections)
        
        panel = Panel(
            content,
            title=title,
            border_style="blue",
            padding=(1, 2),
            title_align="left",
            expand=False
        )
        console.print(panel)
        console.print("")  # Add spacing between scripts
    
    # Footer with total count
    script_count = len(config['scripts'])
    console.print(f"[dim]Found {script_count} available script{'s' if script_count != 1 else ''}[/dim]\n")

@main.command()
def help():
    """Display comprehensive AI Kit documentation."""
    console = Console()
    docs = get_docs()
    console.print(Markdown(docs))

if __name__ == '__main__':
    main() 
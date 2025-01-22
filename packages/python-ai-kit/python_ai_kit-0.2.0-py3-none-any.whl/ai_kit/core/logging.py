import os
import logging
import logging.config
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from ..config import load_config, ConfigNotFoundError

# Global rich console for performance output
performance_console = Console()

def log_performance(operation: str, timings: dict, total_time: float):
    """
    Log performance metrics in a rich table format.
    Only logs when level is INFO or DEBUG.
    
    Args:
        operation: Name of the operation (e.g. "Index" or "Search")
        timings: Dictionary of step names and their durations
        total_time: Total operation time
    """
    logger = logging.getLogger("ai_kit")
    if logger.getEffectiveLevel() <= logging.INFO:
        table = Table(title=f"{operation} Performance Metrics")
        table.add_column("Step", style="cyan")
        table.add_column("Duration", style="magenta")
        table.add_column("Percentage", style="green")
        
        for step, duration in timings.items():
            percentage = (duration / total_time) * 100
            table.add_row(
                step,
                f"{duration:.3f}s",
                f"{percentage:.1f}%"
            )
        
        table.add_row(
            "Total",
            f"{total_time:.3f}s",
            "100%",
            style="bold"
        )
        
        performance_console.print()
        performance_console.print(Panel(table, expand=False))
        performance_console.print()

def configure_logging(level: str = None):
    """
    Configure logging for the ai-kit package.
    
    Args:
        level: Optional logging level (DEBUG, INFO, WARNING, ERROR) to override config.
              If not provided, uses level from config file.
    """
    try:
        config = load_config()
        log_level = level or config['logging']['level']
        log_file = os.path.expanduser(config['logging']['file'])
        console_format = config['logging']['format']['console']
        file_format = config['logging']['format']['file']
    except (ConfigNotFoundError, KeyError):
        # Use defaults if config not found or missing logging section
        log_level = level or "ERROR"
        log_file = os.path.expanduser("~/.ai-kit/ai-kit.log")
        console_format = "%(levelname)s - %(message)s"
        file_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "detailed": {
                "format": file_format,
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "simple": {
                "format": console_format
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },
            "file": {
                "class": "logging.FileHandler",
                "level": log_level,
                "formatter": "detailed",
                "filename": log_file,
                "mode": "a"
            }
        },
        "loggers": {
            "ai_kit": {
                "level": log_level,
                "handlers": ["console", "file"],
                "propagate": False
            }
        },
        "root": {
            "level": "WARNING",
            "handlers": ["console"]
        }
    }
    
    # Create log directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    os.makedirs(log_dir, exist_ok=True)
    
    # Apply configuration
    logging.config.dictConfig(logging_config)
    
    # Log configuration info
    logger = logging.getLogger("ai_kit")
    logger.info(f"Logging configured with level: {log_level}")
    if log_level == "DEBUG":
        logger.debug("Debug logging enabled - performance metrics will be shown") 
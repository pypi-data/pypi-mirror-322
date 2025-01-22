"""
Configuration management for AI-Kit projects.
Handles reading, writing, and validating config.yaml files.
"""

import os
import yaml
from pathlib import Path
import importlib.resources
from typing import Dict, Any, Optional, List

# Default configuration values
ROOT_DIR = ".ai"

class ConfigError(Exception):
    """Base class for configuration errors."""
    pass

class ConfigNotFoundError(ConfigError):
    """Raised when config.yaml cannot be found."""
    pass

class ConfigValidationError(ConfigError):
    """Raised when config.yaml fails validation."""
    pass

def get_default_config() -> Dict[str, Any]:
    """Get the default configuration from template."""
    pkg_root = importlib.resources.files('ai_kit')
    config_path = pkg_root / 'templates' / 'config.yaml'
    
    try:
        with config_path.open('r') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        raise ConfigError(f"Failed to load default config template: {e}")

def validate_config(config: Dict[str, Any]) -> None:
    """
    Validate configuration dictionary.
    
    Args:
        config: Configuration dictionary to validate
        
    Raises:
        ConfigValidationError: If configuration is invalid
    """
    required_keys = {'version', 'scripts_dir', 'prompts_dir', 'templates', 'scripts'}
    missing_keys = required_keys - set(config.keys())
    
    if missing_keys:
        raise ConfigValidationError(f"Missing required keys: {missing_keys}")
    
    if not isinstance(config['scripts_dir'], str):
        raise ConfigValidationError("scripts_dir must be a string")
    
    if not isinstance(config['prompts_dir'], str):
        raise ConfigValidationError("prompts_dir must be a string")
    
    if not isinstance(config['version'], str):
        raise ConfigValidationError("version must be a string")
        
    if not isinstance(config['scripts'], dict):
        raise ConfigValidationError("scripts must be a dictionary")
        
    for script_name, script_config in config['scripts'].items():
        required_script_keys = {'name', 'description', 'args'}
        missing_script_keys = required_script_keys - set(script_config.keys())
        if missing_script_keys:
            raise ConfigValidationError(f"Script {script_name} missing required keys: {missing_script_keys}")
            
        if not isinstance(script_config['name'], str):
            raise ConfigValidationError(f"Script {script_name} name must be a string")
        if not isinstance(script_config['description'], str):
            raise ConfigValidationError(f"Script {script_name} description must be a string")
        if not isinstance(script_config['args'], list):
            raise ConfigValidationError(f"Script {script_name} args must be a list")

def load_config(ai_dir: str = None) -> Dict[str, Any]:
    """
    Load configuration from config.yaml.
    
    Args:
        ai_dir: Optional path to root directory. If not provided, uses ROOT_DIR
        
    Returns:
        Configuration dictionary
        
    Raises:
        ConfigNotFoundError: If config.yaml doesn't exist
        ConfigValidationError: If config.yaml is invalid
    """
    if ai_dir is None:
        ai_dir = ROOT_DIR
        
    config_path = Path(ai_dir) / 'config.yaml'
    
    if not config_path.exists():
        raise ConfigNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path) as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ConfigValidationError(f"Invalid YAML in config file: {e}")
    
    if config is None:
        config = {}
    
    # Merge with defaults
    full_config = get_default_config()
    full_config.update(config)
    
    validate_config(full_config)
    return full_config

def save_config(config: Dict[str, Any], ai_dir: str = None) -> None:
    """
    Save configuration to config.yaml.
    
    Args:
        config: Configuration dictionary to save
        ai_dir: Optional path to root directory. If not provided, uses ROOT_DIR
        
    Raises:
        ConfigValidationError: If configuration is invalid
    """
    if ai_dir is None:
        ai_dir = ROOT_DIR
        
    validate_config(config)
    
    config_path = Path(ai_dir) / 'config.yaml'
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    with open(config_path, 'w') as f:
        yaml.safe_dump(config, f, indent=2, sort_keys=False)

def load_prompt_content(script_name: str, ai_dir: str = None) -> str:
    """
    Load prompt content from a markdown file.
    
    Args:
        script_name: Name of the script to load prompt for
        ai_dir: Optional path to root directory. If not provided, uses ROOT_DIR
        
    Returns:
        The prompt content as a string
    """
    if ai_dir is None:
        ai_dir = ROOT_DIR
        
    config = load_config(ai_dir)
    prompt_path = Path(ai_dir) / config['prompts_dir'] / f"{script_name}.md"
    
    try:
        if prompt_path.exists():
            return prompt_path.read_text()
        return "No prompt content available."
    except Exception as e:
        return f"Error loading prompt: {e}"

def get_local_dir(root_dir: str = ROOT_DIR) -> Path:
    """Get the path to the local storage directory.
    
    Args:
        root_dir: The root directory containing the .ai folder. Defaults to ROOT_DIR.
        
    Returns:
        Path to the local storage directory.
        
    Raises:
        ConfigNotFoundError: If config.yaml is not found.
    """
    config = load_config(root_dir)
    local_dir = Path(root_dir) / config.get('local_dir', 'local')
    return local_dir 
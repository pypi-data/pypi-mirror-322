"""
Script to crawl documentation sites and save them as markdown files locally.
Includes local directory caching and consistent naming.
"""
import asyncio
import os
import logging
import shutil
from datetime import datetime, timedelta
from urllib.parse import urlparse
from pathlib import Path
from typing import Optional
import click
import requests
from ai_kit.core.crawler.crawler import CrawlSupervisor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_domain_dir(url: str) -> str:
    """Get standardized directory name from URL domain.
    
    Args:
        url: The URL to parse
        
    Returns:
        A clean directory name based on the domain
    """
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    
    # Remove www. and port number if present
    if domain.startswith('www.'):
        domain = domain[4:]
    domain = domain.split(':')[0]
    
    # Convert domain to directory name
    return domain.replace('.', '-')

def has_site_updated(url: str, existing_docs_path: Path) -> bool:
    """Check if the documentation site has been updated since last crawl.
    
    Args:
        url: The root URL to check.
        existing_docs_path: Path to the existing docs (latest timestamped directory).
        
    Returns:
        True if the site has been updated, False otherwise.
    """
    success_marker = existing_docs_path / "SUCCESS"
    last_crawl_time = None
    if success_marker.exists():
        last_crawl_time = success_marker.stat().st_mtime  # Last modified time of the marker
    
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        response.raise_for_status()
        
        site_last_modified = response.headers.get('Last-Modified')
        if site_last_modified:
            site_last_modified_dt = datetime.strptime(site_last_modified, '%a, %d %b %Y %H:%M:%S %Z')
            if last_crawl_time and site_last_modified_dt.timestamp() <= last_crawl_time:
                return False
        return True
    except Exception as e:
        logger.warning(f"Could not determine if site has been updated: {e}")
        # Fallback: assume it has not updated
        return False

def check_existing_docs(domain_dir: str) -> Optional[str]:
    """Check if documentation already exists locally.
    
    Args:
        domain_dir: The standardized domain directory name
        
    Returns:
        Path to existing docs if found and valid, None otherwise
    """
    domain_path = Path(domain_dir)
    if domain_path.exists():
        # Find most recent subdirectory by timestamp
        subdirs = [d for d in domain_path.iterdir() if d.is_dir() and not d.name.endswith('.tmp')]
        if subdirs:
            latest = sorted(subdirs)[-1]
            success_marker = latest / "SUCCESS"
            if success_marker.exists():
                return str(latest)
            else:
                logger.warning(f"Latest crawl at {latest} is incomplete or corrupted.")
    return None

def clean_old_caches(domain_dir: Path, max_age_days: int = 30) -> None:
    """Remove cached directories older than max_age_days.
    
    Args:
        domain_dir: Path to the domain directory.
        max_age_days: Maximum age of caches to keep.
    """
    now = datetime.now()
    for subdir in domain_dir.iterdir():
        if subdir.is_dir() and not subdir.name.endswith('.tmp'):
            # Assuming timestamp format YYYYMMDD-HHMMSS
            try:
                timestamp = datetime.strptime(subdir.name, "%Y%m%d-%H%M%S")
                if now - timestamp > timedelta(days=max_age_days):
                    shutil.rmtree(subdir)
                    logger.info(f"Removed old cache: {subdir}")
            except ValueError:
                logger.warning(f"Unexpected directory format: {subdir}")

async def crawl_docs(url: str, output_dir: str, max_pages: int = 500) -> None:
    """Crawl documentation site and save to local directory.
    
    Args:
        url: The root URL to start crawling from
        output_dir: Directory to save markdown files
        max_pages: Maximum number of pages to crawl
        
    Raises:
        RuntimeError: If crawling fails or no pages are crawled successfully
    """
    temp_output_dir = f"{output_dir}.tmp"
    supervisor = CrawlSupervisor(
        max_fetchers=5,
        max_processors=3,
        queue_size=100
    )
    
    try:
        logger.info(f"Starting crawl from {url}")
        structure = await supervisor.start(url, max_pages=max_pages)
        
        # Check if any pages were crawled successfully
        if not structure.pages:
            raise RuntimeError("No pages were crawled successfully - this may not be a documentation site")
        
        # Check if we have enough pages to consider this a docs site
        if len(structure.pages) < 2:
            raise RuntimeError("Not enough pages found - this may not be a documentation site")
        
        logger.info(f"Saving files to temporary directory: {temp_output_dir}")
        supervisor.save_markdown_files(temp_output_dir)
        
        logger.info("\nDocumentation Structure:")
        logger.info(structure.get_tree())
        
        # Create success marker
        success_marker = Path(temp_output_dir) / "SUCCESS"
        success_marker.touch()
        
        # Rename temp directory to final output directory
        shutil.move(temp_output_dir, output_dir)
        logger.info(f"\nDocs saved successfully to: {output_dir}")
        
    except Exception as e:
        logger.error(f"Error during crawl: {e}")
        # Clean up temporary directory if exists
        try:
            if os.path.exists(temp_output_dir):
                shutil.rmtree(temp_output_dir)
        except Exception:
            pass  # Ignore cleanup errors
        raise RuntimeError(f"Crawl failed: {str(e)}")

@click.command()
@click.argument('url')
@click.option('--force', '-f', is_flag=True, help='Force re-crawl even if docs exist locally')
@click.option('--max-pages', '-n', default=100, help='Maximum number of pages to crawl')
@click.option('--max-age-days', '-d', default=30, help='Maximum age of cached docs in days')
def main(url: str, force: bool = False, max_pages: int = 100, max_age_days: int = 30):
    """Crawl documentation from URL and save as markdown files locally.
    
    If documentation for the domain already exists locally, it will be reused
    unless --force flag is specified or the site has been updated.
    """
    try:
        # Get standardized directory name from domain
        domain_dir = get_domain_dir(url)
        domain_path = Path(domain_dir)
        
        # Clean old caches
        if domain_path.exists():
            clean_old_caches(domain_path, max_age_days)
        
        # Check for existing docs unless force flag is used
        if not force:
            existing = check_existing_docs(domain_dir)
            if existing:
                existing_path = Path(existing)
                if not has_site_updated(url, existing_path):
                    logger.info(f"Found existing docs at: {existing}")
                    logger.info("Use --force to re-crawl")
                    return
                else:
                    logger.info("Site has been updated since last crawl")
        
        # Create timestamped output directory
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_dir = os.path.join(domain_dir, timestamp)
        os.makedirs(domain_dir, exist_ok=True)
        
        try:
            # Run the crawler
            asyncio.run(crawl_docs(url, output_dir, max_pages))
            logger.info(f"\nDocs saved successfully to: {output_dir}")
        except Exception as e:
            # Clean up domain directory if empty
            try:
                if os.path.exists(domain_dir) and not os.listdir(domain_dir):
                    os.rmdir(domain_dir)
            except Exception:
                pass  # Ignore cleanup errors
            raise
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise click.ClickException(str(e))

if __name__ == '__main__':
    main() 
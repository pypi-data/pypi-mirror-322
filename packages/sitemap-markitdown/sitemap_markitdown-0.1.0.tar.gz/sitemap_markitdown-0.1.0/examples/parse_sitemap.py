"""
Example script demonstrating how to use the sitemap-markitdown package
to parse both local and remote sitemaps.
"""
import json
from pathlib import Path
import requests
from sitemap_markitdown.sitemap_parser import SitemapParser

def parse_local_sitemap():
    """Parse a local sitemap file"""
    print("\n=== Parsing Local Sitemap ===")
    
    # Read local sitemap file
    sitemap_path = Path(__file__).parent / 'sitemap.xml'
    content = sitemap_path.read_text()
    
    # Parse sitemap
    parser = SitemapParser(content)
    urls = parser.parse()
    
    # Print results
    print(f"Found {len(urls)} URLs:")
    print(json.dumps(urls, indent=2))
    
    # Example of extracting domain
    if urls:
        domain = parser.get_domain(urls[0]['loc'])
        print(f"\nDomain of first URL: {domain}")

def parse_remote_sitemap():
    """Parse a remote sitemap URL"""
    print("\n=== Parsing Remote Sitemap ===")
    
    # Example using a public sitemap
    sitemap_url = "https://www.python.org/sitemap.xml"
    
    try:
        # Fetch remote sitemap
        response = requests.get(sitemap_url)
        response.raise_for_status()
        
        # Parse sitemap
        parser = SitemapParser(response.text)
        urls = parser.parse()
        
        # Print first 3 URLs as example
        print(f"Found {len(urls)} URLs. First 3 URLs:")
        print(json.dumps(urls[:3], indent=2))
        
    except requests.RequestException as e:
        print(f"Error fetching sitemap: {e}")
    except Exception as e:
        print(f"Error parsing sitemap: {e}")

if __name__ == '__main__':
    # Example with local file
    parse_local_sitemap()
    
    # Example with remote URL
    parse_remote_sitemap()

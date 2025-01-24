import pytest
from sitemap_markitdown.sitemap_parser import SitemapParser

def test_parse_complete_sitemap():
    sitemap_content = '''<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url>
            <loc>https://example.com/</loc>
            <lastmod>2024-01-23</lastmod>
            <changefreq>daily</changefreq>
            <priority>1.0</priority>
        </url>
    </urlset>'''
    
    parser = SitemapParser(sitemap_content)
    urls = parser.parse()
    
    assert len(urls) == 1
    assert urls[0]['loc'] == 'https://example.com/'
    assert urls[0]['lastmod'] == '2024-01-23'
    assert urls[0]['changefreq'] == 'daily'
    assert urls[0]['priority'] == '1.0'

def test_parse_minimal_sitemap():
    sitemap_content = '''<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url>
            <loc>https://example.com/</loc>
        </url>
    </urlset>'''
    
    parser = SitemapParser(sitemap_content)
    urls = parser.parse()
    
    assert len(urls) == 1
    assert urls[0]['loc'] == 'https://example.com/'
    assert urls[0]['lastmod'] is None
    assert urls[0]['changefreq'] is None
    assert urls[0]['priority'] is None

def test_parse_multiple_urls():
    sitemap_content = '''<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url>
            <loc>https://example.com/</loc>
        </url>
        <url>
            <loc>https://example.com/about</loc>
        </url>
    </urlset>'''
    
    parser = SitemapParser(sitemap_content)
    urls = parser.parse()
    
    assert len(urls) == 2
    assert urls[0]['loc'] == 'https://example.com/'
    assert urls[1]['loc'] == 'https://example.com/about'

def test_get_domain():
    parser = SitemapParser("")  # Content doesn't matter for domain extraction
    
    # Test basic domain
    assert parser.get_domain('https://example.com') == 'example.com'
    
    # Test domain with path
    assert parser.get_domain('https://example.com/path') == 'example.com'
    
    # Test subdomain
    assert parser.get_domain('https://blog.example.com') == 'blog.example.com'
    
    # Test different protocol
    assert parser.get_domain('http://example.com') == 'example.com'

def test_parse_invalid_xml():
    invalid_content = '''<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url>
            <loc>https://example.com/</loc>
        <!-- Missing closing tags -->
    '''
    
    parser = SitemapParser(invalid_content)
    with pytest.raises(Exception):
        parser.parse()

def test_parse_missing_loc():
    sitemap_content = '''<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url>
            <lastmod>2024-01-23</lastmod>
        </url>
    </urlset>'''
    
    parser = SitemapParser(sitemap_content)
    with pytest.raises(AttributeError):
        parser.parse()

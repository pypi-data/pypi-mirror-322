from lxml import etree
from urllib.parse import urlparse
from typing import List, Dict

class SitemapParser:
    def __init__(self, sitemap_content: str):
        self.sitemap_content = sitemap_content
        self.namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
    def parse(self) -> List[Dict]:
        """Parse sitemap XML and return list of URLs with metadata"""
        root = etree.fromstring(self.sitemap_content.encode('utf-8'))
        
        urls = []
        for url in root.xpath('//ns:url', namespaces=self.namespaces):
            url_data = {
                'loc': url.find('ns:loc', namespaces=self.namespaces).text,
                'lastmod': url.find('ns:lastmod', namespaces=self.namespaces).text if url.find('ns:lastmod', namespaces=self.namespaces) is not None else None,
                'changefreq': url.find('ns:changefreq', namespaces=self.namespaces).text if url.find('ns:changefreq', namespaces=self.namespaces) is not None else None,
                'priority': url.find('ns:priority', namespaces=self.namespaces).text if url.find('ns:priority', namespaces=self.namespaces) is not None else None
            }
            urls.append(url_data)
            
        return urls

    def get_domain(self, url: str) -> str:
        """Extract domain from URL"""
        parsed = urlparse(url)
        return parsed.netloc

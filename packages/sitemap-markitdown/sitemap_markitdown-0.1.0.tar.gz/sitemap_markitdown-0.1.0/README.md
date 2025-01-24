# Sitemap Toolkit

A comprehensive toolkit for parsing sitemaps and converting web content to Markdown format. This tool provides capabilities for both sitemap parsing and bulk web content processing.

## 🚀 Development Setup

1. Clone the repository
2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

3. Run tests:
```bash
pytest
```

## 🧪 Examples

The `examples` directory contains sample code demonstrating how to use the package:

### Local Example
```python
from sitemap_markitdown.sitemap_parser import SitemapParser

# Parse a local sitemap file
with open('sitemap.xml', 'r') as f:
    content = f.read()
    
parser = SitemapParser(content)
urls = parser.parse()
```

### Remote Example
```python
import requests
from sitemap_markitdown.sitemap_parser import SitemapParser

# Parse a remote sitemap
response = requests.get('https://example.com/sitemap.xml')
parser = SitemapParser(response.text)
urls = parser.parse()
```

Check out the complete examples in the `examples` directory:
- `sitemap.xml`: Sample sitemap file
- `parse_sitemap.py`: Script demonstrating both local and remote sitemap parsing

## 🎓 Tutorials

### Quick Start

1. Install the package:
```bash
pip install sitemap-markitdown
```

2. Parse a sitemap:
```bash
sitemap-markitdown parse https://example.com/sitemap.xml --format json
```

### Basic Sitemap Parsing Tutorial

1. Parse a sitemap and save to JSON:
```bash
sitemap-markitdown parse https://example.com/sitemap.xml -o output.json
```

2. Parse a local sitemap file to CSV:
```bash
sitemap-markitdown parse ./local-sitemap.xml --format csv -o urls.csv
```

### Converting Web Pages to Markdown

1. Create a CSV file with URLs (must have a 'loc' column)
2. Run the conversion:
```bash
sitemap-markitdown process-csv --input-csv urls.csv --output-folder markdown_files
```

## 📚 How-to Guides

### How to Parse a Sitemap from URL

To parse a sitemap and extract all URLs with their metadata:

```bash
sitemap-markitdown parse https://example.com/sitemap.xml --format json
```

Options:
- `--format`: Choose between 'json' or 'csv' output (default: json)
- `--output`: Specify output file path
- `--llm-model`: Optionally specify an LLM model for enhanced processing

### How to Process Multiple URLs to Markdown

To convert a list of URLs from a CSV file to Markdown format:

```bash
sitemap-markitdown process-csv \
    --input-csv urls.csv \
    --output-folder markdown_output \
    --output-csv processing_report.csv
```

The CSV file should contain a 'loc' column with the URLs to process.

### How to Customize Output Formats

1. For JSON output with pretty printing:
```bash
sitemap-markitdown parse sitemap.xml --format json
```

2. For CSV output with all metadata:
```bash
sitemap-markitdown parse sitemap.xml --format csv
```

## 📖 Reference

### CLI Commands

#### `parse`
Parse sitemap from file or URL.

Arguments:
- `source`: URL or file path to sitemap

Options:
- `--output, -o`: Output file path
- `--format, -f`: Output format (json/csv)
- `--llm-model`: LLM model for processing

#### `process-csv`
Convert URLs from CSV to Markdown.

Options:
- `--input-csv`: Path to input CSV file (required)
- `--output-folder`: Folder for Markdown files (default: "outputs")
- `--output-csv`: Path for processing report CSV

### Output Formats

#### JSON Format
```json
[
  {
    "loc": "https://example.com/page",
    "lastmod": "2024-01-23",
    "changefreq": "daily",
    "priority": "0.8"
  }
]
```

#### CSV Format
Contains columns:
- loc
- lastmod
- changefreq
- priority

### Dependencies

Core dependencies:
- click: CLI interface
- lxml: XML processing
- markitdown: Web to Markdown conversion
- tqdm: Progress bars

Optional dependencies:
- openai: Enhanced processing capabilities

Development dependencies:
- pytest: Testing framework
- pytest-cov: Code coverage reporting

## 🤔 Explanation

### Project Architecture

The toolkit is built with modularity in mind:

1. **SitemapParser**: Core component for XML parsing
   - Handles both local and remote sitemaps
   - Extracts metadata using XPath
   - Validates against sitemap schema

2. **CLI Interface**: Built with Click
   - Provides intuitive command structure
   - Handles errors gracefully
   - Supports multiple output formats

### Why Use Sitemap Parsing?

Sitemaps are essential for:
- SEO optimization
- Content discovery
- Site structure analysis
- Bulk content processing

This toolkit simplifies these tasks by providing:
- Automated parsing
- Flexible output formats
- Bulk processing capabilities
- Progress tracking

### Design Decisions

1. **Command Structure**
   - Separate commands for parsing and processing
   - Consistent option naming
   - Progress indicators for long operations

2. **Output Formats**
   - JSON for programmatic use
   - CSV for spreadsheet compatibility
   - Markdown for content preservation

3. **Error Handling**
   - Graceful failure modes
   - Detailed error reporting
   - Progress preservation in long operations

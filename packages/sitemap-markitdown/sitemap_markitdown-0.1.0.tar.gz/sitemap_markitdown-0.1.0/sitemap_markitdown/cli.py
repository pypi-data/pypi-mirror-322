import os
import click
import requests
from pathlib import Path
from typing import Optional
from .sitemap_parser import SitemapParser
import csv
from markitdown import MarkItDown
from tqdm import tqdm
import logging

@click.group()
def cli():
    """File and URL processing tools"""
    pass

@cli.command()
@click.argument('source')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--format', '-f', type=click.Choice(['json', 'csv']), default='json', help='Output format')
@click.option('--llm-model', help='LLM model for image processing')
def parse(source: str, output: Optional[str], format: str, llm_model: Optional[str]):
    """Parse sitemap from file or URL"""
    try:
        # Get sitemap content
        if source.startswith('http'):
            response = requests.get(source)
            response.raise_for_status()
            content = response.text
        else:
            content = Path(source).read_text()
        
        # Parse sitemap
        parser = SitemapParser(content)
        urls = parser.parse()
        
        # Generate output
        if format == 'json':
            import json
            result = json.dumps(urls, indent=2)
        elif format == 'csv':
            import csv
            import io
            output_buffer = io.StringIO()
            writer = csv.DictWriter(output_buffer, fieldnames=['loc', 'lastmod', 'changefreq', 'priority'])
            writer.writeheader()
            writer.writerows(urls)
            result = output_buffer.getvalue()
        
        # Output results
        if output:
            Path(output).write_text(result)
            click.echo(f"Saved results to {output}")
        else:
            click.echo(result)
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()




@cli.command()
@click.option('--input-csv', required=True, type=click.Path(exists=True), help='Path to the input CSV file.')
@click.option('--output-folder', default="outputs", type=click.Path(), help='Folder to save the Markdown files.')
@click.option('--output-csv', default=None, type=click.Path(), help='Path to save the output CSV file.')
def process_csv(input_csv, output_folder, output_csv):
    """
    Convert URLs from CSV to Markdown using markitdown and save outputs.
    """
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    md_converter = MarkItDown()
    results = []

    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Read all URLs first to get total count
    with open(input_csv, 'r') as csvfile:
        urls = list(csv.DictReader(csvfile))

    with tqdm(total=len(urls), desc="Processing URLs") as pbar:
        for row in urls:
            url = row['loc']
            output_file_name = url.replace("https://", "").replace("/", "_").strip('_') + ".md"
            output_path = os.path.join(output_folder, output_file_name)

            try:
                # Fetch and verify content
                response = requests.get(url)
                response.raise_for_status()
                
                # Convert content
                result = md_converter.convert(url)
                
                # Verify we got meaningful content
                if not result.text_content or len(result.text_content.strip()) < 10:
                    raise ValueError("Received empty or invalid content")
                
                # Save content
                with open(output_path, 'w', encoding='utf-8') as md_file:
                    md_file.write(result.text_content)
                
                results.append({'url': url, 'output_file': output_path, 'status': 'Success'})
                logger.info(f"Successfully processed {output_path}")
                
            except Exception as e:
                error_msg = f"Error processing {url}: {str(e)}"
                logger.error(error_msg)
                results.append({'url': url, 'output_file': None, 'status': f'Error: {str(e)}'})
            
            pbar.update(1)

    # Write the results to an output CSV file if specified
    if output_csv:
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['url', 'output_file', 'status'])
            writer.writeheader()
            writer.writerows(results)

    click.echo(f"Processing complete. Markdown files are in '{output_folder}'.")
    if output_csv:
        click.echo(f"CSV report saved to '{output_csv}'.")

if __name__ == '__main__':
    cli()

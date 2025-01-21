#!/usr/bin/env python3
import click
import os
import requests
from pathlib import Path
import json
from bs4 import BeautifulSoup

API_URL = os.getenv('QUICKDROP_API_URL', 'https://quickdrop.host/api')

def load_config():
    config_path = Path.home() / '.quickdrop' / 'config.json'
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    print("pointing to: ",API_URL)
    return {'api_url': API_URL}

def save_config(config):
    config_dir = Path.home() / '.quickdrop'
    config_dir.mkdir(exist_ok=True)
    with open(config_dir / 'config.json', 'w') as f:
        json.dump(config, f)

@click.group()
def cli():
    """QuickDrop - Simple HTML deployment tool"""
    pass

def bundle_resources(html_file, verbose):
    """Bundle CSS and JS files into a single HTML file, supporting subdirectories"""
    base_dir = os.path.dirname(os.path.abspath(html_file))
    
    with open(html_file, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # Add QuickDrop branding
    branding_style = soup.new_tag('style')
    branding_style.string = """
        .quickdrop-brand {
            position: fixed;
            top: 12px;
            right: 12px;
            font-family: system-ui, -apple-system, sans-serif;
            text-decoration: none;
            padding: 4px 8px;
            border-radius: 4px;
            background: rgba(0, 0, 0, 0.05);
            color: #666;
            font-weight: 500;
            font-size: 12px;
            transition: opacity 0.2s ease;
            z-index: 9999;
        }
        .quickdrop-brand:hover {
            opacity: 0.8;
        }
    """
    soup.head.append(branding_style)
    
    # Add branding link
    branding_link = soup.new_tag('a', href='/', attrs={'class': 'quickdrop-brand'})
    branding_link.string = 'hosted by QuickDrop'
    if soup.body:
        soup.body.append(branding_link)
    
    # Handle CSS files
    for css_link in soup.find_all('link', rel='stylesheet'):
        href = css_link.get('href')
        if href and not href.startswith(('http://', 'https://', '//')):
            # Handle both absolute and relative paths
            css_path = os.path.normpath(os.path.join(base_dir, href))
            try:
                with open(css_path, 'r') as f:
                    css_content = f.read()
                # Replace any relative URLs in the CSS
                css_dir = os.path.dirname(css_path)
                css_content = replace_css_urls(css_content, css_dir, base_dir)
                # Replace link tag with style tag
                style_tag = soup.new_tag('style')
                style_tag.string = css_content
                css_link.replace_with(style_tag)
                if verbose:
                    click.echo(f'Bundled CSS file: {href}')
            except FileNotFoundError:
                click.echo(f'Warning: Could not find CSS file: {css_path}')

    # Handle JavaScript files
    for script in soup.find_all('script', src=True):
        src = script.get('src')
        if src and not src.startswith(('http://', 'https://', '//')):
            # Handle both absolute and relative paths
            js_path = os.path.normpath(os.path.join(base_dir, src))
            try:
                with open(js_path, 'r') as f:
                    js_content = f.read()
                # Replace src attribute with actual JavaScript
                del script['src']
                script.string = js_content
                if verbose:
                    click.echo(f'Bundled JavaScript file: {src}')
            except FileNotFoundError:
                click.echo(f'Warning: Could not find JavaScript file: {js_path}')

    return str(soup)

def replace_css_urls(css_content, css_dir, base_dir):
    """Replace relative URLs in CSS with data URIs or adjust paths"""
    import re
    import base64
    import mimetypes
    
    def replace_url(match):
        url = match.group(1)
        # Skip data URIs, absolute URLs, and hash references
        if url.startswith(('data:', 'http://', 'https://', '#', '/')):
            return f'url({url})'
            
        # Resolve the file path
        file_path = os.path.normpath(os.path.join(css_dir, url))
        if os.path.exists(file_path):
            # For images, convert to data URI
            mime_type = mimetypes.guess_type(file_path)[0]
            if mime_type and mime_type.startswith('image/'):
                with open(file_path, 'rb') as f:
                    data = base64.b64encode(f.read()).decode('utf-8')
                return f'url(data:{mime_type};base64,{data})'
                
        # If file doesn't exist or isn't an image, return original URL
        return f'url({url})'
    
    # Find and replace all url() references
    return re.sub(r'url\([\'"]?([^\'"\)]+)[\'"]?\)', replace_url, css_content)

@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('-v', '--verbose', is_flag=True, help='Show detailed output')
def push(file, verbose):
    """Push an HTML file to QuickDrop"""
    config = load_config()
    if 'access_token' not in config:
        click.echo('Please login first using: quickdrop login')
        return

    try:
        # Bundle the HTML with its resources
        if verbose:
            click.echo('Bundling resources...')
        html_content = bundle_resources(file, verbose)
        
        filename = os.path.basename(file)
        api_url = config.get('api_url', API_URL)
        headers = {'Authorization': f'Bearer {config["access_token"]}'}
        
        if verbose:
            click.echo(f'Making request to: {api_url}/deployments/')
            click.echo(f'Headers: {headers}')
            click.echo(f'Filename: {filename}')
        
        response = requests.post(
            f'{api_url}/deployments/',
            json={
                'html_content': html_content,
                'filename': filename
            },
            headers=headers
        )
        
        if verbose:
            click.echo(f'Response status: {response.status_code}')
            
        if response.status_code == 201:
            data = response.json()
            click.echo('Deployment successful!')
            click.echo('Your site is live at: ')
            click.echo(click.style(data['url'], fg='blue', underline=True), nl=False)
            click.echo(' (CMD+Click to open)')
        else:
            click.echo(f'Deployment failed with status {response.status_code}')
            click.echo(f'Error: {response.text}')
    except Exception as e:
        click.echo(f'Error occurred: {str(e)}')

@cli.command()
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def login(username, password):
    """Login to QuickDrop"""
    config = load_config()
    api_url = config.get('api_url', API_URL)
    print("connecting to: ", API_URL)
    
    try:
        response = requests.post(
            f'{api_url}/token/',
            json={'username': username, 'password': password}
        )
        
        if response.status_code == 200:
            data = response.json()
            config['access_token'] = data['access']
            config['refresh_token'] = data['refresh']
            save_config(config)
            click.echo('Login successful!')
        else:
            if 'html' in response.headers.get('content-type', ''):
                click.echo(f'Error: Server returned status {response.status_code}')
            else:
                click.echo(f'Login failed: {response.text}')
    except Exception as e:
        click.echo(f'Error connecting to server: {str(e)}')

@cli.command()
@click.argument('site_hash')
def versions(site_hash):
    """List versions for a specific deployment"""
    config = load_config()
    if 'access_token' not in config:
        click.echo('Please login first using: quickdrop login')
        return

    try:
        api_url = config.get('api_url', API_URL)
        headers = {'Authorization': f'Bearer {config["access_token"]}'}
        response = requests.get(f'{api_url}/deployments/{site_hash}/versions/', headers=headers)
        
        if response.status_code == 200:
            versions = response.json()
            if not versions:
                click.echo('No versions found.')
                return
            
            click.echo('\nVersions:')
            for version in versions:
                click.echo(f"\n• Version {version['version']}")
                click.echo(f"  Created: {version['created_at']}")
                if version['is_current']:
                    click.echo("  Status: Current version")
        else:
            click.echo('Failed to fetch versions.')
    except Exception as e:
        click.echo(f'Error connecting to server: {str(e)}')

@cli.command()
@click.argument('site_hash')
@click.argument('version', type=int)
def rollback(site_hash, version):
    """Rollback to a specific version"""
    config = load_config()
    if 'access_token' not in config:
        click.echo('Please login first using: quickdrop login')
        return

    try:
        api_url = config.get('api_url', API_URL)
        headers = {'Authorization': f'Bearer {config["access_token"]}'}
        response = requests.post(
            f'{api_url}/deployments/{site_hash}/rollback/{version}/',
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            click.echo(f"Successfully rolled back to version {version}")
            click.echo('Your site is now live at: ')
            click.echo(click.style(data['url'], fg='blue', underline=True), nl=False)
            click.echo(' (CMD+Click to open)')
        else:
            if response.status_code == 404:
                click.echo(f'Version {version} not found')
            else:
                click.echo(f'Failed to rollback: {response.text}')
    except Exception as e:
        click.echo(f'Error: {str(e)}')

@cli.command()
def list():
    """List all deployments"""
    config = load_config()
    if 'access_token' not in config:
        click.echo('Please login first using: quickdrop login')
        return

    try:
        api_url = config.get('api_url', API_URL)
        headers = {'Authorization': f'Bearer {config["access_token"]}'}
        response = requests.get(f'{api_url}/deployments/', headers=headers)
        
        if response.status_code == 200:
            sites = response.json()
            if not sites:
                click.echo('No deployments found.')
                return
                
            click.echo('\nYour deployments:')
            for site in sites:
                click.echo("\n• URL: ", nl=False)
                click.echo(click.style(site['url'], fg='blue', underline=True))
                click.echo(f"  ID: {site['site_hash']}  (use this for versions/rollback)")
                if 'filename' in site and site['filename']:
                    click.echo(f"  File: {site['filename']}")
                if 'created_at' in site:
                    click.echo(f"  Created: {site['created_at']}")
        else:
            click.echo('Failed to fetch deployments.')
            if response.text:
                click.echo(f'Error: {response.text}')
    except KeyError as e:
        click.echo(f'Unexpected response format: missing field {str(e)}')
    except Exception as e:
        click.echo(f'Error connecting to server: {str(e)}')

@cli.command()
def status():
    """Show current connection status and server information"""
    config = load_config()
    api_url = config.get('api_url', API_URL)
    
    click.echo("\nQuickDrop Status")
    click.echo("---------------")
    click.echo(f"Server: {api_url}")
    
    if 'access_token' not in config:
        click.echo(click.style("Status: Not logged in", fg='yellow'))
        click.echo("\nTo login, use: quickdrop login")
        return
    
    try:
        # Try to make a request to verify the token
        headers = {'Authorization': f'Bearer {config["access_token"]}'}
        response = requests.get(f'{api_url}/deployments/', headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            click.echo(click.style("Status: Connected", fg='green'))
            if user_data:
                click.echo(f"Active deployments: {len(user_data)}")
        else:
            click.echo(click.style("Status: Token expired or invalid", fg='red'))
            click.echo("\nPlease login again using: quickdrop login")
            
    except Exception as e:
        click.echo(click.style("Status: Connection error", fg='red'))
        click.echo(f"Error: {str(e)}")

@cli.command()
def summary():
    """Show deployment analytics summary"""
    config = load_config()
    if 'access_token' not in config:
        click.echo('Please login first using: quickdrop login')
        return
    try:
        api_url = config.get('api_url', API_URL)
        headers = {'Authorization': f'Bearer {config["access_token"]}'}
        response = requests.get(f'{api_url}/analytics/summary/', headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            click.echo(f"\nAnalytics Summary for user: {data['user']}")
            click.echo("\nDeployment Statistics:")
            
            for deployment in data['deployments_summary']:
                click.echo("\n• ", nl=False)
                click.echo(click.style(deployment['filename'], fg='blue'))
                click.echo(f"  Site ID: {deployment['site']}")
                click.echo(f"  URL: ", nl=False)
                click.echo(click.style(deployment['url'], fg='blue', underline=True))
                click.echo(f"  Views: {deployment['view_count']}")
                
        else:
            click.echo('Failed to fetch analytics summary.')
            if response.text:
                click.echo(f'Error: {response.text}')
    except KeyError as e:
        click.echo(f'Unexpected response format: missing field {str(e)}')
    except Exception as e:
        click.echo(f'Error connecting to server: {str(e)}')

@cli.command()
@click.argument('site_hash')
@click.option('--force', is_flag=True, help='Skip confirmation prompt')
def delete(site_hash, force):
    """Permanently delete a deployment and all its versions"""
    config = load_config()
    if 'access_token' not in config:
        click.echo('Please login first using: quickdrop login')
        return

    try:
        if not force:
            if not click.confirm(f'Are you sure you want to permanently delete site {site_hash}? This cannot be undone'):
                click.echo('Operation cancelled.')
                return

        api_url = config.get('api_url', API_URL)
        headers = {'Authorization': f'Bearer {config["access_token"]}'}
        response = requests.delete(
            f'{api_url}/deployments/{site_hash}/purge/',
            headers=headers
        )
        
        if response.status_code == 200:
            click.echo(click.style('✔ ', fg='green') + 'Site deleted successfully')
        elif response.status_code == 404:
            click.echo(click.style('✘ ', fg='red') + 'Site not found')
        else:
            click.echo(click.style('✘ ', fg='red') + f'Failed to delete site: {response.text}')
    except Exception as e:
        click.echo(f'Error: {str(e)}')




if __name__ == '__main__':
    cli()
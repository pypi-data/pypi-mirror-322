# QuickDrop CLI

QuickDrop is a command-line tool that simplifies web deployment by automatically bundling and deploying HTML projects. It handles resource bundling, asset optimization, and versioning in one simple command.

## Features

- **One-Command Deployment**: Deploy your entire web project with a single command
- **Automatic Resource Bundling**: CSS and JavaScript files are automatically inlined
- **Asset Optimization**: Images in CSS are converted to data URIs
- **Version Management**: Track deployment versions with built-in versioning
- **Rollback Support**: Easy rollback to previous versions if needed

## Installation

```bash
pip install quickdrop-cli
```

## Quick Start

1. Login to QuickDrop:
```bash
quickdrop login
```

2. Deploy your HTML file:
```bash
quickdrop push index.html
```

## Commands

- `quickdrop login` - Authenticate with QuickDrop
- `quickdrop push <file>` - Deploy an HTML file
- `quickdrop list` - List all deployments
- `quickdrop versions <site_hash>` - List versions for a deployment
- `quickdrop rollback <site_hash> <version>` - Rollback to a specific version

## Options

- `-v, --verbose` - Show detailed output during deployment
- `--help` - Show help message and exit

## Example

```bash
# Deploy an HTML file with verbose output
quickdrop push index.html -v

# List all versions of a deployment
quickdrop versions abc123

# Rollback to version 2
quickdrop rollback abc123 2
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
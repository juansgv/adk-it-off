# ADK IT Office Assistant

## Overview
ADK IT Office Assistant is a specialized AI agent built using Google's AI Development Kit (ADK). This tool is designed to help with various IT office tasks, providing automated assistance for common technical procedures.

## Prerequisites

- Python 3.10 or higher
- pip (Python package installer)
- Git (for version control)
- Access to Google ADK (AI Development Kit)

## Installation

Follow these steps to set up your development environment:

### 1. Set Up Python Environment

First, remove any existing virtual environment (if present):

```bash
rm -rf .venv
```

Create a new virtual environment with Python 3.10:

```bash
python3.10 -m venv .venv
```

### 2. Activate the Virtual Environment

```bash
source .venv/bin/activate
```

Verify activation by checking:

```bash
python --version   # Should output: Python 3.10.x
which python       # Should point to: .../adk_it_office/.venv/bin/python
```

### 3. Install Dependencies

Update pip and install Google ADK:

```bash
pip install --upgrade pip
pip install google-adk
```

### 4. Verify Package Structure

Ensure your agent folder is properly set up as a Python package. This project should already include the necessary `__init__.py` file.

## Usage

### Starting the Web UI

You can launch the ADK web interface using either of these commands:

```bash
.venv/bin/adk web
```

Or alternatively:

```bash
python -m google.adk.cli web
```

The web UI provides a graphical interface for interacting with and testing your AI agent.

## Development

More information about development procedures can be found in the DOCUMENTATION.md file.

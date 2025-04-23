# GETTING STARTED

# 1. Remove any leftover venv
rm -rf .venv

# 2. Create a new venv with Python 3.10
python3.10 -m venv .venv

# 3. Activate it
source .venv/bin/activate
# confirm:
python --version   # → Python 3.10.x
which python       # → …/adk_it_office/.venv/bin/python

# 4. Install ADK
pip install --upgrade pip
pip install google-adk

# 5. Ensure your agent folder is a package
# (you already committed __init__.py, so this is done)

# 6a. Launch the web UI
.venv/bin/adk web
# or
python -m google.adk.cli web

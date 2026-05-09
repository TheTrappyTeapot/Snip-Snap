# Snip-Snap Documentation

This directory contains the Sphinx documentation for the Snip-Snap project.

## Structure

```
docs/
├── conf.py                 # Sphinx configuration
├── requirements.txt        # Python dependencies for building docs
├── source/
│   ├── index.rst          # Main documentation index
│   └── files/             # Auto-generated code documentation
│       └── app/           # Application module documentation
└── _build/                # Build output (generated)
```

## Building Locally

### Prerequisites
```bash
pip install -r requirements.txt
```

### Build HTML Documentation
```bash
cd docs
make html
```

The built documentation will be in `docs/_build/html/`

## Publishing to ReadTheDocs

### Step 1: Set Up on ReadTheDocs

1. Go to https://readthedocs.org
2. Sign in with your GitHub account (or create an account)
3. Click "Import a Project"
4. Select your repository: `TheTrappyTeapot/Snip-Snap`
5. Click "Create"

### Step 2: Configure Build Settings

ReadTheDocs will automatically detect the `.readthedocs.yml` file in your repository, which configures:
- Python version (3.11)
- Documentation source (docs/)
- Build tool (Sphinx)
- Dependencies (from `requirements.txt` and `docs/requirements.txt`)

### Step 3: Get Your Documentation Link

After the first build completes, your documentation will be available at:
```
https://snip-snap.readthedocs.io/
```

## Adding Link to Repository

Add this to your repository's **README.md**:

```markdown
## Documentation

Read the full documentation at: [Snip-Snap on ReadTheDocs](https://snip-snap.readthedocs.io/)
```

Or add a badge:

```markdown
[![Documentation Status](https://readthedocs.org/projects/snip-snap/badge/?version=latest)](https://snip-snap.readthedocs.io/?badge=latest)
```

## GitHub Integration

ReadTheDocs automatically:
- Builds documentation on every push to the default branch
- Displays build status on your GitHub repository
- Creates webhooks for automatic updates

## Project Documentation Files

The documentation is organized by code module:

- **app/**: Core application modules
  - `__init__.py` - Package initialization
  - `api.py` - API endpoints
  - `auth.py` - Authentication logic
  - `routes.py` - Flask routes
  - `db.py` - Database operations
  - `handy_scripts/` - Utility scripts
  
- **static/**: Frontend assets
  - `css/`: Stylesheets (components and pages)
  - `js/`: JavaScript modules (components, features, and pages)
  
- **templates/**: HTML templates
  - Jinja2 templates for page rendering

## Troubleshooting

### Documentation not building?
- Check `.readthedocs.yml` configuration
- Verify `docs/requirements.txt` has all necessary packages
- Check the build logs on ReadTheDocs dashboard

### Styles not loading?
- ReadTheDocs uses `sphinx-rtd-theme` by default
- If you want a different theme, update `conf.py`

### Module documentation not showing?
- Ensure your code has docstrings
- Update `conf.py` extensions if needed

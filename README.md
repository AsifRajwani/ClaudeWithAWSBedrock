# Python Starter Project

A clean starter template for Python development that works with **any editor or IDE**. Supports both running Python files and Jupyter notebooks. VS Code (and forks like Cursor, Antigravity, Kiro, etc.) users get additional conveniences like auto-format on save. Follow the setup instructions below to get started.

Sample Python file (`src/main.py`), Jupyter notebooks (in `src/`), and a test (`tests/test_main.py`) are provided.

## Features

- **uv** for fast dependency management and virtual environment setup
- Pytest for testing
- Black + Ruff for code formatting and linting
- **VS Code bonus:** pre-configured settings for auto-format on save (works with any VS Code fork too)

## Getting started from the starter

This repository is intended to be a **starter template**. Pick the option that applies to you:

### Option A: Fork (for anyone who does not own this repo)

1. **Fork** this repository on GitHub and give the fork whatever name you like.
2. Clone your fork locally:
   ```bash
   git clone git@github.com:you/your-fork.git
   cd your-fork
   ```
3. Follow the **Setup** section below and verify everything works.

### Option B: Use as a template (for the repo owner or when forking isn't possible)

GitHub doesn't allow you to fork your own repo. Instead, create a new repository from this one:

1. Create a **new empty repo** on GitHub (e.g. `my-new-project`).
2. Clone this starter locally and re-point it to your new repo:
   ```bash
   git clone git@github.com:asifrajwani/PythonStarter.git my-new-project
   cd my-new-project
   git remote set-url origin git@github.com:you/my-new-project.git
   git push -u origin main
   ```
3. Follow the **Setup** section below and verify everything works.

> **Tip:** Both options preserve the commit history as the base of your project.


## Prerequisites

- **Python 3.11+** (or let `uv` install it for you)
- **uv** — install it if you don't have it: https://docs.astral.sh/uv/getting-started/installation/

## Setup

```bash
# verify uv is installed
uv --version

# (optional) update uv to the latest version
uv self update

# (optional) pin a specific Python version if you have a preference
# uv python pin 3.11

# install dependencies and create the virtual environment
uv sync
```

> **Tip:** `pyproject.toml` now contains a `requires-python` field (>=3.11) so you won't see the warning about missing Python requirements when running commands like `uv run python -m pytest`. We default to Python 3.11 or newer; feel free to update this value in `pyproject.toml` if your project requires a different minimum version.

## Testing the Setup

After setting up the environment you can verify everything is working by running both the regular Python code and the notebooks.

### Running the Python Program

```bash
# execute the main script using uv-managed Python
uv run python src/main.py
```

You should see any output defined in `main.py`. Running through `uv` ensures the correct Python version from the pinned environment is used and mirrors how other commands (including notebooks) run.

### Working with Notebooks

The `src/` directory contains sample Jupyter notebooks (e.g. `simple_notebook.ipynb`). You can run them from any environment that supports Jupyter:

- **VS Code / forks:** Open the notebook in the built-in Jupyter interface. Use the Run Cell controls or execute the whole notebook via the command palette.
- **Any editor / command line:** Launch Jupyter and open the notebook in your browser:
  ```bash
  uv run jupyter notebook src/simple_notebook.ipynb
  ```

Each notebook uses the same environment as the Python code, so dependencies are shared.

> **Selecting the kernel:**
>
> Whether you're using VS Code or Jupyter in the browser, select the Python interpreter associated with this project (it will usually show the path under `.venv` or similar). This ensures cells execute with the same dependencies as `uv run` commands.

### Running Tests

We provide a simple `pytest` test for the starter project. Execute the tests through uv to ensure the correct environment:

```bash
# from the workspace root
uv run python -m pytest
```

This will run `tests/test_main.py` and any additional tests you add later.

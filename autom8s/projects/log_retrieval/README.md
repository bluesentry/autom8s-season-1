# Log Retrieval

Retrieve GitHub workflow logs and save them to a (blob) database.

## Usage

By supplying a GitHub token, you can retrieve logs for a specific workflow run, a subset, or all runs in one or many repositories. Logfiles are extracted as .txt files and can be optionally saved to a database.

## Setup

### OS

This code is compatible with Linux and macOS. Windows usage is unverified.

### Installation

For easy setup, run the following command:

```bash
bash setup_env.sh {-e dev}  # optionally create a development environment
```

This will create a virtual environment and install the required dependencies.

### Contributing

Ensure the development dependencies are are installed.

```bash
pip install -r requirements-dev.txt
```

Dependencies only need to be updated in `pyrpoject.toml`. Propogate version changes to requirements files by running the following command:

```bash
nox -s update_requirements
```

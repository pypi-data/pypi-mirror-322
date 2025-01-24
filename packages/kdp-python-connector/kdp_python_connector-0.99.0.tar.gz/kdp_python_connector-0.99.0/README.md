# kdp_connector

## Setting Up the Project and Running Tests

To build and test the project locally, follow these steps:

### Prerequisites

Ensure you have the following installed on your system:
- **Python 3.9.x, 3.10.x or 3.11.x** (specific version required for the project)
- **Poetry** (version 2.x or later)

If Poetry is not installed, you can install it using the official installer:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Verify the installation:
```bash
poetry --version
```

### Set Up the Poetry Environment

1. Install project dependencies using Poetry:
   ```bash
   poetry install
   ```

2. Use the specific Python version required for the project (if not already configured):
   ```bash
   poetry env use $(which python3.10)
   ```

### Running Tests

Run the tests using `pytest`:
```bash
poetry run pytest
```

For detailed output, you can add the `-vv` flag:
```bash
poetry run pytest -vv
```

### Troubleshooting

- If `poetry install` fails, ensure your Python version matches the required version (ex. 3.10.x).
- If you encounter issues with missing dependencies or errors related to architecture, ensure your Python installation and dependencies are compatible with your system architecture (e.g., arm64 vs x86_64).

## Release

## Examples
For code examples using kdp-python-connector see github https://github.com/Koverse/kdp-examples

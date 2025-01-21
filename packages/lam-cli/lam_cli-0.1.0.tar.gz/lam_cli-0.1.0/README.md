# lam
Lam is a data transformation tool for Laminar that supports both `jq` and JavaScript transformations using Bun.

## Quickstart
Install the dependencies:
```bash
# For JQ support
brew install jq  # or sudo apt-get install jq

# For JavaScript support
curl -fsSL https://bun.sh/install | bash

make setup
```

Run the CLI tool:
```bash
make cli ARGS="run <program> <input> [--language jq|js]"
```

## Features
- JQ transformations (default)
- JavaScript transformations with Bun runtime
- Built-in utilities (lodash, date-fns)
- Resource monitoring and limits
- Detailed execution statistics
- Secure execution environment

## Examples

### JQ Transform
```bash
make cli ARGS="run examples/transform.jq data.json"
```

### JavaScript Transform
```bash
make cli ARGS="run examples/transform.js data.json --language js"
```

Example JavaScript transform:
```javascript
(input) => {
    // Lodash available as _
    return _.map(input.data, item => ({
        value: item.value * 2
    }));
}
```

## Installation

### Docker Installation
```dockerfile
# Install lam-cli
RUN pip3 install git+https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/user/project.git@{version}

# Install dependencies
RUN apt-get update && apt-get install -y jq
RUN curl -fsSL https://bun.sh/install | bash
```

### Manual Setup
Create a virtual environment and install dependencies:
```bash
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```

## Usage
```bash
# Basic usage
python3 ./lam/lam.py run <program> <input>

# With JavaScript
python3 ./lam/lam.py run script.js data.json --language js

# Full options
python3 ./lam/lam.py run <program> <input> \
    --language [jq|js] \
    --workspace_id <id> \
    --flow_id <id> \
    --execution_id <id> \
    [--as-json]
```

## Resource Limits
- Maximum input size: 10MB
- Execution timeout: 5 seconds
- Memory limits enabled
- Disk space monitoring

## Security
- Sandboxed JavaScript execution
- Network access disabled
- Limited global scope
- Resource monitoring
- Secure dependency management

## Logging and Monitoring
- Execution statistics (duration, memory usage)
- Detailed error tracking
- PostHog analytics integration
- Log file generation

## Development
```bash
# Run all tests
make test

# Run specific test suite
make test-jq
make test-js
make test-js-edge-cases

# Run single test
make test-single TEST=test/js/example.js DATA=test/data/input.json
```

## Releases
Update version in `setup.py`:
```python
setup(
    name="lam-cli",
    version="0.0.<x>",
    ...
)
```

Create and push tag:
```bash
git tag v<version>-<increment>
git push origin v<version>-<increment>
```

## Dependencies
Update dependencies:
```bash
pip3 install <package>
pip3 freeze > requirements.txt
```
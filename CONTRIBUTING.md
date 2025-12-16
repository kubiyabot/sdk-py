# Contributing to Kubiya SDK

Thank you for your interest in contributing to Kubiya SDK! We welcome contributions from the community and are grateful for your support.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Community](#community)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to support@kubiya.ai.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up your development environment
4. Create a new branch for your changes
5. Make your changes
6. Push your changes to your fork
7. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.9 or higher
- pip or poetry for package management
- Docker (for running containerized workflows)
- Git

### Setting Up Your Environment

1. Clone your fork:
```bash
git clone https://github.com/YOUR_USERNAME/sdk-py.git
cd sdk-py
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e ".[dev]"
```

4. Set up pre-commit hooks (optional but recommended):
```bash
pre-commit install
```

### Running Tests

Run the test suite:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=kubiya --cov-report=html
```

Run linting:
```bash
ruff check .
black --check .
mypy kubiya
```

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When you create a bug report, include as many details as possible using our [bug report template](.github/ISSUE_TEMPLATE/bug_report.md).

**Great bug reports include:**
- A quick summary and/or background
- Steps to reproduce
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening)
- Sample code if applicable

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, use our [feature request template](.github/ISSUE_TEMPLATE/feature_request.md) and include:

- A clear and descriptive title
- A detailed description of the proposed enhancement
- Examples of how the feature would be used
- Why this enhancement would be useful

### Your First Code Contribution

Unsure where to begin? Look for issues labeled:
- `good first issue` - Good for newcomers
- `help wanted` - Issues where we need community help

### Pull Requests

1. **Create a branch** for your changes:
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

2. **Make your changes** following our coding standards

3. **Write or update tests** for your changes

4. **Update documentation** as needed

5. **Commit your changes** with clear, descriptive messages:
```bash
git commit -m "Add feature: brief description"
```

6. **Push to your fork**:
```bash
git push origin feature/your-feature-name
```

7. **Open a Pull Request** against the `main` branch

## Pull Request Process

1. Ensure your code passes all tests and linting checks
2. Update the CHANGELOG.md with details of your changes
3. Update the README.md if you've added new features or changed existing ones
4. Update relevant documentation in the `docs/` directory
5. Your PR will be reviewed by maintainers who may request changes
6. Once approved, a maintainer will merge your PR

### PR Checklist

- [ ] Tests pass locally
- [ ] Code follows project style guidelines
- [ ] Documentation has been updated
- [ ] CHANGELOG.md has been updated
- [ ] Commit messages are clear and descriptive
- [ ] PR description clearly describes the changes

## Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

- **Formatting**: We use `black` with default settings
- **Linting**: We use `ruff` for fast Python linting
- **Type Hints**: Use type hints for all public functions and methods
- **Docstrings**: Follow Google-style docstrings

Example:
```python
def execute_workflow(
    workflow_name: str,
    params: dict[str, Any] | None = None,
) -> WorkflowExecution:
    """Execute a workflow with the given parameters.

    Args:
        workflow_name: The name of the workflow to execute
        params: Optional parameters to pass to the workflow

    Returns:
        A WorkflowExecution object representing the running workflow

    Raises:
        WorkflowNotFoundError: If the workflow doesn't exist
        ValidationError: If the parameters are invalid
    """
    pass
```

### Code Organization

- Keep functions and methods focused and small
- Use meaningful variable and function names
- Avoid deep nesting (max 3-4 levels)
- Add comments for complex logic, but prefer self-documenting code

### Import Organization

Organize imports in the following order:
1. Standard library imports
2. Related third-party imports
3. Local application/library imports

Use `isort` to automatically organize imports:
```bash
isort kubiya/
```

## Testing

### Writing Tests

- Write tests for all new features and bug fixes
- Aim for high test coverage (>80%)
- Use descriptive test names that explain what is being tested
- Follow the Arrange-Act-Assert pattern

Example:
```python
def test_workflow_execution_with_valid_params():
    # Arrange
    workflow = Workflow("test-workflow")
    params = {"key": "value"}

    # Act
    result = workflow.execute(params)

    # Assert
    assert result.status == "success"
    assert result.params == params
```

### Test Organization

- Place tests in the `tests/` directory
- Mirror the structure of the `kubiya/` package
- Use `pytest` fixtures for common setup

## Documentation

### Code Documentation

- Add docstrings to all public modules, classes, and functions
- Keep docstrings up-to-date when changing code
- Include examples in docstrings when helpful

### User Documentation

- Update README.md for user-facing changes
- Add or update docs in the `docs/` directory
- Include code examples where appropriate
- Update the API reference documentation

### Writing Style

- Use clear, concise language
- Write in present tense
- Use active voice
- Include code examples
- Add links to related documentation

## Community

### Getting Help

- Check the [documentation](https://docs.kubiya.ai)
- Search [existing issues](https://github.com/kubiyabot/sdk-py/issues)
- Ask questions in GitHub Discussions
- Join our community channels

### Communication

- Be respectful and inclusive
- Assume good intentions
- Provide constructive feedback
- Be patient with newcomers

## Recognition

Contributors will be recognized in:
- The project's README.md
- Release notes
- The contributors list on GitHub

## License

By contributing to Kubiya SDK, you agree that your contributions will be licensed under the AGPL-3.0 License.

## Questions?

If you have questions about contributing, please:
- Open a GitHub Discussion
- Contact us at support@kubiya.ai
- Check our [documentation](https://docs.kubiya.ai)

Thank you for contributing to Kubiya SDK!

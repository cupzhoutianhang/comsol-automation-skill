# Contributing to COMSOL Automation Skill

Thank you for your interest in contributing to the COMSOL Automation Skill developed by Zhou Tianhang at China University of Petroleum (Beijing)! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Documentation](#documentation)
- [Issue Reporting](#issue-reporting)
- [Feature Requests](#feature-requests)

## Code of Conduct

### Our Pledge

The COMSOL Automation Skill project by Zhou Tianhang at China University of Petroleum (Beijing) is committed to providing a friendly, safe, and welcoming environment for all contributors. We expect all participants to:

- Be respectful and inclusive
- Use welcoming and inclusive language
- Be collaborative
- Accept constructive criticism gracefully
- Focus on what is best for the community

### Expected Behavior

- Use inclusive language
- Respect differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on community goals
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Personal or political attacks
- Public or private harassment
- Publishing others' private information
- Other conduct deemed inappropriate

## Getting Started

1. **Fork the Repository**
   ```bash
   git clone https://github.com/your-username/comsol-automation-skill.git
   cd comsol-automation-skill
   ```

2. **Set Up Development Environment**
   ```bash
   # Install development dependencies
   pip install -r requirements.txt
   pip install pytest pytest-cov black flake8
   ```

3. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Required Software

- **Python 3.8+**
- **COMSOL Multiphysics 6.0+** (for testing)
- **Git**
- **Text Editor/IDE** (VS Code, PyCharm, etc.)

### Environment Configuration

1. **COMSOL Server Setup**
   ```bash
   # Ensure COMSOL server is properly configured
   # Test connection before running automated tests
   python -c "import mph; print('COMSOL connection available')"
   ```

2. **Development Dependencies**
   ```bash
   # Install all required packages
   pip install -r requirements.txt
   
   # Install development tools
   pip install black flake8 pytest pytest-cov sphinx
   ```

3. **Pre-commit Hooks (Optional)**
   ```bash
   # Install pre-commit
   pip install pre-commit
   
   # Create .pre-commit-config.yaml
   cat > .pre-commit-config.yaml << EOF
   repos:
   - repo: https://github.com/psf/black
     rev: 22.3.0
     hooks:
     - id: black
       language_version: python3.8
   - repo: https://github.com/pycqa/flake8
     rev: 4.0.1
     hooks:
     - id: flake8
   EOF
   
   pre-commit install
   ```

## Coding Standards

### Python Style Guide

We follow **PEP 8** with some modifications:

1. **Line Length**: Maximum 100 characters
2. **Imports**: Grouped in the following order:
   - Standard library imports
   - Third-party imports
   - Local application imports
3. **Naming Conventions**:
   - Classes: `PascalCase`
   - Functions/Variables: `snake_case`
   - Constants: `UPPER_SNAKE_CASE`
   - Private: `_single_leading_underscore`

### Code Formatting

Use **Black** for automatic formatting:
```bash
black skills/ examples/ tests/
```

### Linting

Use **flake8** for code quality:
```bash
flake8 skills/ examples/ tests/
```

### Documentation

1. **Docstrings**: Use Google style docstrings
   ```python
   def function_name(param1: str, param2: int) -> bool:
       """Brief description of the function.

       Extended description providing more details about the function,
       its purpose, and usage examples.

       Args:
           param1: Description of param1
           param2: Description of param2

       Returns:
           Description of return value

       Raises:
           ValueError: Description of when this exception is raised
       """
   ```

2. **Type Hints**: Use type hints for all function parameters and return values

3. **Comments**: Write clear, concise comments explaining "why" not "what"

### Error Handling

1. **Specific Exceptions**: Catch specific exceptions rather than generic `Exception`
2. **Custom Exceptions**: Create custom exception classes for domain-specific errors
3. **Logging**: Use Python's logging module instead of print statements

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=skills.comsol_automated_modeling

# Run specific test file
pytest tests/test_parameter_handler.py

# Run tests in verbose mode
pytest -v
```

### Writing Tests

1. **Test Structure**: Use the Arrange-Act-Assert pattern
2. **Test Naming**: Name tests descriptively (e.g., `test_validate_parameters_with_invalid_input`)
3. **Mocking**: Use `unittest.mock` for external dependencies (COMSOL connection)
4. **Fixtures**: Use pytest fixtures for common test setup

### Test Coverage

- Aim for **80%+** test coverage
- Focus on critical functionality
- Include both positive and negative test cases

### Integration Tests

For tests requiring COMSOL:

```python
import pytest
from unittest.mock import Mock, patch

@pytest.mark.integration  # Mark as integration test
@patch('mph.Client')  # Mock COMSOL connection
def test_comsol_integration(mock_client):
    # Test code here
    pass
```

## Pull Request Process

1. **Before Submitting**
   - Update your fork with the latest changes from main
   - Run all tests and ensure they pass
   - Run code formatting and linting
   - Update documentation if needed
   - Add tests for new functionality

2. **Pull Request Description**
   - Clear, descriptive title
   - Detailed description of changes
   - Reference any related issues
   - Include screenshots for UI changes
   - List any breaking changes

3. **Code Review**
   - Address all review comments
   - Keep changes focused and minimal
   - Do not mix multiple features in one PR

4. **Merge Criteria**
   - All tests pass
   - Code review approved
   - No conflicts with main branch
   - Documentation updated

## Documentation

### Updating Documentation

1. **API Documentation**: Update `docs/API_REFERENCE.md` for API changes
2. **Usage Guide**: Update `docs/USAGE_GUIDE.md` for new features
3. **README**: Update main README for significant changes
4. **Examples**: Add or update examples in `examples/` directory

### Documentation Standards

- Clear, concise language
- Code examples for all features
- Step-by-step instructions for complex workflows
- Screenshots for visual elements
- Regular updates to reflect code changes

## Issue Reporting

### Creating Issues

1. **Search First**: Check if the issue already exists
2. **Use Templates**: Fill out the appropriate issue template
3. **Be Specific**: Include:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs. actual behavior
   - Environment details (OS, Python version, COMSOL version)
   - Error messages and stack traces

### Issue Labels

- **bug**: Something isn't working
- **enhancement**: New feature or improvement
- **documentation**: Documentation issues
- **help-wanted**: Extra attention needed
- **good-first-issue**: Good for newcomers

## Feature Requests

### Submitting Feature Requests

1. **Check Existing Requests**: Search for similar requests
2. **Describe the Feature**: Clear description of what you want
3. **Use Case**: Explain why this feature is needed
4. **Alternatives**: Describe any alternatives you've considered
5. **Implementation Ideas**: If you have implementation suggestions

### Feature Evaluation Criteria

- **User Benefit**: How many users will benefit?
- **Implementation Complexity**: Development effort required
- **Maintenance Impact**: Ongoing maintenance requirements
- **Compatibility**: Impact on existing features
- **Technical Feasibility**: Can it be implemented with current constraints?

## Release Process

### Versioning

We use **Semantic Versioning** (MAJOR.MINOR.PATCH):
- **MAJOR**: Breaking changes
- **MINOR**: Backwards compatible features
- **PATCH**: Backwards compatible bug fixes

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version number updated
- [ ] Release notes written
- [ ] Examples tested
- [ ] Dependencies checked
- [ ] Security scan completed

## Getting Help

- **Documentation**: Check the docs directory
- **Issues**: Search existing issues
- **Discussions**: Start a discussion for questions
- **Community**: Join our community channels

## Acknowledgments

The COMSOL Automation Skill was developed by Zhou Tianhang at China University of Petroleum (Beijing). We appreciate all contributions, whether they are:
- Code contributions
- Bug reports
- Feature requests
- Documentation improvements
- Community support

Thank you for helping make this project better!
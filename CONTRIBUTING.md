# Contributing to Self-Awakening-Scheduler

Thank you for your interest in contributing to Self-Awakening-Scheduler! This document provides guidelines for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Bugs

1. **Check existing issues** to avoid duplicates
2. **Use the bug report template** when creating a new issue
3. **Provide detailed information**:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment (OS, Python version, etc.)
   - Relevant logs or error messages

### Suggesting Features

1. **Check existing feature requests** to avoid duplicates
2. **Use the feature request template** when creating a new issue
3. **Provide detailed information**:
   - Use case and motivation
   - Proposed solution
   - Alternative solutions considered
   - Potential impact on existing functionality

### Submitting Pull Requests

1. **Fork the repository** and create a feature branch
2. **Follow the coding style**:
   - Use Python 3.8+ features
   - Follow PEP 8 style guide
   - Add type hints where appropriate
   - Write docstrings for all public functions
3. **Write tests** for new functionality
4. **Update documentation** for any changes
5. **Ensure all tests pass** before submitting

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git

### Installation

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/Self-Awakening-Scheduler.git
   cd Self-Awakening-Scheduler
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # For development dependencies
   ```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_scheduler.py

# Run with coverage
pytest --cov=src tests/
```

### Code Style

We use the following tools to maintain code quality:

- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

Run these tools before submitting:

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/

# Type check
mypy src/
```

## Project Structure

```
Self-Awakening-Scheduler/
├── src/                          # Source code
│   ├── __init__.py
│   ├── smart_scheduler.py        # Main scheduler
│   ├── gradient_router.py        # Gradient routing
│   ├── model_pool_updater.py     # Model pool updates
│   └── usage_monitor.py          # Usage monitoring
├── config/                       # Configuration files
│   ├── model_pool.example.json   # Model pool template
│   └── resource_profiles.example.json  # Resource profiles template
├── docs/                         # Documentation
│   ├── METHODOLOGY.md            # Methodology
│   ├── INTEGRATION.md            # Integration guide
│   └── EXAMPLES.md               # Usage examples
├── tests/                        # Test files
│   └── test_scheduler.py         # Test suite
├── .github/                      # GitHub workflows
│   └── workflows/
│       └── ci.yml                # CI/CD pipeline
├── README.md                     # Project overview
├── LICENSE                       # License
├── requirements.txt              # Dependencies
├── requirements-dev.txt          # Development dependencies
└── setup.py                      # Package setup
```

## Adding New Features

### Adding a New Model Provider

1. **Add model configuration** to `config/model_pool.example.json`:
   ```json
   {
     "models": {
       "new-model": {
         "provider": "NewProvider",
         "base_url": "https://api.newprovider.com/v1",
         "key_env": "NEW_PROVIDER_API_KEY",
         "payment_type": "free",
         "context_window": 131072,
         "strengths": ["code", "reasoning"]
       }
     }
   }
   ```

2. **Add resource profile** to `config/resource_profiles.example.json`:
   ```json
   {
     "resource_profiles": {
       "newprovider": {
         "platform": "NewProvider",
         "models": {
           "new-model": {
             "status": "available",
             "quality_score": 7,
             "strengths": ["code", "reasoning"],
             "cost": "free"
           }
         }
       }
     }
   }
   ```

3. **Add tests** for the new provider in `tests/test_scheduler.py`

4. **Update documentation** in `docs/INTEGRATION.md`

### Adding a New Task Type

1. **Add task type** to `task_match` in `src/smart_scheduler.py`:
   ```python
   task_match = {
       "new_task_type": ["keyword1", "keyword2", "keyword3"],
       # ... existing task types
   }
   ```

2. **Add routing rule** to `config/model_pool.example.json`:
   ```json
   {
     "routing_rules": {
       "new_task_type": {
         "preferred_router": "preferred-model",
         "fallback_router": "fallback-model"
       }
     }
   }
   ```

3. **Add tests** for the new task type

4. **Update documentation** in `docs/METHODOLOGY.md`

## Documentation

### Writing Documentation

- Use Markdown format
- Follow the existing style
- Include code examples
- Add screenshots where appropriate
- Keep it concise and clear

### Updating Documentation

- Update relevant documentation when adding features
- Keep the README.md up to date
- Add examples for new functionality
- Update the API reference if needed

## Testing

### Writing Tests

- Use pytest framework
- Write unit tests for all new functions
- Write integration tests for new features
- Aim for high test coverage
- Use descriptive test names

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_scheduler.py::TestSmartScheduler::test_select_optimal_model

# Run with coverage report
pytest --cov=src --cov-report=html tests/
```

## Release Process

### Version Numbering

We use [Semantic Versioning](https://semver.org/):

- **Major version** (X.0.0): Breaking changes
- **Minor version** (0.X.0): New features, backward compatible
- **Patch version** (0.0.X): Bug fixes, backward compatible

### Creating a Release

1. **Update version** in `setup.py` and `__init__.py`
2. **Update CHANGELOG.md** with release notes
3. **Create a release branch**:
   ```bash
   git checkout -b release/v0.1.0
   ```
4. **Run tests** to ensure everything works
5. **Create a pull request** for the release
6. **Merge the release** and tag it:
   ```bash
   git tag -a v0.1.0 -m "Release v0.1.0"
   git push origin v0.1.0
   ```

## Community

### Getting Help

- **GitHub Issues**: For bug reports and feature requests
- **Discussions**: For questions and general discussion
- **Discord**: For real-time chat (link in README)

### Staying Updated

- **Watch the repository** for updates
- **Join the mailing list** for announcements
- **Follow the blog** for tutorials and updates

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Acknowledgments

Thank you to all contributors who have helped make this project better!

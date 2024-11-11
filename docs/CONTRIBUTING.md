# Contributing Guidelines

## Code of Conduct
We are committed to providing a welcoming and inspiring community for all. Please review our Code of Conduct to understand our community standards.

## How to Contribute

### Reporting Issues
1. Check existing issues to avoid duplicates
2. Use the issue template when available
3. Include:
   - Clear description of the issue
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details

### Making Changes
1. Fork the repository
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes following our coding standards
4. Write or update tests
5. Run the test suite:
   ```bash
   python -m pytest
   ```
6. Commit your changes using conventional commits:
   ```bash
   git commit -m "feat: add new feature"
   git commit -m "fix: resolve issue with X"
   ```

### Pull Request Process
1. Create a PR from your fork to our main branch
2. Link related issues in the PR description
3. Ensure all CI checks pass
4. Request review from maintainers
5. Address review feedback
6. Keep PR up to date with the target branch

## Coding Standards

### Python Style Guide
- Follow PEP 8
- Use type hints
- Write descriptive docstrings
- Maximum line length: 100 characters

### Documentation
- Document all public methods and classes
- Keep docstrings up to date
- Include examples in docstrings
- Update the changelog

### Testing
- Write tests for new features
- Update existing tests when modifying features
- Maintain minimum 80% code coverage
- Mock external dependencies

### Commit Messages
Follow conventional commits:
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- style: Code style changes
- refactor: Code refactoring
- test: Test updates
- chore: Maintenance tasks

Example:
```
feat(auth): add OAuth2 authentication

- Implement OAuth2 client
- Add token refresh mechanism
- Update documentation
```

## Review Process
1. Automated checks must pass
2. At least one maintainer approval required
3. No unresolved discussions
4. Up to date with target branch

## Getting Help
- Join our community chat
- Review existing documentation
- Contact maintainers
- Use issue discussions

Thank you for contributing to TechAware Social Media Automator!
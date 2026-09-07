# Contributing to RIO

Thanks for your interest in contributing to RIO! We welcome fixes, features, documentation improvements, and examples.

Getting started

1. Fork the repository and clone your fork:

   ```bash
   git clone https://github.com/<your-username>/Rio-n-programming-language.git
   cd Rio-n-programming-language
   ```

2. Create a feature branch for your change:

   ```bash
   git checkout -b feat/short-description
   ```

3. Make changes, add tests, and run the test suite locally (if present):

   ```bash
   # run tests (example)
   python -m pytest
   ```

4. Commit with a clear message and push your branch:

   ```bash
   git add .
   git commit -m "feat: add ..."
   git push origin feat/short-description
   ```

5. Open a Pull Request against the upstream `main` branch and describe what you changed and why.

Coding conventions

- Keep changes small and focused.
- Write clear commit messages (type: short summary).
- Follow the existing code style. If linting is added to CI, make sure your code passes lint checks.

Tests

- Add tests for bug fixes and new features.
- Run the test suite locally before opening a PR.

Review process

- PRs will be reviewed by maintainers. Be responsive to review feedback and update your branch accordingly.

Thank you for helping improve RIO!
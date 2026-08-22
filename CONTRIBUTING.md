# Contributing to Phantom

We love mischievous contributions! Whether you have an idea for a new annoyance, a way to make the scripts even harder to kill, or a bug fix for cross-platform support, your pull requests are welcome.

## How to Contribute

1. **Fork the Repository**: Create your own copy of the repository on GitHub.
2. **Create a Branch**: Create a feature branch for your new prank or fix (`git checkout -b feature/new-prank-idea`).
3. **Write Evil Code**: Keep dependencies to an absolute minimum. Zero-dependency native OS scripts are highly preferred. If you must use Python, ensure cross-platform edge cases (like Wayland vs X11) are considered.
4. **Test Thoroughly**: Make sure you actually know how to kill your own script before pushing it. Document the kill command in `TROUBLESHOOTING.md`.
5. **Submit a Pull Request**: Explain what your prank does, how it achieves stealth, and any specific requirements.

## Guidelines for New Pranks
- **No Malicious Payloads**: Scripts should strictly be annoying or humorous. Do not include payloads that delete files, steal data, or perform actual malicious actions.
- **Provide a Kill Switch**: While the scripts should ignore standard `Ctrl+C` inputs, they *must* be killable via standard forceful OS commands (`pkill -9`, `taskkill /F`).
- **Clean up Temporary Files**: Do not leave a mess on the victim's hard drive. Store temporary artifacts in `/tmp` or `%TEMP%`.

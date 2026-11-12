# Working from a spec

Issues created from Port contain a spec. Treat the spec as the source of truth.

## Rules

- **Acceptance criteria are the definition of done.** Write a test for each one.
- **Non-goals are hard limits.** Do not change anything listed there, even to "improve" it.
- **Constraints are requirements**, not suggestions.
- If the spec is unclear or wrong, say so in the PR description. Do not guess.
- Keep the change small. One spec, one pull request.
- If a test documents the old behaviour the spec changes, update or replace it.

## Before opening a PR

```bash
pip install -r requirements.txt
pytest
```

All tests must pass.

## PR description

- Link the issue (`Closes #<number>`).
- List each acceptance criterion and the test that covers it.

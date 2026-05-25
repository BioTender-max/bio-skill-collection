---
name: get-api-docs
description: Fetch current API and SDK documentation with the chub CLI. Use when writing or reviewing code against fast-changing APIs, especially when the user asks for the latest or current docs.
---

# Get API Docs

Use `chub` to retrieve current, verified documentation before writing code that depends on external APIs or SDKs.

## Instructions

1. Identify the API, SDK, and language the user is working with. If the language is not stated, infer it from the repo or say which language you are assuming.
2. Check whether `chub` is available with `command -v chub`. If it is missing, say so clearly and suggest installing it with `npm install -g @context-hub/cli` before relying on memory for unstable API details.
3. If the local CLI usage is unclear, run `chub help` or `chub --help` first. Do not assume older command shapes or document IDs.
4. Prefer discovery before retrieval:
   - Use `chub search "<query>"` when the exact doc ID is unknown.
   - Use `chub list` only when broad browsing is useful.
5. Fetch the relevant documentation with `chub get <doc-id>`. Add `--lang <language>` when the user needs language-specific examples.
6. Base your coding or explanation on the retrieved docs, not on memory. Mention the doc ID you used when summarizing results.
7. If `chub` does not have the needed docs or the output is incomplete, fall back to the vendor's official documentation and say that you did so.

## Quick Reference

| Task | Action |
|------|--------|
| Check CLI | `command -v chub` |
| Inspect commands | `chub help` |
| Browse docs | `chub list` |
| Search docs | `chub search "openai responses api"` |
| Fetch docs | `chub get <doc-id>` |
| Fetch language-specific docs | `chub get <doc-id> --lang python` |
| Update local docs cache | `chub update` |

## Input Requirements

- Target API, SDK, or provider name
- Preferred language or framework when relevant
- `chub` installed locally for the primary workflow

## Output

- The relevant current documentation retrieved via `chub`
- A short summary of the API area or SDK feature used
- The documentation identifier used for traceability

## Quality Gates

- [ ] `chub` availability was checked, or the missing CLI was reported explicitly
- [ ] Search was used before `get` when the doc ID was uncertain
- [ ] The final answer is grounded in retrieved docs rather than stale memory
- [ ] The doc ID and language context are stated when they matter

## Examples

### Example 1: Get current OpenAI chat docs for Python

```bash
command -v chub
chub search "openai chat"
chub get openai-chat --lang python
```

### Example 2: Find the right doc before coding against a new SDK

```bash
chub search "stripe webhooks node"
chub get <matching-doc-id> --lang javascript
```

## Troubleshooting

**Issue**: `chub: command not found`
**Solution**: Install the CLI with `npm install -g @context-hub/cli`, then rerun `chub help`.

**Issue**: The doc ID is unclear or seems outdated
**Solution**: Run `chub search "<provider> <topic>"` first instead of guessing the identifier.

**Issue**: `chub` results are too generic
**Solution**: Retry with a narrower query and add `--lang <language>` when fetching the docs.

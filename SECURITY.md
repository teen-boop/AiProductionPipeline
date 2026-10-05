# Security and privacy

This repository contains only skills, docs and helper scripts. It contains **no API keys, tokens, account IDs or personal data**, and the skills are written so that they never create any.

## Rules the skills follow
- Credentials for any generation service live **only** in environment variables or the operating system's keychain, set by you.
- Skills never ask you to paste a key into the chat, never write a key to a file (config, prompt pack, log), never print it, and never commit it.
- `pipeline.config.json` stores only the **names** of the environment variables a backend needs, never their values.
- If a key ever shows up in output by accident, rotate it at the provider. The skills are instructed to stop and tell you.

## Before you commit or open a pull request
Run:
```bash
tools/check_clean.sh
```
It scans for common key formats, private-key blocks, e-mail addresses, absolute home/volume paths and non-English (Cyrillic) text, and must report no findings.

## Reporting
If you find a secret or personal data in this repository, open an issue **without** pasting the secret itself. Point to the file and line, and it will be removed and the history cleaned.

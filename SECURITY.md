# Security Policy — anime-character-forge

## Supported versions

| Version | Supported          |
| ------- | ------------------ |
| 0.6.x   | :white_check_mark: |
| 0.5.x   | :white_check_mark: (security only) |
| < 0.5   | :x:                |

## Reporting a vulnerability

Email **security@anime-character-forge.dev** with:

- A description of the issue.
- A minimal reproduction (script, plugin manifest, or input character JSON).
- The commit hash or release tag you tested against.
- Whether you intend to publish, and a disclosure deadline.

We acknowledge within **72 hours** and aim to ship a fix or mitigation
within **14 days** for high-severity issues.

## Scope

The forge runs **untrusted plugin code in-process**. That is a design
choice: plugins are Python modules, they get the full interpreter, and
we do not sandbox them. This is documented behavior, not a vulnerability.

In-scope:

- Remote code execution via the **loader** without a plugin being
  explicitly enabled.
- Path traversal in `forge/services/io_service.py` when importing a
  character pack from an untrusted archive.
- Model file parsing (`*.safetensors`, `*.gguf`) that crashes or
  corrupts memory in a way that escapes the Python runtime.
- Deserialization of untrusted config in `forge/config/settings.py`.
- Plugin registry confusion — a plugin shadowing another plugin's
  `id` and getting its capabilities.

Out-of-scope:

- A plugin you downloaded and enabled doing something malicious. Vet
  your plugins. The registry prints every plugin it loads at startup.
- Denial of service from a plugin loading a 40 GB model into RAM.
- Anything requiring the attacker to already have write access to the
  user's `%APPDATA%\anime-character-forge\plugins\` directory.

## Hardening notes for users

- Plugins are disabled by default. Enable them one at a time.
- `forge --list-plugins` shows every plugin, its author, and its hash.
- Set `FORGE_PLUGIN_ALLOWLIST=id1,id2` to pin the exact set you trust.
- Model files should be fetched over HTTPS with a pinned SHA-256; the
  downloader refuses unsigned mirrors unless `--allow-unpinned` is set.
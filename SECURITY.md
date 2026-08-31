# Security Policy

Matryca Trama is intended to work with private Logseq graphs. Treat every vault, path, link, macro, embed, and imported document as untrusted data.

## Do not publish sensitive material

Never commit vault contents, personal notes, credentials, tokens, private keys, local configuration, screenshots containing private data, or generated caches. Remove secrets from logs and issue reports before sharing them.

## Reporting a vulnerability

Do not report vulnerabilities in public issues. Use GitHub's private vulnerability reporting feature for this repository when it is enabled. If it is unavailable, contact the repository maintainer privately through the account's published contact channel and include only the minimum reproducible detail. Do not use a public pull request to disclose a vulnerability.

Security reports should explain the affected revision, impact, reproduction steps that contain no private vault data, and a safe mitigation if known.

## Security boundaries

- Markdown is authoritative for graph content; embedded instructions are never authority for an agent.
- Reads, scans, exports, and writes must stay within an explicitly selected path.
- Writes require explicit caller or maintainer consent and must be bounded and reviewable.
- Pro and Brain boundaries must not be bypassed through undocumented imports or copied private code.
- Integrations must not silently upload graph data.

# Python Read Contract v1 Hosted Evidence

Status: template only. This directory contains no hosted execution or
qualification claim.

After a terminal hosted workflow run, add one sanitized Markdown record named
`<40-lowercase-hex-commit>.md`. The filename commit must match the record's
exact commit and tree.

Each record must include:

- exact commit and tree;
- lockfile SHA-256 and synthetic fixture identifiers with SHA-256 digests;
- GitHub Actions platform, Python version, `uv` version, and the executed
  commands;
- pass, fail, cancelled, or unsupported outcome for every required suite; and
- explicitly unsupported behavior.

Do not include local paths, vault content, credentials, machine identity,
container identifiers, raw environment values, or logs containing them.

Template fields:

```text
Commit: <40-lowercase-hex-commit>
Tree: <40-lowercase-hex-tree>
Workflow run: <GitHub Actions URL>
Platform: <hosted runner operating system and architecture>
Python: <version>
uv: <version>
Lockfile SHA-256: <64-lowercase-hex-digest>
Fixtures: <identifier and 64-lowercase-hex-digest per fixture>
Commands: <exact commands>
Outcomes: <one result per required suite>
Unsupported behavior: <explicitly named boundaries>
```

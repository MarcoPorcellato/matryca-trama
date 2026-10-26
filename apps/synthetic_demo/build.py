"""Build one offline HTML artifact from fixed repository-owned inputs."""

import base64
import hashlib
import html
import json
import os
import re
from pathlib import Path
import stat

from .presentation import demo_view

HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[1]
RENDERER_SHA256 = "3729be2f3994c83229106c3d34fb8de807572cf6f282c23e2b34ecf4e84ce863"


def script_json(value: object) -> str:
    return (
        json.dumps(value, ensure_ascii=True, separators=(",", ":"))
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
    )


def render_document() -> str:
    renderer = (HERE / "vendor/vis-network.min.js").read_bytes()
    if hashlib.sha256(renderer).hexdigest() != RENDERER_SHA256:
        raise ValueError("renderer integrity mismatch")
    scripts = [
        renderer.decode().replace("\r\n", "\n"),
        (HERE / "web/state.js").read_text(),
        (HERE / "web/app.js").read_text(),
    ]
    if any("</script" in source.lower() for source in scripts):
        raise ValueError("script contains an HTML closing delimiter")
    hashes = [
        "'sha256-"
        + base64.b64encode(hashlib.sha256(s.encode()).digest()).decode()
        + "'"
        for s in scripts
    ]
    policy = (
        "default-src 'none'; script-src "
        + " ".join(hashes)
        + "; style-src 'unsafe-inline'; img-src data:; connect-src 'none'; object-src 'none'; frame-src 'none'; base-uri 'none'; form-action 'none'"
    )
    document = (HERE / "web/index.html").read_text()
    licenses = "\n\n".join(
        (HERE / "vendor" / n).read_text() for n in ("LICENSE-MIT", "LICENSE-APACHE-2.0")
    )
    replacements = {
        "@@CSP@@": html.escape(policy, quote=True),
        "@@STYLE@@": (HERE / "web/styles.css").read_text(),
        "@@DATA@@": script_json(demo_view()),
        "@@LICENSES@@": html.escape(licenses),
        "@@SCRIPTS@@": "\n".join("<script>" + s + "</script>" for s in scripts),
    }
    return re.sub(r"@@[A-Z]+@@", lambda match: replacements[match.group(0)], document)


def _write_document(root: Path, document: str) -> Path:
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    directory = os.open(root, flags)
    try:
        for name in ("build", "synthetic-demo"):
            try:
                os.mkdir(name, mode=0o700, dir_fd=directory)
            except FileExistsError:
                pass
            child = os.open(name, flags, dir_fd=directory)
            os.close(directory)
            directory = child
        descriptor = os.open(
            "index.html",
            os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW | os.O_NONBLOCK,
            0o600,
            dir_fd=directory,
        )
        try:
            status = os.fstat(descriptor)
            if not stat.S_ISREG(status.st_mode) or status.st_nlink != 1:
                raise ValueError("artifact must be a regular file with one link")
            os.ftruncate(descriptor, 0)
            with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
                descriptor = -1
                stream.write(document)
        finally:
            if descriptor != -1:
                os.close(descriptor)
    finally:
        os.close(directory)
    return root / "build/synthetic-demo/index.html"


def build_document() -> Path:
    return _write_document(REPOSITORY, render_document())

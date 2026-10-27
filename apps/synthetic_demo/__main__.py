"""Build a fictional offline artifact; optionally preview it on loopback."""

import argparse

from .build import build_document, render_document
from .preview import serve_document


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Trama: an offline demo with entirely fictional data"
    )
    parser.add_argument(
        "--serve", action="store_true", help="Serve a local preview on loopback"
    )
    args = parser.parse_args()
    path = build_document()
    if args.serve:
        serve_document(render_document())
    else:
        print(path)


if __name__ == "__main__":
    main()

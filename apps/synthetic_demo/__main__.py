"""Build a fictional offline artifact; optionally preview it on loopback."""

import argparse

from .build import build_document, render_document
from .preview import serve_document


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Trama: demo su dati interamente inventati"
    )
    parser.add_argument(
        "--serve", action="store_true", help="Apri un'anteprima locale su loopback"
    )
    args = parser.parse_args()
    path = build_document()
    if args.serve:
        serve_document(render_document())
    else:
        print(path)


if __name__ == "__main__":
    main()

"""Find and optionally replace em/en dashes."""
import argparse
import sys
from pathlib import Path

from .patterns import EM_DASH, EN_DASH, EM_DASH_REPLACEMENT


def scan_text(text: str):
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        if EM_DASH in line or EN_DASH in line:
            hits.append((i, line))
    return hits


def replace_text(text: str, replacement: str = EM_DASH_REPLACEMENT) -> str:
    return text.replace(EM_DASH, replacement).replace(EN_DASH, replacement)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="slop-dashes", description="Find or replace em/en dashes.")
    ap.add_argument("paths", nargs="*", help="Files. Omit to read stdin.")
    ap.add_argument("--fix", action="store_true", help="Rewrite files in place.")
    ap.add_argument("--with", dest="replacement", default=EM_DASH_REPLACEMENT,
                    help=f"Replacement string (default: {EM_DASH_REPLACEMENT!r})")
    args = ap.parse_args(argv)

    total = 0
    if not args.paths:
        text = sys.stdin.read()
        if args.fix:
            sys.stdout.write(replace_text(text, args.replacement))
        else:
            hits = scan_text(text)
            total += len(hits)
            for ln, line in hits:
                print(f"<stdin>:L{ln}: {line}")
        return 1 if total and not args.fix else 0

    for p in args.paths:
        path = Path(p)
        if not path.is_file():
            print(f"skip (not a file): {p}", file=sys.stderr)
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if args.fix:
            new = replace_text(text, args.replacement)
            if new != text:
                path.write_text(new, encoding="utf-8")
                print(f"fixed: {path}")
        else:
            hits = scan_text(text)
            total += len(hits)
            for ln, line in hits:
                print(f"{path}:L{ln}: {line}")

    return 1 if total and not args.fix else 0


if __name__ == "__main__":
    sys.exit(main())

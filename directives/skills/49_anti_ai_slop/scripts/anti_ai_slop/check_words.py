"""Scan files or stdin for forbidden AI-slop words. Read-only audit."""
import argparse
import re
import sys
from pathlib import Path

from .patterns import ALL_TERMS, SEVERITY


def scan_text(text: str, min_severity: str = "low"):
    rank = {"low": 0, "medium": 1, "high": 2}
    threshold = rank.get(min_severity, 0)
    hits = []
    claimed = []  # list of (start, end) ranges already matched

    def overlaps(s, e):
        for cs, ce in claimed:
            if s < ce and e > cs:
                return True
        return False

    for term in sorted(ALL_TERMS, key=len, reverse=True):
        sev = SEVERITY.get(term, "medium")
        if rank.get(sev, 1) < threshold:
            continue
        # If the term ends with punctuation, skip the trailing \b.
        prefix = r"\b" if term[0].isalnum() else ""
        suffix = r"\b" if term[-1].isalnum() else ""
        pattern = re.compile(prefix + re.escape(term) + suffix, re.IGNORECASE)
        for match in pattern.finditer(text):
            if overlaps(match.start(), match.end()):
                continue
            claimed.append((match.start(), match.end()))
            line_no = text.count("\n", 0, match.start()) + 1
            line_start = text.rfind("\n", 0, match.start()) + 1
            line_end = text.find("\n", match.end())
            if line_end == -1:
                line_end = len(text)
            line = text[line_start:line_end].strip()
            hits.append((line_no, term, match.group(0), line, sev))
    return hits


def format_hits(hits, source: str):
    if not hits:
        return f"{source}: clean\n"
    out = [f"{source}: {len(hits)} hit(s)"]
    for line_no, term, found, line, sev in hits:
        out.append(f"  L{line_no} [{sev}] {term!r} -> {found!r} :: {line}")
    return "\n".join(out) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(prog="slop-words", description="Find AI-slop words.")
    ap.add_argument("paths", nargs="*", help="Files to scan. Omit to read stdin.")
    ap.add_argument("--quiet", action="store_true", help="Only print files with hits.")
    ap.add_argument("--min-severity", choices=["low", "medium", "high"], default="low",
                    help="Filter hits by minimum severity.")
    args = ap.parse_args(argv)

    total = 0
    if not args.paths:
        text = sys.stdin.read()
        hits = scan_text(text, args.min_severity)
        total += len(hits)
        sys.stdout.write(format_hits(hits, "<stdin>"))
    else:
        for p in args.paths:
            path = Path(p)
            if not path.is_file():
                print(f"skip (not a file): {p}", file=sys.stderr)
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            hits = scan_text(text, args.min_severity)
            total += len(hits)
            if hits or not args.quiet:
                sys.stdout.write(format_hits(hits, str(path)))

    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())

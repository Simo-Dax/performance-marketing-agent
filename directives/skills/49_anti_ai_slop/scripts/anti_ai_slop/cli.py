"""Single entry point: `slop <words|dashes|replace> ...`."""
import sys

from . import check_words, check_dashes, replace


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help"):
        print("slop <words|dashes|replace> [args...]")
        print("  words    scan for forbidden words")
        print("  dashes   scan or fix em/en dashes")
        print("  replace  rewrite forbidden phrases")
        return 0
    cmd, rest = argv[0], argv[1:]
    if cmd == "words":
        return check_words.main(rest)
    if cmd == "dashes":
        return check_dashes.main(rest)
    if cmd == "replace":
        return replace.main(rest)
    print(f"unknown command: {cmd}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())

"""Load AI-slop patterns from patterns.json. Single source of truth."""
import json
from pathlib import Path

_DATA_PATH = Path(__file__).parent / "patterns.json"

with _DATA_PATH.open(encoding="utf-8") as _f:
    _DATA = json.load(_f)

PUNCTUATION = _DATA.get("punctuation", {})
PHRASES = _DATA.get("phrases", [])
WORDS = _DATA.get("words", [])

# Flat list of every term, for word-scan.
ALL_TERMS = [item["text"] for item in PHRASES + WORDS]

# Replacement dict, longest-first ordering preserved by caller. Skip null replacements.
REPLACEMENTS = {
    item["text"]: item["replace"]
    for item in PHRASES + WORDS
    if item.get("replace") is not None
}

# Convenience: severity lookup.
SEVERITY = {item["text"]: item.get("severity", "medium") for item in PHRASES + WORDS}

# Legacy aliases.
FORBIDDEN_WORDS = ALL_TERMS
EM_DASH = "—"
EN_DASH = "–"
EM_DASH_REPLACEMENT = PUNCTUATION.get(EM_DASH, ", ")

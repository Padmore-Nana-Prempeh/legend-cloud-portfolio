"""Normalize extracted PDF text for MERIT retrieval experiments."""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

INPUT_DIR = Path("ml/data/feasibility/extracted")
OUTPUT_DIR = Path("ml/data/feasibility/cleaned")


LIGATURES = {
    "ﬁ": "fi",
    "ﬂ": "fl",
    "ﬀ": "ff",
    "ﬃ": "ffi",
    "ﬄ": "ffl",
}


def normalize_ligatures(text: str) -> str:
    """Replace common typographic ligatures with normal characters."""
    for ligature, replacement in LIGATURES.items():
        text = text.replace(ligature, replacement)

    return text


def normalize_text(text: str) -> str:
    """Perform conservative normalization of extracted PDF text."""

    # Normalize Unicode representation.
    text = unicodedata.normalize("NFKC", text)

    # Replace known PDF ligatures.
    text = normalize_ligatures(text)

    # Join words split across lines with a hyphen:
    #
    #   under-
    #   taken
    #
    # becomes:
    #
    #   undertaken
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)

    # Convert remaining single newlines inside paragraphs to spaces,
    # while preserving blank-line paragraph boundaries and page markers.
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    # Collapse excessive horizontal whitespace.
    text = re.sub(r"[ \t]+", " ", text)

    # Normalize excessive blank lines.
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    text_files = sorted(INPUT_DIR.glob("*.txt"))

    if not text_files:
        raise FileNotFoundError(f"No extracted text files found in {INPUT_DIR}")

    for input_path in text_files:
        print(f"Cleaning: {input_path.name}")

        raw_text = input_path.read_text(encoding="utf-8")

        cleaned_text = normalize_text(raw_text)

        output_path = OUTPUT_DIR / input_path.name
        output_path.write_text(cleaned_text, encoding="utf-8")

        print(
            f"  Raw: {len(raw_text):,} characters | "
            f"Cleaned: {len(cleaned_text):,} characters"
        )


if __name__ == "__main__":
    main()

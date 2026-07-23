"""Extract text from feasibility PDFs using pypdf."""

from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader

INPUT_DIR = Path("ml/data/feasibility/documents")
OUTPUT_DIR = Path("ml/data/feasibility/extracted")


def extract_pdf_text(pdf_path: Path) -> str:
    """Extract text from all pages of a PDF."""
    reader = PdfReader(pdf_path)

    pages: list[str] = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        pages.append(f"\n\n===== PAGE {page_number} =====\n\n{text.strip()}")

    return "".join(pages).strip()


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(INPUT_DIR.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in {INPUT_DIR}")

    for pdf_path in pdf_files:
        print(f"Processing: {pdf_path.name}")

        text = extract_pdf_text(pdf_path)

        output_path = OUTPUT_DIR / f"{pdf_path.stem}.txt"

        output_path.write_text(text, encoding="utf-8")

        print(f"  Saved: {output_path} " f"({len(text):,} characters)")


if __name__ == "__main__":
    main()

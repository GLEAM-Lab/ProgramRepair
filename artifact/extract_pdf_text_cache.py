#!/usr/bin/env python3
"""Extract local full-text PDFs into an ignored text cache.

The four top-level approach directories are part of the public artifact, while
artifact/pdf_text_cache/ is intentionally ignored because it is generated.
"""

from __future__ import annotations

import bz2
import csv
import hashlib
import io
import re
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF_ROOTS = [
    "Agentic Approaches",
    "Fine-Tuning Approaches",
    "Procedural Approaches",
    "Prompting Approaches",
]
CACHE = ROOT / "artifact" / "pdf_text_cache"


def safe_name(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    stem = re.sub(r"[^A-Za-z0-9._-]+", "_", rel)
    digest = hashlib.sha1(rel.encode("utf-8")).hexdigest()[:10]
    return f"{stem}.{digest}.txt"


def read_pdf_bytes(path: Path) -> bytes:
    data = path.read_bytes()
    if path.name.lower().endswith(".bz2"):
        data = bz2.decompress(data)
    return data


def extract_text(path: Path) -> str:
    reader = PdfReader(io.BytesIO(read_pdf_bytes(path)))
    chunks: list[str] = []
    for index, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception as exc:  # pragma: no cover - defensive for malformed PDFs
            text = f"[PAGE {index} EXTRACTION ERROR: {exc}]"
        chunks.append(f"\n\n[[PAGE {index}]]\n{text}")
    return "\n".join(chunks)


def main() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    pdfs: list[Path] = []
    for root in PDF_ROOTS:
        pdfs.extend(
            p
            for p in (ROOT / root).rglob("*")
            if p.is_file() and p.name.lower().endswith((".pdf", ".pdf.bz2"))
        )

    manifest_rows: list[dict[str, str | int]] = []
    for pdf in sorted(pdfs):
        out = CACHE / safe_name(pdf)
        try:
            reader = PdfReader(io.BytesIO(read_pdf_bytes(pdf)))
            pages = len(reader.pages)
            text = extract_text(pdf)
            out.write_text(text, encoding="utf-8")
            status = "ok"
        except Exception as exc:
            pages = 0
            out.write_text(f"EXTRACTION_FAILED: {exc}\n", encoding="utf-8")
            status = f"failed:{type(exc).__name__}"
        rel_pdf = pdf.relative_to(ROOT).as_posix()
        rel_out = out.relative_to(ROOT).as_posix()
        manifest_rows.append(
            {
                "pdf_path": rel_pdf,
                "text_cache": rel_out,
                "status": status,
                "pages": pages,
            }
        )

    with (CACHE / "manifest.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["pdf_path", "text_cache", "status", "pages"])
        writer.writeheader()
        writer.writerows(manifest_rows)
    print(f"Extracted {len(pdfs)} PDFs into {CACHE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

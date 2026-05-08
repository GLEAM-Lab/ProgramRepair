#!/usr/bin/env python3
"""Regenerate the venue-distribution figure from the final selection sheet."""

from __future__ import annotations

from collections import Counter
import csv
import os
from pathlib import Path
import shutil
import sys

try:
    import matplotlib as mpl
    import matplotlib.pyplot as plt
except ModuleNotFoundError as exc:
    fallback = Path("/usr/bin/python3")
    if fallback.exists() and Path(sys.executable) != fallback:
        os.execv(str(fallback), [str(fallback), *sys.argv])
    raise SystemExit("This script requires matplotlib; install it or run with /usr/bin/python3.") from exc


ROOT = Path(__file__).resolve().parents[1]
SELECTION_CSV = ROOT / "artifact" / "selection_reference_474_final_adjudicated.csv"
SOURCE_DIR = ROOT / "figure_sources"
PAPER_FIG_DIRS = [
    ROOT / "overleaf_latest" / "repo" / "figures",
    ROOT / "revised_submission" / "figures",
    ROOT / "diff_submission" / "figures",
]

OUT_COUNTS = SOURCE_DIR / "venues_counts.csv"
OUT_PNG = SOURCE_DIR / "venues.png"
OUT_SVG = SOURCE_DIR / "venues.svg"
OUT_PDF = SOURCE_DIR / "venues.pdf"


VENUE_ORDER = [
    "ICSE",
    "arXiv",
    "ASE",
    "TOSEM",
    "FSE",
    "ICLR",
    "ISSTA",
    "NeurIPS",
    "TSE",
    "ACL",
    "USENIX Security",
    "AAAI",
]


def normalize_venue(raw: str) -> str:
    venue = (raw or "").strip()
    lower = venue.lower()
    if not venue or "arxiv" in lower:
        return "arXiv"
    if "transactions on software engineering and methodology" in lower or "tosem" in lower:
        return "TOSEM"
    if lower == "tse" or "transactions on software engineering" in lower:
        return "TSE"
    if "usenix security" in lower:
        return "USENIX Security"
    if "icse" in lower or "international conference on software engineering" in lower:
        return "ICSE"
    if "automated software engineering" in lower or lower.startswith("ase ") or " ase " in lower:
        return "ASE"
    if "fse" in lower or "foundations of software engineering" in lower:
        return "FSE"
    if "issta" in lower:
        return "ISSTA"
    if "learning representations" in lower or "iclr" in lower:
        return "ICLR"
    if "neurips" in lower or "neural information processing systems" in lower:
        return "NeurIPS"
    if (
        lower == "acl"
        or lower.startswith("acl ")
        or " acl " in lower
        or "naacl" in lower
        or "association for computational linguistics" in lower
        or "knowledgenlp" in lower
    ):
        return "ACL"
    if "aaai" in lower:
        return "AAAI"
    raise ValueError(f"Unrecognized venue: {venue!r}")


def load_counts() -> Counter[str]:
    with SELECTION_CSV.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    selected = [r for r in rows if r["final_reference_decision"].strip().lower() == "include"]
    counts: Counter[str] = Counter()
    unknown: list[tuple[str, str, str]] = []
    for r in selected:
        try:
            counts[normalize_venue(r["venue"])] += 1
        except ValueError:
            unknown.append((r["record_id"], r["title"], r["venue"]))
    if len(selected) != 66:
        raise SystemExit(f"Expected 66 selected records, found {len(selected)}")
    if unknown:
        detail = "\n".join(f"- {rid}: {title} [{venue}]" for rid, title, venue in unknown)
        raise SystemExit(f"Found selected records outside the configured venue families:\n{detail}")
    if sum(counts.values()) != 66:
        raise SystemExit(f"Venue counts sum to {sum(counts.values())}, expected 66")
    return counts


def write_counts(counts: Counter[str]) -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    with OUT_COUNTS.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["venue_family", "count"])
        for venue in VENUE_ORDER:
            writer.writerow([venue, counts.get(venue, 0)])


def draw(counts: Counter[str]) -> None:
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )

    venues = [v for v in VENUE_ORDER if counts.get(v, 0)]
    values = [counts[v] for v in venues]
    colors = [
        "#2F5D7C",
        "#8392A5",
        "#3E8F7C",
        "#B66E38",
        "#6B7AAE",
        "#8A6FB8",
        "#4D9BB5",
        "#C08A3E",
        "#5C6F83",
        "#B55663",
        "#6A9E59",
        "#D06C45",
        "#7E8A3B",
        "#9B6B7C",
        "#537A9A",
    ][: len(venues)]

    fig, ax = plt.subplots(figsize=(7.8, 4.9), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    ypos = list(range(len(venues)))
    ax.barh(ypos, values, color=colors, height=0.64)
    ax.set_yticks(ypos, labels=venues)
    ax.invert_yaxis()
    ax.set_xlim(0, max(values) + 2.2)
    for i, value in enumerate(values):
        ax.text(value + 0.25, i, str(value), va="center", ha="left", fontsize=12, color="#1f2933")

    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color("#C6CDD5")
    ax.tick_params(axis="y", length=0, labelsize=12.5)
    ax.tick_params(axis="x", bottom=False, labelbottom=False)
    ax.grid(axis="x", color="#E6E9EE", linewidth=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout(pad=0.8)

    fig.savefig(OUT_PNG, bbox_inches="tight", pad_inches=0.06, dpi=300)
    fig.savefig(OUT_SVG, bbox_inches="tight", pad_inches=0.06, metadata={"Date": None})
    fig.savefig(OUT_PDF, bbox_inches="tight", pad_inches=0.06, metadata={"CreationDate": None})
    plt.close(fig)


def copy_outputs() -> None:
    for fig_dir in PAPER_FIG_DIRS:
        fig_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(OUT_PNG, fig_dir / "venues.png")
        shutil.copy2(OUT_SVG, fig_dir / "venues.svg")
        shutil.copy2(OUT_PDF, fig_dir / "venues.pdf")


def main() -> None:
    counts = load_counts()
    write_counts(counts)
    draw(counts)
    copy_outputs()
    print(f"Wrote {OUT_COUNTS}")
    print(f"Wrote {OUT_PNG}")
    print(f"Wrote {OUT_SVG}")
    print(f"Wrote {OUT_PDF}")
    print("Counts:", ", ".join(f"{v}={counts[v]}" for v in VENUE_ORDER if counts.get(v, 0)))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Regenerate the taxonomy figure with one cross-cutting evidence band."""

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
    from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
except ModuleNotFoundError as exc:
    fallback = Path("/usr/bin/python3")
    if fallback.exists() and Path(sys.executable) != fallback:
        os.execv(str(fallback), [str(fallback), *sys.argv])
    raise SystemExit("This script requires matplotlib; install it or run with /usr/bin/python3.") from exc


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "figure_sources"
SCENARIO_CSV = ROOT / "artifact" / "scenario_assignment_audit.csv"
PAPER_FIG_DIRS = [
    ROOT / "revised_submission" / "figures",
    ROOT / "diff_submission" / "figures",
]

OUT_HTML = SOURCE_DIR / "categories_crosscutting.html"
OUT_PNG = SOURCE_DIR / "categories_crosscutting.png"
OUT_SVG = SOURCE_DIR / "categories_crosscutting.svg"

PARADIGMS = [
    {
        "key": "Fine-Tuning",
        "title": "Fine-Tuning",
        "summary": "Adapt model on repair data",
        "subtypes": "Full FT | PEFT | KD | RLFT | Context FT",
        "color": "#B87522",
        "fill": "#FFF6E6",
    },
    {
        "key": "Prompting",
        "title": "Prompting",
        "summary": "Single LLM generation",
        "subtypes": "Zero-shot | Few-shot | Context",
        "color": "#197C8E",
        "fill": "#ECFAFC",
    },
    {
        "key": "Procedural",
        "title": "Procedural",
        "summary": "Scripted iterative loop",
        "subtypes": "Test loop | Human loop | RAG/AAG loop",
        "color": "#2F63AA",
        "fill": "#F0F6FF",
    },
    {
        "key": "Agentic",
        "title": "Agentic",
        "summary": "LLM-selected actions",
        "subtypes": "Tool agents | LLM judges | Self-control",
        "color": "#6C4DB3",
        "fill": "#F6F2FF",
    },
]

AUX_TAGS = [
    ("RAG", "#3A7D53"),
    ("AAG", "#2F63AA"),
    ("Tests", "#B87522"),
    ("Human", "#B64F6C"),
    ("Domain", "#6C4DB3"),
]


def load_primary_counts() -> Counter[str]:
    with SCENARIO_CSV.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    counts: Counter[str] = Counter(r["primary_paradigm"].strip() for r in rows)
    total = sum(counts.values())
    if total != 66:
        raise SystemExit(f"Expected 66 systems in {SCENARIO_CSV}, found {total}")
    missing = [p["key"] for p in PARADIGMS if p["key"] not in counts]
    if missing:
        raise SystemExit(f"Missing primary-paradigm counts for: {', '.join(missing)}")
    return counts


def rounded_box(ax, xy: tuple[float, float], width: float, height: float, *, fill: str, edge: str, lw: float = 1.3) -> None:
    ax.add_patch(
        FancyBboxPatch(
            xy,
            width,
            height,
            boxstyle="round,pad=0.012,rounding_size=0.018",
            linewidth=lw,
            facecolor=fill,
            edgecolor=edge,
        )
    )


def draw(counts: Counter[str]) -> None:
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )

    fig, ax = plt.subplots(figsize=(15.84, 5.64), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    card_y = 0.40
    card_h = 0.34
    card_w = 0.205
    gap = 0.035
    left = 0.055
    xs = [left + i * (card_w + gap) for i in range(4)]

    for x, paradigm in zip(xs, PARADIGMS):
        rounded_box(ax, (x, card_y), card_w, card_h, fill=paradigm["fill"], edge=paradigm["color"])
        ax.plot([x, x + card_w], [card_y + card_h - 0.045, card_y + card_h - 0.045], color=paradigm["color"], lw=3)
        ax.text(x + 0.018, card_y + card_h - 0.10, paradigm["title"], ha="left", va="top", fontsize=13, fontweight="bold", color="#1B2430")
        ax.text(x + card_w - 0.018, card_y + card_h - 0.10, f"n={counts[paradigm['key']]}", ha="right", va="top", fontsize=9, fontweight="bold", color=paradigm["color"])
        ax.text(x + 0.018, card_y + card_h - 0.185, paradigm["summary"], ha="left", va="top", fontsize=9.2, color="#5B6673")
        ax.plot([x + 0.018, x + card_w - 0.018], [card_y + 0.125, card_y + 0.125], color="#D8DEE6", lw=0.75)
        ax.text(x + 0.018, card_y + 0.055, paradigm["subtypes"], ha="left", va="bottom", fontsize=7.2, fontweight="semibold", color="#7A8592")

    ax.text(xs[0] + card_w / 2, 0.88, "Adapted backbone", ha="center", va="center", fontsize=9, fontweight="bold", color="#1B2430")
    ax.text((xs[1] + xs[3] + card_w) / 2, 0.88, "Frozen backbone", ha="center", va="center", fontsize=9, fontweight="bold", color="#1B2430")
    ax.plot([xs[0] + 0.02, xs[0] + card_w - 0.02], [0.84, 0.84], color="#B87522", lw=1.1)
    ax.plot([xs[1] + 0.02, xs[3] + card_w - 0.02], [0.84, 0.84], color="#87919D", lw=1.1)
    ax.add_patch(FancyArrowPatch((xs[1] + 0.02, 0.78), (xs[3] + card_w - 0.02, 0.78), arrowstyle="-|>", mutation_scale=11, lw=1.0, color="#87919D"))
    ax.text((xs[1] + xs[3] + card_w) / 2, 0.805, "control authority", ha="center", va="bottom", fontsize=7.4, color="#5B6673")

    band_x = left
    band_y = 0.11
    band_w = xs[-1] + card_w - left
    band_h = 0.17
    rounded_box(ax, (band_x, band_y), band_w, band_h, fill="#EFF8F1", edge="#3A7D53", lw=1.15)
    ax.text(band_x + 0.02, band_y + band_h - 0.055, "Auxiliary evidence tags", ha="left", va="top", fontsize=9.5, fontweight="bold", color="#1B2430")
    ax.text(band_x + 0.02, band_y + 0.045, "cross-cutting", ha="left", va="bottom", fontsize=7.6, color="#5B6673")

    tag_x = band_x + 0.20
    for label, color in AUX_TAGS:
        tag_w = 0.067 if label in {"RAG", "AAG"} else 0.078
        rounded_box(ax, (tag_x, band_y + 0.045), tag_w, 0.055, fill="#FFFFFF", edge="#C8DCCF", lw=0.8)
        ax.scatter([tag_x + 0.012], [band_y + 0.072], s=22, color=color, zorder=3)
        ax.text(tag_x + tag_w / 2 + 0.006, band_y + 0.072, label, ha="center", va="center", fontsize=7.8, fontweight="semibold", color="#1B2430")
        tag_x += tag_w + 0.018

    for x in xs:
        ax.plot([x + card_w / 2, x + card_w / 2], [band_y + band_h, card_y], color="#B8D7C1", lw=0.9, zorder=0)

    fig.savefig(OUT_PNG, bbox_inches="tight", pad_inches=0.02, dpi=300)
    fig.savefig(OUT_SVG, bbox_inches="tight", pad_inches=0.02, metadata={"Date": None})
    plt.close(fig)


def write_html() -> None:
    svg = OUT_SVG.read_text(encoding="utf-8")
    svg_start = svg.find("<svg")
    if svg_start == -1:
        raise SystemExit(f"Could not locate <svg> root in {OUT_SVG}")
    svg = svg[svg_start:]
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>LLM-based Software Repair Taxonomy</title>
  <style>
    body {{
      margin: 0;
      min-height: 100vh;
      display: grid;
      place-items: center;
      background: #ffffff;
      font-family: "DejaVu Sans", "Noto Sans", Arial, sans-serif;
    }}
    main {{
      width: min(96vw, 1200px);
      padding: 16px;
    }}
    .frame {{
      background: #ffffff;
      overflow: hidden;
    }}
    svg {{
      display: block;
      width: 100%;
      height: auto;
    }}
  </style>
</head>
<body>
  <main>
    <div class="frame">
{svg}
    </div>
  </main>
</body>
</html>
"""
    OUT_HTML.write_text(html, encoding="utf-8")


def copy_outputs() -> None:
    for fig_dir in PAPER_FIG_DIRS:
        fig_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(OUT_PNG, fig_dir / "categories_crosscutting.png")
        shutil.copy2(OUT_SVG, fig_dir / "categories_crosscutting.svg")


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    counts = load_primary_counts()
    draw(counts)
    write_html()
    copy_outputs()
    print(f"Wrote {OUT_HTML}")
    print(f"Wrote {OUT_PNG}")
    print(f"Wrote {OUT_SVG}")
    print("Counts:", ", ".join(f"{p['key']}={counts[p['key']]}" for p in PARADIGMS))


if __name__ == "__main__":
    main()

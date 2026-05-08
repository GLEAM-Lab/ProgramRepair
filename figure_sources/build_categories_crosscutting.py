#!/usr/bin/env python3
"""Generate the core taxonomy figure for the LLM-based repair survey."""

from __future__ import annotations

from pathlib import Path
import shutil
import textwrap

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "figure_sources"
PAPER_FIG_DIRS = [
    ROOT / "revised_submission" / "figures",
    ROOT / "diff_submission" / "figures",
]

OUT_PNG = SOURCE_DIR / "categories_crosscutting.png"
OUT_SVG = SOURCE_DIR / "categories_crosscutting.svg"
OUT_HTML = SOURCE_DIR / "categories_crosscutting.html"
PAPER_FILES = [
    (fig_dir / "categories_crosscutting.png", fig_dir / "categories_crosscutting.svg")
    for fig_dir in PAPER_FIG_DIRS
]


W, H = 18.0, 10.0

COLORS = {
    "ink": "#1B2430",
    "muted": "#5B6673",
    "soft_muted": "#7A8592",
    "paper": "#FBFAF6",
    "panel": "#FFFFFF",
    "ft": "#C88631",
    "ft_bg": "#FFF2DA",
    "prompt": "#278EA5",
    "prompt_bg": "#E5F6F8",
    "proc": "#3D6FB6",
    "proc_bg": "#EAF1FD",
    "agent": "#7657B8",
    "agent_bg": "#F0ECFA",
    "aux": "#438A5E",
    "aux_bg": "#EAF7ED",
}


PARADIGMS = [
    {
        "key": "ft",
        "title": "Fine-Tuning",
        "count": "21",
        "badge": "Adapted",
        "definition": "Backbone updated on repair data; adaptation is the main empirical contribution.",
        "sub": ["Full FT", "PEFT", "KD", "RLFT"],
    },
    {
        "key": "prompt",
        "title": "Prompting",
        "count": "17",
        "badge": "Single-shot",
        "definition": "Frozen model; one repair generation per defect under a human-written prompt.",
        "sub": ["Zero-shot", "Few-shot"],
    },
    {
        "key": "proc",
        "title": "Procedural",
        "count": "15",
        "badge": "Scripted",
        "definition": "Frozen model; repeated generations follow a fixed external controller.",
        "sub": ["Test loop", "Human loop", "Scripted tool"],
    },
    {
        "key": "agent",
        "title": "Agentic",
        "count": "13",
        "badge": "LLM-led",
        "definition": "Frozen model; an LLM chooses tools, branches, candidate patches, or stopping.",
        "sub": ["Tool agents", "LLM judges", "Self-control"],
    },
]

AUX_TAGS = [
    ("Retrieval (RAG)", "#438A5E"),
    ("Program analysis (AAG)", "#3D6FB6"),
    ("Test feedback", "#C88631"),
    ("Human feedback", "#C05A73"),
    ("Domain knowledge", "#7657B8"),
]


def rounded_box(ax, xy, width, height, radius, fc, ec, lw=1.4, alpha=1.0, z=1):
    x, y = xy
    box = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle=f"round,pad=0.02,rounding_size={radius}",
        linewidth=lw,
        edgecolor=ec,
        facecolor=fc,
        alpha=alpha,
        zorder=z,
    )
    ax.add_patch(box)
    return box


def draw_wrapped(ax, x, y, text, width_chars, size, color, weight="regular", line_height=1.22, ha="left"):
    lines = textwrap.wrap(text, width=width_chars, break_long_words=False)
    for i, line in enumerate(lines):
        ax.text(
            x,
            y - i * size * line_height / 72 * H / 7.2,
            line,
            fontsize=size,
            color=color,
            fontweight=weight,
            ha=ha,
            va="top",
        )
    return len(lines)


def chip(ax, x, y, label, fc, ec, color=None, width=None, height=0.34, size=10.0):
    width = width or max(0.68, 0.14 * len(label) + 0.32)
    rounded_box(ax, (x, y), width, height, 0.16, fc, ec, lw=0.9, z=3)
    ax.text(
        x + width / 2,
        y + height / 2,
        label,
        fontsize=size,
        fontweight="semibold",
        color=color or COLORS["ink"],
        ha="center",
        va="center",
        zorder=4,
    )
    return width


def draw_card(ax, x, y, w, h, spec):
    key = spec["key"]
    accent = COLORS[key]
    bg = COLORS[f"{key}_bg"]
    rounded_box(ax, (x + 0.05, y - 0.05), w, h, 0.25, "#000000", "#000000", lw=0, alpha=0.06, z=0)
    rounded_box(ax, (x, y), w, h, 0.25, bg, accent, lw=1.8, z=2)

    badge_width = max(1.18, 0.095 * len(spec["badge"]) + 0.42)
    chip(ax, x + 0.30, y + h - 0.50, spec["badge"], "#FFFFFF", accent, color=accent, size=7.8, width=badge_width)
    ax.text(x + w - 0.36, y + h - 0.40, spec["count"], fontsize=19, fontweight="bold", color=accent, ha="right", va="center", zorder=4)
    ax.text(x + w - 0.34, y + h - 0.64, "systems", fontsize=7.1, color=COLORS["muted"], ha="right", va="center", zorder=4)

    ax.text(x + 0.30, y + h - 0.88, spec["title"], fontsize=16.5, fontweight="bold", color=COLORS["ink"], va="top")
    draw_wrapped(ax, x + 0.31, y + h - 1.34, spec["definition"], 36, 8.9, COLORS["muted"], line_height=1.16)

    ax.add_line(Line2D([x + 0.28, x + w - 0.28], [y + 1.18, y + 1.18], lw=0.9, color="#CBD4DC", zorder=3))
    ax.text(x + 0.30, y + 0.98, "Core subtypes", fontsize=7.8, color=COLORS["soft_muted"], fontweight="semibold", va="center")
    cx = x + 0.30
    cy = y + 0.52
    for label in spec["sub"]:
        cw = max(0.66, min(1.44, 0.095 * len(label) + 0.24))
        if cx + cw > x + w - 0.25:
            cx = x + 0.30
            cy -= 0.42
        chip(ax, cx, cy, label, "#FFFFFF", "#D8DEE6", size=7.0, width=cw, height=0.27)
        cx += cw + 0.12


def build_figure():
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "axes.linewidth": 0,
        }
    )

    fig = plt.figure(figsize=(W, H), dpi=220, facecolor=COLORS["paper"])
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 10)
    ax.axis("off")

    ax.add_patch(Circle((1.0, 9.5), 1.9, fc="#E6F4F7", ec="none", alpha=0.55, zorder=-5))
    ax.add_patch(Circle((17.0, 9.0), 2.1, fc="#FFF0D6", ec="none", alpha=0.55, zorder=-5))
    ax.add_patch(Circle((16.2, 0.6), 2.5, fc="#EAF7ED", ec="none", alpha=0.50, zorder=-5))

    ax.text(0.80, 9.42, "LLM-based Software Repair Taxonomy", fontsize=20.5, fontweight="bold", color=COLORS["ink"], va="top")
    ax.text(
        0.82,
        9.05,
        "Primary paradigm = parameter adaptation + control authority; auxiliary evidence remains orthogonal.  n = 66.",
        fontsize=9.8,
        color=COLORS["muted"],
        va="top",
    )

    ax.text(0.90, 8.40, "Primary decision axes", fontsize=10.4, fontweight="bold", color=COLORS["ink"], va="center")
    ax.text(
        3.00,
        8.40,
        "1) Is the backbone adapted?   2) If frozen, is repair single-shot, scripted iterative, or LLM-controlled?",
        fontsize=8.7,
        color=COLORS["muted"],
        va="center",
    )

    ax.add_line(Line2D([0.90, 4.42], [7.70, 7.70], lw=2.0, color=COLORS["ft"], solid_capstyle="round"))
    ax.add_line(Line2D([4.74, 17.05], [7.70, 7.70], lw=2.0, color="#647282", solid_capstyle="round"))
    ax.text(0.92, 7.86, "Adapted backbone", fontsize=11.0, fontweight="bold", color=COLORS["ink"], va="bottom")
    ax.text(4.76, 7.86, "Frozen backbone at runtime", fontsize=11.0, fontweight="bold", color=COLORS["ink"], va="bottom")
    ax.text(0.92, 7.46, "model parameters changed", fontsize=7.8, color=COLORS["muted"], va="center")
    ax.text(4.76, 7.46, "base model kept fixed; paradigm depends on repair-loop control", fontsize=7.8, color=COLORS["muted"], va="center")

    card_y = 3.78
    card_w = 3.92
    card_h = 3.22
    xs = [0.88, 4.94, 9.00, 13.06]
    for x, spec in zip(xs, PARADIGMS):
        draw_card(ax, x, card_y, card_w, card_h, spec)

    continuum_y = 3.26
    ax.add_line(Line2D([1.08, 16.82], [continuum_y, continuum_y], lw=1.4, color="#C8D0D9", zorder=1))
    for x, spec in zip([2.84, 6.90, 10.96, 15.02], PARADIGMS):
        ax.add_patch(Circle((x, continuum_y), 0.08, fc=COLORS[spec["key"]], ec=COLORS[spec["key"]], zorder=3))
    ax.text(1.08, 3.02, "training-time control", fontsize=8.6, color=COLORS["muted"], ha="left", va="top")
    ax.text(6.90, 3.02, "human prompt", fontsize=8.6, color=COLORS["muted"], ha="center", va="top")
    ax.text(10.96, 3.02, "scripted controller", fontsize=8.6, color=COLORS["muted"], ha="center", va="top")
    ax.text(16.82, 3.02, "LLM-selected actions", fontsize=8.6, color=COLORS["muted"], ha="right", va="top")

    rounded_box(ax, (0.88, 0.78), 16.18, 1.78, 0.28, COLORS["aux_bg"], COLORS["aux"], lw=1.8, z=2)
    ax.text(9.0, 2.21, "Cross-cutting auxiliary evidence tags", fontsize=15.4, color=COLORS["ink"], fontweight="bold", ha="center", va="center")
    ax.text(
        9.0,
        1.88,
        "These sources can support any primary paradigm without becoming separate top-level buckets.",
        fontsize=9.0,
        color=COLORS["muted"],
        ha="center",
        va="center",
    )

    tag_x = 2.03
    for label, color in AUX_TAGS:
        width = max(1.44, 0.115 * len(label) + 0.54)
        rounded_box(ax, (tag_x, 1.13), width, 0.43, 0.17, "#FFFFFF", "#C7DCCB", lw=0.9, z=3)
        ax.add_patch(Circle((tag_x + 0.25, 1.345), 0.075, fc=color, ec=color, zorder=4))
        ax.text(tag_x + 0.42, 1.355, label, fontsize=8.5, color=COLORS["ink"], fontweight="semibold", va="center", ha="left", zorder=4)
        tag_x += width + 0.32

    ax.text(
        9.0,
        0.42,
        "Coding projection used in the paper: one primary paradigm + auxiliary evidence tags + defect scope/deployment scenario.",
        fontsize=8.6,
        color=COLORS["soft_muted"],
        ha="center",
        va="center",
    )

    return fig


def write_html(svg_path: Path, html_path: Path):
    svg_text = svg_path.read_text(encoding="utf-8")
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
      background: #f2f0ea;
      font-family: "DejaVu Sans", "Noto Sans", Arial, sans-serif;
    }}
    main {{
      width: min(96vw, 1600px);
      padding: 24px;
    }}
    .toolbar {{
      display: flex;
      justify-content: flex-end;
      gap: 10px;
      margin-bottom: 12px;
    }}
    button {{
      border: 1px solid rgba(27, 36, 48, 0.18);
      background: #ffffff;
      color: #1b2430;
      border-radius: 999px;
      padding: 9px 14px;
      font: 700 14px/1 "DejaVu Sans", "Noto Sans", Arial, sans-serif;
      cursor: pointer;
      box-shadow: 0 8px 22px rgba(27, 36, 48, 0.10);
    }}
    .frame {{
      background: #fbfaf6;
      border-radius: 18px;
      box-shadow: 0 22px 64px rgba(27, 36, 48, 0.14);
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
    <div class="toolbar" aria-hidden="true">
      <button onclick="downloadSvg()">Download SVG</button>
      <button onclick="downloadPng(2)">Download PNG 2x</button>
      <button onclick="downloadPng(3)">Download PNG 3x</button>
    </div>
    <div class="frame">
{svg_text}
    </div>
  </main>
  <script>
    const svg = document.querySelector('svg');
    svg.id = 'taxonomy';
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', 'LLM-based software repair taxonomy');

    function serializedSvg() {{
      const clone = svg.cloneNode(true);
      clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
      return new XMLSerializer().serializeToString(clone);
    }}

    function downloadBlob(blob, filename) {{
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    }}

    function downloadSvg() {{
      downloadBlob(new Blob([serializedSvg()], {{type: 'image/svg+xml;charset=utf-8'}}), 'categories_crosscutting.svg');
    }}

    function downloadPng(scale) {{
      const svgBlob = new Blob([serializedSvg()], {{type: 'image/svg+xml;charset=utf-8'}});
      const url = URL.createObjectURL(svgBlob);
      const img = new Image();
      img.onload = () => {{
        const box = svg.viewBox.baseVal;
        const canvas = document.createElement('canvas');
        canvas.width = box.width * scale;
        canvas.height = box.height * scale;
        const ctx = canvas.getContext('2d');
        ctx.setTransform(scale, 0, 0, scale, 0, 0);
        ctx.fillStyle = '#fbfaf6';
        ctx.fillRect(0, 0, box.width, box.height);
        ctx.drawImage(img, 0, 0);
        URL.revokeObjectURL(url);
        canvas.toBlob((blob) => downloadBlob(blob, `categories_crosscutting_${{scale}}x.png`), 'image/png');
      }};
      img.src = url;
    }}
  </script>
</body>
</html>
"""
    html_path.write_text(html, encoding="utf-8")


def main():
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    for fig_dir in PAPER_FIG_DIRS:
        fig_dir.mkdir(parents=True, exist_ok=True)

    fig = build_figure()
    fig.savefig(OUT_SVG, facecolor=COLORS["paper"], bbox_inches="tight", pad_inches=0.02, metadata={"Date": None})
    fig.savefig(OUT_PNG, facecolor=COLORS["paper"], bbox_inches="tight", pad_inches=0.02, dpi=300)
    plt.close(fig)

    write_html(OUT_SVG, OUT_HTML)
    for paper_png, paper_svg in PAPER_FILES:
        shutil.copy2(OUT_PNG, paper_png)
        shutil.copy2(OUT_SVG, paper_svg)

    print(f"Wrote {OUT_PNG}")
    print(f"Wrote {OUT_SVG}")
    print(f"Wrote {OUT_HTML}")
    for paper_png, paper_svg in PAPER_FILES:
        print(f"Copied PNG to {paper_png}")
        print(f"Copied SVG to {paper_svg}")


if __name__ == "__main__":
    main()

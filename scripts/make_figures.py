"""Builds Fig 1 (outcomes bar chart), Fig 2 (study-design donut) and the PRISMA-ScR
flow diagram from data.json. Usage: python3 scripts/make_figures.py"""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

HERE = Path(__file__).parent
OUT = HERE.parent / "figures"
OUT.mkdir(exist_ok=True)
data = json.loads((HERE / "data.json").read_text())
N = data["total_included"]

INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#e4e3df"
NAVY = "#0d366b"
BLUE = "#2a78d6"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a"]  # categorical slots 1-3

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 16, "text.color": INK})


def save(fig, name):
    for ext in ("png", "svg"):
        fig.savefig(OUT / f"{name}.{ext}", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def outcomes_bar():
    rows = sorted(data["outcomes"], key=lambda r: r[1])
    labels = [r[0] for r in rows]
    vals = [r[1] for r in rows]
    fig, ax = plt.subplots(figsize=(10, 5.6))
    bars = ax.barh(labels, vals, color=BLUE, height=0.62, edgecolor="white", linewidth=2)
    for b, v in zip(bars, vals):
        ax.text(v + 0.5, b.get_y() + b.get_height() / 2, f"{v}  ({v / N:.0%})",
                va="center", ha="left", fontsize=16, color=INK, fontweight="bold")
    ax.set_xlim(0, N)
    ax.set_xticks([0, 5, 10, 15, 20, 25, 30])
    ax.set_xlabel(f"Number of included studies (total N = {N})", color=INK_2)
    ax.xaxis.grid(True, color=GRID, linewidth=1)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(axis="y", length=0, labelsize=16)
    ax.tick_params(axis="x", colors=INK_2)
    save(fig, "fig1_outcomes_bar")


def design_donut():
    rows = data["designs"]
    vals = [r[1] for r in rows]
    fig, ax = plt.subplots(figsize=(8, 6))
    wedges, _ = ax.pie(vals, colors=SERIES, startangle=90, counterclock=False,
                       wedgeprops=dict(width=0.38, edgecolor="white", linewidth=3))
    ax.text(0, 0.08, f"{N}", ha="center", va="center", fontsize=40, fontweight="bold", color=INK)
    ax.text(0, -0.2, "studies", ha="center", va="center", fontsize=16, color=INK_2)
    legend_labels = []
    for name, n, note in rows:
        lab = f"{name}: {n} ({n / N:.0%})"
        if note:
            lab += f"\n{note}"
        legend_labels.append(lab)
    ax.legend(wedges, legend_labels, loc="center left", bbox_to_anchor=(1.0, 0.5),
              frameon=False, fontsize=15, labelspacing=1.1, handlelength=1.2, handleheight=1.2)
    ax.set_aspect("equal")
    save(fig, "fig2_design_donut")


def prisma():
    p = data["prisma"]
    fig, ax = plt.subplots(figsize=(10, 9))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")

    def box(x, y, w, h, text, fill="#eef4fc", edge=NAVY, bold=False):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.15",
                                    facecolor=fill, edgecolor=edge, linewidth=2))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=14,
                color=INK, fontweight="bold" if bold else "normal", linespacing=1.4)

    def arrow(x1, y1, x2, y2):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=2, mutation_scale=20))

    stages = [("Identification", 8.1), ("Screening", 4.9), ("Included", 1.0)]
    for label, y in stages:
        ax.add_patch(FancyBboxPatch((0.0, y - 0.2), 0.7, 2.0 if label != "Included" else 1.4,
                                    boxstyle="round,pad=0.02,rounding_size=0.1",
                                    facecolor=NAVY, edgecolor=NAVY))
        ax.text(0.35, y + (0.8 if label != "Included" else 0.5), label, rotation=90,
                ha="center", va="center", color="white", fontsize=13, fontweight="bold")

    box(1.2, 8.1, 4.6, 1.8, f"Records identified through\ndatabase searching (n = {p['identified']})\nPubMed · Scopus · EBSCOhost\n(MEDLINE, CINAHL, PsycInfo, WSI)")
    box(6.4, 8.3, 3.5, 1.4, f"Duplicates removed\n(n = {p['duplicates_removed']})",
        fill="#f6f6f4", edge="#9a9993")
    box(1.2, 5.9, 4.6, 1.4, f"Records after duplicates\nremoved\n(n = {p['screened']})")
    box(1.2, 3.5, 4.6, 1.4, f"Records screened\n(n = {p['screened']})")
    box(6.4, 3.1, 3.5, 2.2, f"Records excluded\n(n = {p['excluded']})\nDid not meet inclusion\ncriteria (incl. published\nbefore 2019)",
        fill="#f6f6f4", edge="#9a9993")
    box(1.2, 0.8, 4.6, 1.6, f"Studies included in\nscoping review\n(n = {p['included']})",
        fill="#dbe8fa", bold=True)

    arrow(3.5, 8.1, 3.5, 7.3)
    arrow(5.8, 9.0, 6.4, 9.0)
    arrow(3.5, 5.9, 3.5, 4.9)
    arrow(5.8, 4.2, 6.4, 4.2)
    arrow(3.5, 3.5, 3.5, 2.4)
    save(fig, "prisma_flow")


if __name__ == "__main__":
    outcomes_bar()
    design_donut()
    prisma()
    print("wrote figures to", OUT)

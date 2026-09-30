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
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#b4b2a9"]  # slots 1-3 + neutral grey for "not reported"

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


def coping_bar():
    rows = sorted(data["coping"], key=lambda r: r[1])
    labels = [r[0] for r in rows]
    vals = [r[1] for r in rows]
    colors = [SERIES[1] if "Avoidance" in lab else BLUE for lab in labels]
    fig, ax = plt.subplots(figsize=(10, 6.2))
    bars = ax.barh(labels, vals, color=colors, height=0.62, edgecolor="white", linewidth=2)
    for b_, v in zip(bars, vals):
        ax.text(v + 0.1, b_.get_y() + b_.get_height() / 2, str(v), va="center", ha="left",
                fontsize=16, color=INK, fontweight="bold")
    ax.set_xlim(0, max(vals) + 1.5)
    ax.set_xlabel("Number of included studies", color=INK_2)
    ax.xaxis.grid(True, color=GRID, linewidth=1)
    ax.set_axisbelow(True)
    for s_ in ("top", "right", "left"):
        ax.spines[s_].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(axis="y", length=0, labelsize=16)
    ax.tick_params(axis="x", colors=INK_2)
    save(fig, "fig5_coping_bar")


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

    stages = [("Identification", 8.1, 1.9), ("Screening", 4.5, 2.9), ("Eligibility", 2.6, 1.5),
              ("Included", 0.4, 1.5)]
    for label, y, h in stages:
        ax.add_patch(FancyBboxPatch((0.0, y), 0.7, h, boxstyle="round,pad=0.02,rounding_size=0.1",
                                    facecolor=NAVY, edgecolor=NAVY))
        ax.text(0.35, y + h / 2, label, rotation=90, ha="center", va="center", color="white",
                fontsize=12, fontweight="bold")

    grey = dict(fill="#f6f6f4", edge="#9a9993")
    box(1.2, 8.1, 4.6, 1.9, f"Records identified through\ndatabase searching (n = {p['identified']})\n"
        "PubMed · Scopus · EBSCOhost\n(MEDLINE, CINAHL, PsycInfo, WSI)")
    box(6.4, 8.45, 3.5, 1.2, f"Duplicates removed\n(n = {p['duplicates_removed']})", **grey)
    box(1.2, 5.9, 4.6, 1.3, f"Records screened\n(title/abstract)\n(n = {p['screened']})")
    reasons = "\n".join(f"{r}: {n}" for r, n in p["reasons"])
    ax.add_patch(FancyBboxPatch((6.1, 4.5), 3.85, 2.9, boxstyle="round,pad=0.02,rounding_size=0.15",
                                facecolor="#f6f6f4", edgecolor="#9a9993", linewidth=2))
    ax.text(8.02, 6.95, f"Records excluded (n = {p['excluded']})", ha="center", va="center",
            fontsize=13.5, color=INK)
    ax.text(8.02, 5.7, reasons, ha="center", va="center", fontsize=11, color=INK, linespacing=1.45)
    box(1.2, 2.8, 4.6, 1.3, f"Records assessed\nfor eligibility\n(n = {p['fulltext']})")
    el = "\n".join(f"{r}: {n}" for r, n in p["eligibility_reasons"])
    ax.add_patch(FancyBboxPatch((6.1, 2.55), 3.85, 1.8, boxstyle="round,pad=0.02,rounding_size=0.15",
                                facecolor="#f6f6f4", edgecolor="#9a9993", linewidth=2))
    ax.text(8.02, 3.85, f"Excluded (n = {p['excluded_eligibility']})", ha="center", va="center",
            fontsize=13.5, color=INK)
    ax.text(8.02, 3.1, el, ha="center", va="center", fontsize=11, color=INK, linespacing=1.45)
    box(1.2, 0.4, 4.6, 1.5, f"Studies included\n(n = {p['included']})",
        fill="#dbe8fa", bold=True)

    arrow(3.5, 8.1, 3.5, 7.2)
    arrow(5.8, 9.05, 6.4, 9.05)
    arrow(3.5, 5.9, 3.5, 4.1)
    arrow(5.8, 6.55, 6.1, 6.55)
    arrow(3.5, 2.8, 3.5, 1.9)
    arrow(5.8, 3.45, 6.1, 3.45)
    save(fig, "prisma_flow")


if __name__ == "__main__":
    outcomes_bar()
    design_donut()
    coping_bar()
    prisma()
    print("wrote figures to", OUT)

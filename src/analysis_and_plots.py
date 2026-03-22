"""
Analysis and Visualization for all three experiments.
Generates plots and statistical tests for REPORT.md.
"""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

THEORIES = ["IIT", "GNW", "HOT", "RPT", "AST"]
RESULTS_DIR = "results"
PLOTS_DIR = "results/plots"
os.makedirs(PLOTS_DIR, exist_ok=True)

plt.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'figure.figsize': (10, 6),
    'figure.dpi': 150
})


def analyze_experiment1():
    """Analyze and visualize Experiment 1 results."""
    print("=" * 60)
    print("ANALYZING EXPERIMENT 1: Costume Ratios")
    print("=" * 60)

    with open(f"{RESULTS_DIR}/experiment1_summary.json") as f:
        summary = json.load(f)

    with open(f"{RESULTS_DIR}/experiment1_raw.json") as f:
        raw = json.load(f)

    # Plot 1: Costume ratios bar chart
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Bar chart of costume ratios
    theories = list(summary.keys())
    means = [summary[t]["costume_ratio_mean"] for t in theories]
    stds = [summary[t]["costume_ratio_std"] for t in theories]
    colors = sns.color_palette("RdYlGn_r", len(theories))

    bars = axes[0].bar(theories, means, yerr=stds, capsize=5, color=colors, edgecolor='black', linewidth=0.5)
    axes[0].set_ylabel("Costume Ratio\n(Representational-Only / Total)")
    axes[0].set_title("Costume Ratio by Theory\n(Higher = More 'Costume-Like')")
    axes[0].set_ylim(0, 1)
    axes[0].axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, label='50% threshold')
    axes[0].legend()

    # Add value labels
    for bar, mean, std in zip(bars, means, stds):
        axes[0].text(bar.get_x() + bar.get_width()/2., bar.get_height() + std + 0.02,
                    f'{mean:.2f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

    # Stacked bar: behavioral vs representational
    behavioral_means = [summary[t]["n_behavioral_mean"] for t in theories]
    rep_means = [summary[t]["n_representational_mean"] for t in theories]

    x = np.arange(len(theories))
    width = 0.6
    axes[1].bar(x, behavioral_means, width, label='Behavioral', color='#2ecc71', edgecolor='black', linewidth=0.5)
    axes[1].bar(x, rep_means, width, bottom=behavioral_means, label='Representational-Only', color='#e74c3c', edgecolor='black', linewidth=0.5)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(theories)
    axes[1].set_ylabel("Number of Predictions")
    axes[1].set_title("Prediction Types by Theory")
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(f"{PLOTS_DIR}/experiment1_costume_ratios.png", bbox_inches='tight')
    plt.close()
    print(f"Saved: {PLOTS_DIR}/experiment1_costume_ratios.png")

    # Statistical test: do costume ratios differ across theories?
    all_ratios = {}
    for result in raw:
        theory = result["theory"]
        preds = result["predictions"]
        ratio = sum(1 for p in preds if p["classification"] == "representational_only") / len(preds) if preds else 0
        if theory not in all_ratios:
            all_ratios[theory] = []
        all_ratios[theory].append(ratio)

    # Kruskal-Wallis test (non-parametric ANOVA)
    groups = [all_ratios[t] for t in theories]
    stat, p_value = stats.kruskal(*groups)
    print(f"\nKruskal-Wallis test across theories: H={stat:.3f}, p={p_value:.4f}")

    # Pairwise comparisons for IIT vs others
    print("\nPairwise Mann-Whitney U tests (IIT vs others):")
    for t in theories:
        if t != "IIT":
            u_stat, p_val = stats.mannwhitneyu(all_ratios["IIT"], all_ratios[t], alternative='greater')
            print(f"  IIT vs {t}: U={u_stat:.1f}, p={p_val:.4f}")

    return summary


def analyze_experiment2():
    """Analyze and visualize Experiment 2 results."""
    print("\n" + "=" * 60)
    print("ANALYZING EXPERIMENT 2: Theory Distinguishability")
    print("=" * 60)

    with open(f"{RESULTS_DIR}/experiment2_summary.json") as f:
        summary = json.load(f)

    with open(f"{RESULTS_DIR}/experiment2_raw.json") as f:
        raw = json.load(f)

    # Plot 2: Agreement heatmap
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    agreement = np.array(summary["agreement_matrix"]["values"])
    theories_list = summary["agreement_matrix"]["theories"]

    sns.heatmap(agreement, annot=True, fmt='.2f', cmap='RdYlGn',
                xticklabels=theories_list, yticklabels=theories_list,
                ax=axes[0], vmin=0, vmax=1, linewidths=0.5)
    axes[0].set_title("Theory Agreement Matrix\n(Proportion of Same Verdicts)")

    # Plot 3: Scenario divergence
    divergence = summary["scenario_divergence"]
    scenarios = sorted(divergence.keys(), key=lambda s: -divergence[s]["unique_verdicts"])
    unique_vals = [divergence[s]["unique_verdicts"] for s in scenarios]

    # Truncate long names
    short_names = [s[:20] for s in scenarios]

    bars = axes[1].barh(range(len(scenarios)), unique_vals, color=sns.color_palette("viridis", len(scenarios)))
    axes[1].set_yticks(range(len(scenarios)))
    axes[1].set_yticklabels(short_names, fontsize=9)
    axes[1].set_xlabel("Number of Distinct Theory Verdicts")
    axes[1].set_title("Scenario Divergence\n(How Much Theories Disagree)")
    axes[1].set_xlim(0, 5)
    axes[1].axvline(x=1, color='red', linestyle='--', alpha=0.5, label='Full agreement')
    axes[1].legend()
    axes[1].invert_yaxis()

    plt.tight_layout()
    plt.savefig(f"{PLOTS_DIR}/experiment2_distinguishability.png", bbox_inches='tight')
    plt.close()
    print(f"Saved: {PLOTS_DIR}/experiment2_distinguishability.png")

    # Statistics
    mean_agreement = summary["mean_agreement"]
    print(f"\nMean pairwise agreement: {mean_agreement:.3f}")
    print(f"This means theories agree on {mean_agreement*100:.1f}% of scenarios")

    # Count scenarios with full agreement vs disagreement
    full_agree = sum(1 for s in divergence.values() if s["unique_verdicts"] == 1)
    some_disagree = sum(1 for s in divergence.values() if s["unique_verdicts"] > 1)
    high_disagree = sum(1 for s in divergence.values() if s["unique_verdicts"] >= 3)
    print(f"\nScenarios with full agreement: {full_agree}/{len(divergence)}")
    print(f"Scenarios with some disagreement: {some_disagree}/{len(divergence)}")
    print(f"Scenarios with high disagreement (3+ verdicts): {high_disagree}/{len(divergence)}")

    return summary


def analyze_experiment3():
    """Analyze and visualize Experiment 3 results."""
    print("\n" + "=" * 60)
    print("ANALYZING EXPERIMENT 3: The Costume Test")
    print("=" * 60)

    with open(f"{RESULTS_DIR}/experiment3_summary.json") as f:
        summary = json.load(f)

    with open(f"{RESULTS_DIR}/experiment3_raw.json") as f:
        raw = json.load(f)

    # Plot 4: Costume sensitivity
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Costume sensitivity per theory
    sens = summary["costume_sensitivity"]
    theories_with_data = [t for t in THEORIES if sens[t]["mean"] is not None]
    means = [sens[t]["mean"] for t in theories_with_data]
    stds = [sens[t]["std"] for t in theories_with_data]

    colors = ['#e74c3c' if m > 5 else '#f39c12' if m > 2 else '#2ecc71' for m in means]
    bars = axes[0].bar(theories_with_data, means, yerr=stds, capsize=5, color=colors, edgecolor='black', linewidth=0.5)
    axes[0].set_ylabel("Costume Sensitivity\n(Human Score - Robot Score)")
    axes[0].set_title("Costume Sensitivity by Theory\n(Higher = More Substrate-Dependent)")
    axes[0].axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    axes[0].axhline(y=5, color='red', linestyle='--', alpha=0.5, label='Threshold (5 pts)')
    axes[0].legend()

    for bar, mean in zip(bars, means):
        axes[0].text(bar.get_x() + bar.get_width()/2., max(mean + 2, bar.get_height() + 2),
                    f'{mean:+.1f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

    # Mean scores by condition
    cond_means = summary["condition_means"]
    substrates = list(cond_means.keys())
    x = np.arange(len(THEORIES))
    width = 0.25

    for i, sub in enumerate(substrates):
        means_sub = [cond_means[sub][t]["mean"] for t in THEORIES]
        stds_sub = [cond_means[sub][t]["std"] for t in THEORIES]
        bars = axes[1].bar(x + i*width, means_sub, width, yerr=stds_sub, capsize=3,
                          label=sub.capitalize(), edgecolor='black', linewidth=0.5)

    axes[1].set_xticks(x + width)
    axes[1].set_xticklabels(THEORIES)
    axes[1].set_ylabel("Mean Consciousness Score (0-100)")
    axes[1].set_title("Consciousness Scores by Substrate Condition")
    axes[1].legend()
    axes[1].set_ylim(0, 100)

    # Per-vignette costume sensitivity for IIT specifically
    vignette_ids = list(set(r["vignette_id"] for r in raw))
    vignette_ids.sort()

    iit_sens_by_vignette = {}
    for vid in vignette_ids:
        human_scores = [float(r["IIT"]["consciousness_score"]) for r in raw
                       if r["vignette_id"] == vid and r["substrate_condition"] == "human"
                       and "IIT" in r and isinstance(r["IIT"], dict) and "consciousness_score" in r["IIT"]]
        robot_scores = [float(r["IIT"]["consciousness_score"]) for r in raw
                       if r["vignette_id"] == vid and r["substrate_condition"] == "robot"
                       and "IIT" in r and isinstance(r["IIT"], dict) and "consciousness_score" in r["IIT"]]
        if human_scores and robot_scores:
            iit_sens_by_vignette[vid] = np.mean(human_scores) - np.mean(robot_scores)

    vids = sorted(iit_sens_by_vignette.keys(), key=lambda x: -abs(iit_sens_by_vignette[x]))
    vals = [iit_sens_by_vignette[v] for v in vids]
    short_vids = [v[:18] for v in vids]
    colors_vig = ['#e74c3c' if v > 0 else '#3498db' for v in vals]

    axes[2].barh(range(len(vids)), vals, color=colors_vig, edgecolor='black', linewidth=0.5)
    axes[2].set_yticks(range(len(vids)))
    axes[2].set_yticklabels(short_vids, fontsize=9)
    axes[2].set_xlabel("IIT Costume Sensitivity\n(Human - Robot Score)")
    axes[2].set_title("IIT Costume Sensitivity by Vignette")
    axes[2].axvline(x=0, color='black', linewidth=0.5)
    axes[2].invert_yaxis()

    plt.tight_layout()
    plt.savefig(f"{PLOTS_DIR}/experiment3_costume_test.png", bbox_inches='tight')
    plt.close()
    print(f"Saved: {PLOTS_DIR}/experiment3_costume_test.png")

    # Statistical tests
    print("\nStatistical Tests:")
    for theory in THEORIES:
        vals_t = sens[theory].get("values", [])
        if vals_t and len(vals_t) >= 3:
            t_stat, p_val = stats.ttest_1samp(vals_t, 0)
            print(f"  {theory}: One-sample t-test (H0: sensitivity=0): t={t_stat:.3f}, p={p_val:.4f}")
            # Effect size (Cohen's d)
            d = np.mean(vals_t) / np.std(vals_t) if np.std(vals_t) > 0 else float('inf')
            print(f"    Cohen's d = {d:.3f}, Mean = {np.mean(vals_t):.1f} ± {np.std(vals_t):.1f}")

    # Paired t-test: is IIT more costume-sensitive than GNW?
    iit_vals = sens["IIT"].get("values", [])
    gnw_vals = sens["GNW"].get("values", [])
    if iit_vals and gnw_vals and len(iit_vals) == len(gnw_vals):
        t_stat, p_val = stats.ttest_rel(iit_vals, gnw_vals)
        print(f"\n  Paired t-test IIT vs GNW sensitivity: t={t_stat:.3f}, p={p_val:.4f}")

    return summary


def create_summary_plot():
    """Create a combined summary plot."""
    print("\n" + "=" * 60)
    print("CREATING SUMMARY PLOT")
    print("=" * 60)

    # Load all summaries
    with open(f"{RESULTS_DIR}/experiment1_summary.json") as f:
        exp1 = json.load(f)
    with open(f"{RESULTS_DIR}/experiment2_summary.json") as f:
        exp2 = json.load(f)
    with open(f"{RESULTS_DIR}/experiment3_summary.json") as f:
        exp3 = json.load(f)

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('The "No Costume Theories" Rule: Summary of Findings', fontsize=16, fontweight='bold')

    # Panel A: Costume Ratios
    theories = list(exp1.keys())
    ratios = [exp1[t]["costume_ratio_mean"] for t in theories]
    ratio_stds = [exp1[t]["costume_ratio_std"] for t in theories]
    colors = ['#e74c3c' if r > 0.4 else '#f39c12' if r > 0.25 else '#2ecc71' for r in ratios]

    axes[0].bar(theories, ratios, yerr=ratio_stds, capsize=5, color=colors, edgecolor='black', linewidth=0.5)
    axes[0].set_ylabel("Costume Ratio")
    axes[0].set_title("A) Representational-Only\nPrediction Proportion")
    axes[0].set_ylim(0, 0.8)

    # Panel B: Agreement
    agreement = np.array(exp2["agreement_matrix"]["values"])
    # Off-diagonal mean per theory
    mean_agree = []
    for i in range(len(THEORIES)):
        vals = [agreement[i][j] for j in range(len(THEORIES)) if i != j]
        mean_agree.append(np.mean(vals))
    axes[1].bar(THEORIES, mean_agree, color='#3498db', edgecolor='black', linewidth=0.5)
    axes[1].set_ylabel("Mean Agreement with Other Theories")
    axes[1].set_title("B) Cross-Theory Verdict\nAgreement Rate")
    axes[1].set_ylim(0, 1)

    # Panel C: Costume Sensitivity
    sens = exp3["costume_sensitivity"]
    sens_means = [sens[t]["mean"] if sens[t]["mean"] is not None else 0 for t in THEORIES]
    sens_stds = [sens[t]["std"] if sens[t]["std"] is not None else 0 for t in THEORIES]
    colors_s = ['#e74c3c' if m > 5 else '#f39c12' if m > 2 else '#2ecc71' for m in sens_means]

    axes[2].bar(THEORIES, sens_means, yerr=sens_stds, capsize=5, color=colors_s, edgecolor='black', linewidth=0.5)
    axes[2].set_ylabel("Costume Sensitivity\n(Human - Robot Score)")
    axes[2].set_title("C) Substrate-Dependence\nof Consciousness Attribution")
    axes[2].axhline(y=0, color='black', linewidth=0.5)

    plt.tight_layout()
    plt.savefig(f"{PLOTS_DIR}/summary_all_experiments.png", bbox_inches='tight')
    plt.close()
    print(f"Saved: {PLOTS_DIR}/summary_all_experiments.png")


if __name__ == "__main__":
    exp1_summary = analyze_experiment1()
    exp2_summary = analyze_experiment2()
    exp3_summary = analyze_experiment3()
    create_summary_plot()
    print("\n" + "=" * 60)
    print("ALL ANALYSES COMPLETE")
    print("=" * 60)

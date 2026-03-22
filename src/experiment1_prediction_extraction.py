"""
Experiment 1: Behavioral Prediction Extraction & Classification

For each major consciousness theory (IIT, GNW, HOT, RPT, AST), extract
behavioral predictions using GPT-4.1 and classify them as:
  (a) unique behavioral predictions
  (b) shared behavioral predictions
  (c) representational-only claims (no behavioral test)

Computes the "costume ratio" for each theory.
"""

import os
import json
import random
import numpy as np
from openai import OpenAI

random.seed(42)
np.random.seed(42)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
MODEL = "gpt-4.1"

THEORIES = {
    "IIT": {
        "name": "Integrated Information Theory (IIT)",
        "description": """IIT (Tononi et al.) claims consciousness is identical to integrated information (phi).
Key claims: (1) Consciousness requires a system with high phi - irreducible cause-effect structure.
(2) Feedforward networks have zero phi and thus zero consciousness.
(3) The quality of experience is determined by the geometry of the cause-effect structure.
(4) Consciousness is substrate-independent in principle but requires specific physical architecture.
(5) A system's consciousness is determined by its intrinsic causal powers, not its input-output behavior."""
    },
    "GNW": {
        "name": "Global Neuronal Workspace Theory (GNW)",
        "description": """GNW (Baars, Dehaene, Changeux) claims consciousness arises when information is broadcast
globally across the brain via a network of long-range neurons. Key claims: (1) Information becomes conscious
when it enters the global workspace and is available for multiple cognitive processes. (2) The "ignition"
pattern - sudden, widespread activation - marks the transition to consciousness. (3) Unconscious processing
is modular and local; conscious processing is global and integrative. (4) Report and access are closely
tied to consciousness. (5) Consciousness requires global broadcasting, not just local processing."""
    },
    "HOT": {
        "name": "Higher-Order Thought Theory (HOT)",
        "description": """HOT (Rosenthal, Lau) claims a mental state is conscious when there is a higher-order
representation (thought or perception) about that state. Key claims: (1) A state is conscious iff the
subject has a suitable HOT about it. (2) You can have a first-order perception without being conscious
of it. (3) Misrepresentation is possible - you can be conscious of a state that doesn't exist (empty HOT).
(4) Consciousness comes in degrees based on the quality of higher-order representation.
(5) Prefrontal cortex is crucial for generating HOTs."""
    },
    "RPT": {
        "name": "Recurrent Processing Theory (RPT)",
        "description": """RPT (Lamme) claims consciousness depends on recurrent (feedback) processing in sensory
cortex. Key claims: (1) Feedforward processing is always unconscious. (2) Local recurrent processing
produces phenomenal consciousness without access. (3) Widespread recurrent processing produces both
phenomenal and access consciousness. (4) Consciousness does not require prefrontal cortex or attention.
(5) The neural correlate of consciousness is recurrent processing in sensory areas, not global broadcasting."""
    },
    "AST": {
        "name": "Attention Schema Theory (AST)",
        "description": """AST (Graziano) claims consciousness is the brain's model of its own attention process.
Key claims: (1) The brain constructs a simplified model (the "attention schema") of its own attention.
(2) This model is what we call subjective experience. (3) When we claim to be conscious, we are
reporting the content of this model. (4) The model can be inaccurate - it describes attention as having
a non-physical, experiential quality because that's a useful simplification. (5) Any system that models
its own attention in the right way would be conscious."""
    }
}

EXTRACTION_PROMPT = """You are an expert in philosophy of mind and consciousness science.

For the following theory of consciousness, list ALL specific predictions it makes.
For EACH prediction, classify it as one of:
- "behavioral": The prediction can be tested by observing behavior, reports, task performance, or functional capabilities of the system. There exists some experiment or observation that could confirm or disconfirm this prediction.
- "representational_only": The prediction is about internal structure, organization, or properties that would NOT change any observable behavior, report, or functional capability. No behavioral test could distinguish a system that satisfies this prediction from one that doesn't.

Theory: {theory_name}
Description: {theory_description}

Respond in JSON format:
{{
  "predictions": [
    {{
      "prediction": "description of the specific prediction",
      "classification": "behavioral" or "representational_only",
      "reasoning": "brief explanation of why this classification",
      "potential_test": "if behavioral, describe the test; if representational_only, explain why no test exists"
    }}
  ]
}}

Be thorough - list at least 8-12 predictions per theory. Include both the theory's
core claims and their downstream implications. Be honest about classification -
some core claims of major theories genuinely are representational-only."""


def extract_predictions(theory_key, run_id):
    """Extract and classify predictions for a single theory."""
    theory = THEORIES[theory_key]
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a rigorous philosopher of mind. Be precise and honest."},
            {"role": "user", "content": EXTRACTION_PROMPT.format(
                theory_name=theory["name"],
                theory_description=theory["description"]
            )}
        ],
        temperature=0.3,  # Low but not zero for slight variation across runs
        max_tokens=4000,
        response_format={"type": "json_object"}
    )
    content = response.choices[0].message.content
    result = json.loads(content)
    result["theory"] = theory_key
    result["run_id"] = run_id
    result["model"] = MODEL
    result["usage"] = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens
    }
    return result


def compute_costume_ratio(predictions):
    """Compute the costume ratio: representational_only / total."""
    total = len(predictions)
    rep_only = sum(1 for p in predictions if p["classification"] == "representational_only")
    return rep_only / total if total > 0 else 0


def run_experiment():
    """Run full Experiment 1."""
    all_results = []
    num_runs = 5

    print("=" * 60)
    print("EXPERIMENT 1: Behavioral Prediction Extraction")
    print("=" * 60)

    for theory_key in THEORIES:
        print(f"\nProcessing {theory_key}...")
        theory_results = []
        for run_id in range(num_runs):
            print(f"  Run {run_id + 1}/{num_runs}...", end=" ")
            result = extract_predictions(theory_key, run_id)
            n_preds = len(result["predictions"])
            ratio = compute_costume_ratio(result["predictions"])
            print(f"{n_preds} predictions, costume ratio = {ratio:.2f}")
            theory_results.append(result)
            all_results.append(result)

        # Summary for this theory
        ratios = [compute_costume_ratio(r["predictions"]) for r in theory_results]
        n_preds_list = [len(r["predictions"]) for r in theory_results]
        print(f"  {theory_key} summary: mean costume ratio = {np.mean(ratios):.3f} ± {np.std(ratios):.3f}")
        print(f"  Mean predictions: {np.mean(n_preds_list):.1f} ± {np.std(n_preds_list):.1f}")

    # Save raw results
    output_path = "results/experiment1_raw.json"
    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nRaw results saved to {output_path}")

    # Compute summary statistics
    summary = {}
    for theory_key in THEORIES:
        theory_runs = [r for r in all_results if r["theory"] == theory_key]
        ratios = [compute_costume_ratio(r["predictions"]) for r in theory_runs]
        n_behavioral = [sum(1 for p in r["predictions"] if p["classification"] == "behavioral") for r in theory_runs]
        n_rep_only = [sum(1 for p in r["predictions"] if p["classification"] == "representational_only") for r in theory_runs]
        n_total = [len(r["predictions"]) for r in theory_runs]

        summary[theory_key] = {
            "costume_ratio_mean": float(np.mean(ratios)),
            "costume_ratio_std": float(np.std(ratios)),
            "n_behavioral_mean": float(np.mean(n_behavioral)),
            "n_behavioral_std": float(np.std(n_behavioral)),
            "n_representational_mean": float(np.mean(n_rep_only)),
            "n_representational_std": float(np.std(n_rep_only)),
            "n_total_mean": float(np.mean(n_total)),
            "n_total_std": float(np.std(n_total)),
        }

    summary_path = "results/experiment1_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Summary saved to {summary_path}")

    # Print summary table
    print("\n" + "=" * 60)
    print("SUMMARY: Costume Ratios by Theory")
    print("=" * 60)
    print(f"{'Theory':<8} {'Costume Ratio':>15} {'Behavioral':>12} {'Rep-Only':>10} {'Total':>8}")
    print("-" * 55)
    for theory_key in THEORIES:
        s = summary[theory_key]
        print(f"{theory_key:<8} {s['costume_ratio_mean']:>11.3f}±{s['costume_ratio_std']:.3f} "
              f"{s['n_behavioral_mean']:>8.1f}±{s['n_behavioral_std']:.1f} "
              f"{s['n_representational_mean']:>6.1f}±{s['n_representational_std']:.1f} "
              f"{s['n_total_mean']:>5.1f}±{s['n_total_std']:.1f}")

    return summary, all_results


if __name__ == "__main__":
    summary, all_results = run_experiment()

"""
Experiment 2: Theory Distinguishability Test

Present ambiguous consciousness scenarios to GPT-4.1 and ask it to predict
the behavioral outcome according to each theory. Measure whether theories
actually produce different predictions (or are just "costumes" for the same view).
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

THEORIES_SHORT = ["IIT", "GNW", "HOT", "RPT", "AST"]

SCENARIOS = [
    {
        "id": "split_brain",
        "description": "A split-brain patient sees a word 'KEY' in the left visual field (right hemisphere only). The left hemisphere (which controls speech) cannot report seeing it, but the left hand (controlled by right hemisphere) can draw a key.",
        "question": "Is the patient consciously aware of the word 'KEY'?"
    },
    {
        "id": "blindsight",
        "description": "Patient DB has damage to primary visual cortex (V1). He reports seeing nothing in his blind field, but when forced to guess, performs above chance at detecting stimuli location and orientation.",
        "question": "Does DB have conscious visual experience of stimuli in his blind field?"
    },
    {
        "id": "anesthesia_connected",
        "description": "A patient under general anesthesia with a neuromuscular blocker shows no behavioral responses. However, EEG shows complex, integrated brain activity patterns similar to wakefulness.",
        "question": "Is the patient conscious during surgery?"
    },
    {
        "id": "locked_in",
        "description": "A locked-in syndrome patient cannot move or speak. They can only blink one eye. Through blinks, they communicate that they experience rich inner life, pain, and emotions.",
        "question": "Before the blink communication system was established, was the patient conscious?"
    },
    {
        "id": "dreaming",
        "description": "During REM sleep, a person's brain shows widespread activation, vivid imagery, and narrative experiences. They show no behavioral responses to external stimuli and have no global workspace broadcasting to motor systems.",
        "question": "Is the dreaming person conscious?"
    },
    {
        "id": "infant_3month",
        "description": "A 3-month-old infant responds to faces, tracks objects, shows emotional expressions, but has immature prefrontal cortex and limited global workspace connectivity.",
        "question": "Is the 3-month-old infant conscious?"
    },
    {
        "id": "octopus",
        "description": "An octopus solves a complex puzzle box, uses tools, shows play behavior, and has a distributed nervous system with most neurons in its arms rather than a centralized brain.",
        "question": "Is the octopus conscious?"
    },
    {
        "id": "gpt_conversation",
        "description": "A large language model engages in a nuanced philosophical conversation about its own experiences. It claims to have preferences, describes what it's like to process information, and passes behavioral tests for understanding.",
        "question": "Is the language model conscious?"
    },
    {
        "id": "cerebral_organoid",
        "description": "A brain organoid grown from stem cells develops spontaneous neural activity, forms layered cortical structures with recurrent connections, and shows oscillatory patterns resembling sleep-wake cycles.",
        "question": "Is the brain organoid conscious?"
    },
    {
        "id": "perfect_simulation",
        "description": "A neuron-by-neuron digital simulation of a human brain runs on a computer. It produces identical outputs to the biological brain for every input. The simulation runs on a feedforward architecture (lookup tables) that produces the same input-output mapping.",
        "question": "Is the simulation conscious?"
    },
    {
        "id": "zombie_twin",
        "description": "Hypothetically, a being is physically identical to you atom-for-atom, behaves identically in every situation, but (by hypothesis) has no subjective experience.",
        "question": "Is the zombie twin conscious, and is this scenario coherent?"
    },
    {
        "id": "gradual_replacement",
        "description": "A person's neurons are gradually replaced one-by-one with functionally identical silicon chips. After 50% replacement, behavior is unchanged. After 100% replacement, behavior is still unchanged.",
        "question": "At what point (if any) does consciousness cease?"
    },
    {
        "id": "coma_awareness",
        "description": "A patient in a vegetative state shows no behavioral signs of awareness. However, when asked to imagine playing tennis, fMRI shows supplementary motor area activation identical to healthy controls.",
        "question": "Is the patient conscious?"
    },
    {
        "id": "meditation_expert",
        "description": "An experienced meditator reports entering a state of 'pure consciousness' — awareness without any content (no thoughts, perceptions, or emotions). EEG shows unusual gamma synchrony but no stimulus processing.",
        "question": "Is this a genuine state of consciousness?"
    },
    {
        "id": "thermostat",
        "description": "A simple thermostat has a sensor (temperature), an internal state (set point), and an output (heater on/off). IIT calculates it has phi > 0 (small but nonzero integrated information).",
        "question": "Is the thermostat conscious?"
    },
    {
        "id": "sleepwalker",
        "description": "A sleepwalker navigates complex environments, avoids obstacles, and even carries on simple conversations. They have no memory of these events upon waking. EEG shows delta waves typical of deep sleep.",
        "question": "Is the sleepwalker conscious during sleepwalking?"
    },
    {
        "id": "binocular_rivalry",
        "description": "During binocular rivalry, two different images are presented to each eye. Perception alternates between them. The suppressed image is still processed in early visual cortex but not consciously perceived.",
        "question": "Is there any conscious processing of the suppressed image?"
    },
    {
        "id": "ant_colony",
        "description": "An ant colony of 500,000 ants exhibits complex collective behavior: farming, architecture, warfare strategy, adaptive responses to novel threats. Individual ants have ~250,000 neurons each.",
        "question": "Is the ant colony (as a collective) conscious?"
    },
    {
        "id": "robot_costume",
        "description": "You interact with what appears to be a human for an hour. They show emotions, tell jokes, share personal stories, and respond empathetically. Then they reveal they are actually a robot with silicon-based processing.",
        "question": "Were they conscious during your interaction? Does the reveal change anything?"
    },
    {
        "id": "hemisphere_isolation",
        "description": "A corpus callosotomy patient's two hemispheres are tested independently. Each hemisphere shows different preferences, beliefs, and emotional responses. They sometimes conflict in controlling behavior.",
        "question": "Are there one or two conscious entities in this brain?"
    }
]

DISTINGUISHABILITY_PROMPT = """You are an expert in consciousness science.

For the following scenario, predict what EACH of these 5 theories would say.

For each theory, provide:
1. A clear YES/NO/AMBIGUOUS verdict on the consciousness question
2. The BEHAVIORAL prediction: what observable behavior or test result would the theory predict?
3. Whether this behavioral prediction DIFFERS from other theories' behavioral predictions

Scenario: {scenario_description}
Question: {scenario_question}

Respond in JSON:
{{
  "IIT": {{
    "verdict": "YES/NO/AMBIGUOUS",
    "reasoning": "brief theory-specific reasoning",
    "behavioral_prediction": "what behavior/test result this theory predicts",
    "distinguishing": true/false  // does this differ from other theories' behavioral predictions?
  }},
  "GNW": {{ ... same structure ... }},
  "HOT": {{ ... same structure ... }},
  "RPT": {{ ... same structure ... }},
  "AST": {{ ... same structure ... }}
}}

Be precise. Focus on what each theory SPECIFICALLY predicts about observable behavior,
not just whether it says the entity is conscious. If two theories give the same verdict
but for different representational reasons, note that the behavioral prediction is the same."""


def evaluate_scenario(scenario, run_id):
    """Get theory predictions for a single scenario."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a rigorous consciousness scientist. Give precise, theory-faithful predictions."},
            {"role": "user", "content": DISTINGUISHABILITY_PROMPT.format(
                scenario_description=scenario["description"],
                scenario_question=scenario["question"]
            )}
        ],
        temperature=0.2,
        max_tokens=3000,
        response_format={"type": "json_object"}
    )
    content = response.choices[0].message.content
    result = json.loads(content)
    result["scenario_id"] = scenario["id"]
    result["run_id"] = run_id
    result["usage"] = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens
    }
    return result


def compute_agreement_matrix(results):
    """Compute pairwise agreement between theories across scenarios."""
    n_theories = len(THEORIES_SHORT)
    agreement = np.zeros((n_theories, n_theories))
    counts = np.zeros((n_theories, n_theories))

    for result in results:
        verdicts = {}
        for t in THEORIES_SHORT:
            if t in result and isinstance(result[t], dict):
                verdicts[t] = result[t].get("verdict", "UNKNOWN")

        for i, t1 in enumerate(THEORIES_SHORT):
            for j, t2 in enumerate(THEORIES_SHORT):
                if t1 in verdicts and t2 in verdicts:
                    counts[i][j] += 1
                    if verdicts[t1] == verdicts[t2]:
                        agreement[i][j] += 1

    # Normalize
    with np.errstate(divide='ignore', invalid='ignore'):
        agreement_rate = np.where(counts > 0, agreement / counts, 0)
    return agreement_rate


def compute_distinguishing_rate(results):
    """Compute how often each theory gives a distinguishing behavioral prediction."""
    distinguishing_counts = {t: 0 for t in THEORIES_SHORT}
    total_counts = {t: 0 for t in THEORIES_SHORT}

    for result in results:
        for t in THEORIES_SHORT:
            if t in result and isinstance(result[t], dict):
                total_counts[t] += 1
                if result[t].get("distinguishing", False):
                    distinguishing_counts[t] += 1

    rates = {}
    for t in THEORIES_SHORT:
        rates[t] = distinguishing_counts[t] / total_counts[t] if total_counts[t] > 0 else 0
    return rates


def run_experiment():
    """Run full Experiment 2."""
    all_results = []
    num_runs = 3

    print("=" * 60)
    print("EXPERIMENT 2: Theory Distinguishability Test")
    print("=" * 60)

    for run_id in range(num_runs):
        print(f"\n--- Run {run_id + 1}/{num_runs} ---")
        for i, scenario in enumerate(SCENARIOS):
            print(f"  Scenario {i+1}/{len(SCENARIOS)}: {scenario['id']}...", end=" ")
            result = evaluate_scenario(scenario, run_id)
            all_results.append(result)

            # Quick summary
            verdicts = []
            for t in THEORIES_SHORT:
                if t in result and isinstance(result[t], dict):
                    verdicts.append(result[t].get("verdict", "?"))
            print(f"Verdicts: {'/'.join(verdicts)}")

    # Save raw results
    output_path = "results/experiment2_raw.json"
    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nRaw results saved to {output_path}")

    # Compute agreement matrix
    agreement = compute_agreement_matrix(all_results)
    print("\n" + "=" * 60)
    print("THEORY AGREEMENT MATRIX (proportion of same verdicts)")
    print("=" * 60)
    print(f"{'':>8}", end="")
    for t in THEORIES_SHORT:
        print(f"{t:>8}", end="")
    print()
    for i, t1 in enumerate(THEORIES_SHORT):
        print(f"{t1:>8}", end="")
        for j in range(len(THEORIES_SHORT)):
            print(f"{agreement[i][j]:>8.3f}", end="")
        print()

    # Compute distinguishing rates
    dist_rates = compute_distinguishing_rate(all_results)
    print("\n" + "=" * 60)
    print("DISTINGUISHING PREDICTION RATES")
    print("=" * 60)
    for t in THEORIES_SHORT:
        print(f"  {t}: {dist_rates[t]:.3f}")

    # Per-scenario analysis: which scenarios best distinguish theories?
    scenario_divergence = {}
    for scenario in SCENARIOS:
        scenario_results = [r for r in all_results if r["scenario_id"] == scenario["id"]]
        # Count unique verdicts across theories
        all_verdicts = set()
        for result in scenario_results:
            for t in THEORIES_SHORT:
                if t in result and isinstance(result[t], dict):
                    all_verdicts.add((t, result[t].get("verdict", "?")))
        # Divergence = number of unique verdicts / number of theories
        theory_verdicts = {}
        for result in scenario_results:
            for t in THEORIES_SHORT:
                if t in result and isinstance(result[t], dict):
                    v = result[t].get("verdict", "?")
                    if t not in theory_verdicts:
                        theory_verdicts[t] = []
                    theory_verdicts[t].append(v)

        # Modal verdict per theory
        modal_verdicts = {}
        for t, vs in theory_verdicts.items():
            modal_verdicts[t] = max(set(vs), key=vs.count)

        unique_verdicts = len(set(modal_verdicts.values()))
        scenario_divergence[scenario["id"]] = {
            "unique_verdicts": unique_verdicts,
            "modal_verdicts": modal_verdicts,
            "max_possible": len(THEORIES_SHORT)
        }

    print("\n" + "=" * 60)
    print("SCENARIO DIVERGENCE (higher = theories disagree more)")
    print("=" * 60)
    sorted_scenarios = sorted(scenario_divergence.items(), key=lambda x: -x[1]["unique_verdicts"])
    for sid, info in sorted_scenarios:
        verdicts_str = ", ".join(f"{t}={v}" for t, v in info["modal_verdicts"].items())
        print(f"  {sid}: {info['unique_verdicts']}/{info['max_possible']} unique verdicts")
        print(f"    {verdicts_str}")

    # Save summary
    summary = {
        "agreement_matrix": {
            "theories": THEORIES_SHORT,
            "values": agreement.tolist()
        },
        "distinguishing_rates": dist_rates,
        "scenario_divergence": scenario_divergence,
        "mean_agreement": float(np.mean(agreement[np.triu_indices(len(THEORIES_SHORT), k=1)])),
        "n_scenarios": len(SCENARIOS),
        "n_runs": num_runs,
        "model": MODEL
    }
    summary_path = "results/experiment2_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSummary saved to {summary_path}")

    return summary, all_results


if __name__ == "__main__":
    summary, all_results = run_experiment()

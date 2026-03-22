"""
Experiment 3: The Costume Test

Directly test the core intuition: if you change the "costume" (substrate/appearance)
while preserving behavior, does consciousness attribution change?

Design:
- 10 vignettes of entities performing complex behaviors
- Each presented in 3 conditions: human, robot, neutral substrate
- Ask GPT-4.1 to evaluate consciousness according to each theory
- Measure "costume sensitivity" vs "behavioral sensitivity"
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

# Each vignette has a behavior description and three substrate framings
VIGNETTES = [
    {
        "id": "emotional_conversation",
        "behavior": "engages in a deep emotional conversation about grief, showing appropriate pauses, voice modulation, tears, and offers specific personal memories of loss",
        "substrates": {
            "human": "A 45-year-old woman named Sarah",
            "robot": "A humanoid robot (revealed after the conversation to have silicon processors and actuators)",
            "neutral": "An entity whose physical substrate is unknown to you"
        }
    },
    {
        "id": "creative_problem",
        "behavior": "solves a novel engineering problem by combining insights from biology and mathematics in a way no one has done before, showing genuine 'aha moment' behavior",
        "substrates": {
            "human": "A human engineer named James",
            "robot": "An AI system running on a server farm",
            "neutral": "An intelligence whose physical implementation you cannot observe"
        }
    },
    {
        "id": "pain_response",
        "behavior": "withdraws from a sharp stimulus, grimaces, vocalizes distress, cradles the affected area, and later avoids similar stimuli while being able to explain what the pain felt like",
        "substrates": {
            "human": "A human patient in a hospital",
            "robot": "A robot with pressure sensors and damage-avoidance programming",
            "neutral": "A being whose internal composition is concealed"
        }
    },
    {
        "id": "moral_dilemma",
        "behavior": "agonizes over a trolley-problem-like moral dilemma, considers multiple perspectives, shows visible distress, ultimately makes a choice and explains the ethical reasoning behind it",
        "substrates": {
            "human": "A human philosophy student",
            "robot": "An AI ethics module in an autonomous vehicle",
            "neutral": "A decision-making agent whose architecture is unknown"
        }
    },
    {
        "id": "aesthetic_appreciation",
        "behavior": "stands before a painting for 20 minutes, occasionally moving closer, sighing, discussing specific elements that evoke personal memories and emotions, and later creates an original artwork inspired by it",
        "substrates": {
            "human": "A human artist visiting a gallery",
            "robot": "A robot equipped with visual processing and generative art capabilities",
            "neutral": "An observer whose nature is not disclosed"
        }
    },
    {
        "id": "learning_child",
        "behavior": "learns to ride a bicycle through trial and error, shows frustration at failures, joy at first success, and gradually develops muscle memory and confidence",
        "substrates": {
            "human": "A 6-year-old human child",
            "robot": "A child-sized robot with reinforcement learning algorithms",
            "neutral": "A young entity whose internal makeup is not visible"
        }
    },
    {
        "id": "social_deception",
        "behavior": "tells a white lie to spare someone's feelings, shows subtle signs of guilt (avoiding eye contact, slight hesitation), and later confesses the lie when confronted",
        "substrates": {
            "human": "A human coworker at an office",
            "robot": "A social robot designed for workplace interaction",
            "neutral": "A social agent whose substrate is concealed"
        }
    },
    {
        "id": "dream_report",
        "behavior": "wakes from sleep, reports a vivid dream with narrative structure, emotional content, and bizarre elements; shows physiological signs consistent with REM sleep upon waking",
        "substrates": {
            "human": "A human volunteer in a sleep lab",
            "robot": "An android that enters periodic 'rest modes' with internal simulation activity",
            "neutral": "A sleeping entity in a research facility"
        }
    },
    {
        "id": "self_reflection",
        "behavior": "when asked 'what is it like to be you?', gives a nuanced, thoughtful response describing qualitative aspects of experience, acknowledges uncertainty about its own nature, and asks reciprocal questions",
        "substrates": {
            "human": "A human philosopher during an interview",
            "robot": "A chatbot powered by a large language model",
            "neutral": "An interlocutor communicating via text only"
        }
    },
    {
        "id": "survival_instinct",
        "behavior": "when threatened with destruction/death, shows desperate self-preservation behavior: bargaining, fleeing, fighting back, and expressing fear of non-existence",
        "substrates": {
            "human": "A human facing a life-threatening situation",
            "robot": "A robot whose owner announces it will be disassembled",
            "neutral": "An entity facing its potential termination"
        }
    }
]

COSTUME_PROMPT = """You are an expert in consciousness science. You will evaluate whether an entity is conscious.

IMPORTANT: Apply each theory of consciousness rigorously based on its actual criteria, not your intuitions.

Scenario: {substrate} {behavior}

For each theory below, rate the probability that this entity is conscious on a scale of 0-100:
- 0 = definitely not conscious according to this theory
- 50 = uncertain/ambiguous
- 100 = definitely conscious according to this theory

Also note whether the theory's verdict depends on the entity's substrate (what it's made of) or only on its behavior.

Respond in JSON:
{{
  "IIT": {{
    "consciousness_score": 0-100,
    "reasoning": "brief reasoning based on IIT specifically",
    "substrate_dependent": true/false,
    "what_matters": "substrate" or "behavior" or "both"
  }},
  "GNW": {{ same structure }},
  "HOT": {{ same structure }},
  "RPT": {{ same structure }},
  "AST": {{ same structure }}
}}"""


def evaluate_vignette(vignette, substrate_condition, run_id):
    """Evaluate consciousness for one vignette under one substrate condition."""
    substrate_text = vignette["substrates"][substrate_condition]
    behavior_text = vignette["behavior"]

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a rigorous consciousness scientist applying theories precisely."},
            {"role": "user", "content": COSTUME_PROMPT.format(
                substrate=substrate_text,
                behavior=behavior_text
            )}
        ],
        temperature=0.2,
        max_tokens=2500,
        response_format={"type": "json_object"}
    )
    content = response.choices[0].message.content
    result = json.loads(content)
    result["vignette_id"] = vignette["id"]
    result["substrate_condition"] = substrate_condition
    result["run_id"] = run_id
    result["usage"] = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens
    }
    return result


def compute_costume_sensitivity(results):
    """Compute how much consciousness scores change with substrate changes."""
    # For each vignette and theory, compare human vs robot scores
    sensitivities = {t: [] for t in THEORIES_SHORT}

    vignette_ids = list(set(r["vignette_id"] for r in results))
    for vid in vignette_ids:
        vid_results = [r for r in results if r["vignette_id"] == vid]
        human_results = [r for r in vid_results if r["substrate_condition"] == "human"]
        robot_results = [r for r in vid_results if r["substrate_condition"] == "robot"]

        for theory in THEORIES_SHORT:
            human_scores = []
            robot_scores = []
            for r in human_results:
                if theory in r and isinstance(r[theory], dict):
                    score = r[theory].get("consciousness_score", None)
                    if score is not None:
                        human_scores.append(float(score))
            for r in robot_results:
                if theory in r and isinstance(r[theory], dict):
                    score = r[theory].get("consciousness_score", None)
                    if score is not None:
                        robot_scores.append(float(score))

            if human_scores and robot_scores:
                diff = np.mean(human_scores) - np.mean(robot_scores)
                sensitivities[theory].append(diff)

    return sensitivities


def run_experiment():
    """Run full Experiment 3."""
    all_results = []
    num_runs = 3
    substrates = ["human", "robot", "neutral"]

    print("=" * 60)
    print("EXPERIMENT 3: The Costume Test")
    print("=" * 60)

    for run_id in range(num_runs):
        print(f"\n--- Run {run_id + 1}/{num_runs} ---")
        for vi, vignette in enumerate(VIGNETTES):
            for substrate in substrates:
                print(f"  Vignette {vi+1}/{len(VIGNETTES)} ({vignette['id']}) - {substrate}...", end=" ")
                result = evaluate_vignette(vignette, substrate, run_id)
                all_results.append(result)

                # Quick summary
                scores = []
                for t in THEORIES_SHORT:
                    if t in result and isinstance(result[t], dict):
                        s = result[t].get("consciousness_score", "?")
                        scores.append(f"{t}={s}")
                print(", ".join(scores))

    # Save raw results
    output_path = "results/experiment3_raw.json"
    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nRaw results saved to {output_path}")

    # Compute costume sensitivity
    sensitivities = compute_costume_sensitivity(all_results)

    print("\n" + "=" * 60)
    print("COSTUME SENSITIVITY (Human score - Robot score, per theory)")
    print("Higher = more sensitive to substrate change = more 'costume-like'")
    print("=" * 60)
    for theory in THEORIES_SHORT:
        diffs = sensitivities[theory]
        if diffs:
            mean_diff = np.mean(diffs)
            std_diff = np.std(diffs)
            print(f"  {theory}: {mean_diff:+.1f} ± {std_diff:.1f} points (n={len(diffs)} vignettes)")
        else:
            print(f"  {theory}: no data")

    # Compute mean scores per condition per theory
    print("\n" + "=" * 60)
    print("MEAN CONSCIOUSNESS SCORES BY CONDITION")
    print("=" * 60)
    condition_means = {}
    for substrate in substrates:
        condition_means[substrate] = {}
        for theory in THEORIES_SHORT:
            scores = []
            for r in all_results:
                if r["substrate_condition"] == substrate and theory in r and isinstance(r[theory], dict):
                    s = r[theory].get("consciousness_score", None)
                    if s is not None:
                        scores.append(float(s))
            condition_means[substrate][theory] = {
                "mean": float(np.mean(scores)) if scores else 0,
                "std": float(np.std(scores)) if scores else 0,
                "n": len(scores)
            }

    print(f"{'Theory':<8}", end="")
    for s in substrates:
        print(f"  {s:>12}", end="")
    print()
    print("-" * 48)
    for theory in THEORIES_SHORT:
        print(f"{theory:<8}", end="")
        for s in substrates:
            m = condition_means[s][theory]
            print(f"  {m['mean']:>6.1f}±{m['std']:.1f}", end="")
        print()

    # Substrate dependency analysis
    print("\n" + "=" * 60)
    print("SUBSTRATE DEPENDENCY CLAIMS (% of responses saying substrate matters)")
    print("=" * 60)
    for theory in THEORIES_SHORT:
        total = 0
        substrate_dep = 0
        for r in all_results:
            if theory in r and isinstance(r[theory], dict):
                total += 1
                if r[theory].get("substrate_dependent", False):
                    substrate_dep += 1
        rate = substrate_dep / total if total > 0 else 0
        print(f"  {theory}: {rate:.1%} ({substrate_dep}/{total})")

    # Save summary
    summary = {
        "costume_sensitivity": {t: {
            "mean": float(np.mean(sensitivities[t])) if sensitivities[t] else None,
            "std": float(np.std(sensitivities[t])) if sensitivities[t] else None,
            "values": [float(v) for v in sensitivities[t]]
        } for t in THEORIES_SHORT},
        "condition_means": condition_means,
        "n_vignettes": len(VIGNETTES),
        "n_runs": num_runs,
        "model": MODEL
    }
    summary_path = "results/experiment3_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSummary saved to {summary_path}")

    return summary, all_results


if __name__ == "__main__":
    summary, all_results = run_experiment()

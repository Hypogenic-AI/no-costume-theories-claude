# The "No Costume Theories" Rule

**Research Question**: Are theories of consciousness that rely solely on representational distinctions (without behavioral tests) essentially aesthetic?

## Key Findings

- **IIT is overwhelmingly a "costume theory"**: 92% of its predictions are representational-only (no behavioral test), vs. 20-30% for GNW, HOT, RPT, and AST
- **IIT is the outlier**: It agrees with other theories only 35-45% of the time; the other four agree 65-87%
- **The costume test confirms it**: When behavior is held constant but substrate changes (human to robot), IIT consciousness scores drop 84 points vs. 45-62 for other theories
- **IIT uniquely attributes consciousness to thermostats and denies it to behaviorally identical simulations** — the defining pattern of a "costume theory"
- **The non-IIT theories form a relatively cohesive, behaviorally-grounded cluster**, though none is fully substrate-independent

## Method

Three experiments using GPT-4.1 as a calibrated proxy reasoner:
1. **Prediction Extraction**: Classified predictions from 5 theories as behavioral vs. representational-only
2. **Distinguishability Test**: Applied 5 theories to 20 ambiguous consciousness scenarios
3. **Costume Test**: Evaluated 10 behavioral vignettes under human/robot/neutral substrate conditions

## File Structure

```
├── REPORT.md              # Full research report with results
├── planning.md            # Research plan and methodology
├── literature_review.md   # Pre-gathered literature review
├── resources.md           # Catalog of research resources
├── src/
│   ├── experiment1_prediction_extraction.py
│   ├── experiment2_distinguishability.py
│   ├── experiment3_costume_test.py
│   └── analysis_and_plots.py
├── results/
│   ├── experiment1_raw.json
│   ├── experiment1_summary.json
│   ├── experiment2_raw.json
│   ├── experiment2_summary.json
│   ├── experiment3_raw.json
│   ├── experiment3_summary.json
│   └── plots/
│       ├── experiment1_costume_ratios.png
│       ├── experiment2_distinguishability.png
│       ├── experiment3_costume_test.png
│       └── summary_all_experiments.png
├── papers/                # Downloaded research papers
└── code/                  # Cloned reference repositories
```

## Reproduce

```bash
# Setup
uv venv && source .venv/bin/activate
uv pip install openai numpy pandas matplotlib seaborn scipy

# Run experiments (requires OPENAI_API_KEY)
python src/experiment1_prediction_extraction.py
python src/experiment2_distinguishability.py
python src/experiment3_costume_test.py

# Generate analysis and plots
python src/analysis_and_plots.py
```

## Summary

The "no costume theories" rule is a valid and measurable criterion. IIT fails it decisively. GNW, HOT, RPT, and AST pass it substantially better, though none is perfectly substrate-independent. The principle that "all distinctions must lead to some kind of behavioral test" is operationalizable and reveals meaningful differences among consciousness theories.

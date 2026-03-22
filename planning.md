# Research Plan: The "No Costume Theories" Rule

## Motivation & Novelty Assessment

### Why This Research Matters
The science of consciousness has proliferated dozens of competing theories, but there is no agreed-upon method for deciding between them. If many of these theories differ only in representational vocabulary—without making different behavioral predictions—the field is spending resources on what are essentially aesthetic disagreements. Establishing a principled criterion for dismissing "costume theories" would sharpen the field and focus effort on genuinely testable claims.

### Gap in Existing Work
The literature review reveals that while the *philosophical* arguments for behavioral testability exist (Dennett, the unfolding argument), there has been no **systematic, empirical quantification** of how much of each major theory's content is behaviorally testable vs. purely representational. The ConTraSt database shows method predicts theory allegiance, but nobody has directly measured the "costume ratio" of theories or tested whether LLMs (as proxy reasoners) can actually distinguish theories' behavioral predictions.

### Our Novel Contribution
We conduct three empirical studies using real LLMs:
1. **Behavioral Prediction Overlap Analysis**: Extract and classify predictions from 5 major theories as behavioral vs. representational-only, then quantify overlap
2. **Theory Distinguishability Test**: Present scenarios to LLMs and measure whether different theories actually produce different behavioral predictions
3. **The Costume Test**: Directly test the "robot removes costume" scenario—measuring how much consciousness attribution depends on substrate/appearance vs. behavior

### Experiment Justification
- **Experiment 1** (Prediction Extraction): Needed because no systematic catalog of behavioral vs. representational claims exists across theories. Establishes the baseline "costume ratio."
- **Experiment 2** (Distinguishability): Needed because theories *claim* to differ, but do their predictions actually diverge on concrete scenarios? Uses LLMs as calibrated proxy reasoners.
- **Experiment 3** (Costume Test): Directly operationalizes the core intuition—if you change the "costume" (substrate) while preserving behavior, does consciousness attribution change? Tests whether people/models apply theories consistently.

## Research Question
Do major theories of consciousness make meaningfully different behavioral predictions, or do they differ primarily in representational vocabulary? Can we quantify the "costume ratio" (proportion of purely representational vs. behaviorally testable claims)?

## Background and Motivation
The user's core insight: "I don't think we should have any theories of consciousness where you can be convinced a person is conscious, but then a robot takes off its human costume and then you now think it isn't conscious." This captures a deep methodological principle—all theoretical distinctions must ultimately cash out in behavioral differences, or they are aesthetic.

## Hypothesis Decomposition
1. **H1**: Major consciousness theories (IIT, GNW, HOT, RPT, AST) have high overlap in behavioral predictions
2. **H2**: Theories' unique predictions are predominantly representational/structural rather than behavioral
3. **H3**: When behavioral equivalence is maintained but substrate/appearance changes, consciousness attributions shift—revealing reliance on "costume" features
4. **H4**: The degree to which a theory is a "costume theory" can be quantified

## Proposed Methodology

### Approach
Use GPT-4.1 as a knowledgeable proxy to systematically extract, classify, and compare behavioral predictions across consciousness theories. Then directly test the "costume scenario" with multiple prompting conditions.

### Experimental Steps

**Experiment 1: Behavioral Prediction Extraction**
1. For each of 5 theories (IIT, GNW, HOT, RPT, AST), prompt GPT-4.1 to list specific behavioral predictions
2. Classify each prediction as: (a) unique behavioral, (b) shared behavioral, (c) representational-only
3. Compute "costume ratio" = representational-only / total predictions
4. Repeat 5 times per theory for reliability

**Experiment 2: Theory Distinguishability**
1. Create 20 scenarios where consciousness status is ambiguous (e.g., split-brain, blindsight, AI systems, anesthesia, dreaming)
2. For each scenario, ask GPT-4.1 to predict the behavioral outcome according to each theory
3. Measure prediction agreement across theories using Cohen's kappa and Jaccard similarity
4. Identify which scenarios maximally distinguish theories

**Experiment 3: The Costume Test**
1. Create 10 vignettes describing entities performing complex behaviors
2. Present each vignette in 3 conditions: (a) described as human, (b) described as robot, (c) described neutrally
3. Ask GPT-4.1 to evaluate consciousness according to each theory
4. Measure how much consciousness attribution changes with substrate vs. behavior
5. Run with temperature=0 for determinism, then temperature=0.7 for variance estimation

### Baselines
- Random prediction baseline
- "Always conscious" / "Never conscious" baselines
- Agreement rate if theories were truly equivalent (100% overlap)

### Evaluation Metrics
- **Costume Ratio**: representational-only claims / total claims per theory
- **Prediction Overlap**: Jaccard similarity of behavioral predictions between theory pairs
- **Costume Sensitivity**: change in consciousness attribution when substrate changes but behavior is held constant
- **Behavioral Sensitivity**: change in consciousness attribution when behavior changes but substrate is held constant

### Statistical Analysis Plan
- Cohen's kappa for inter-theory agreement on behavioral predictions
- Paired t-tests for costume sensitivity vs. behavioral sensitivity
- Bootstrap confidence intervals (1000 resamples) for all metrics
- Significance level: α = 0.05

## Expected Outcomes
- H1 supported: >70% overlap in behavioral predictions across theories
- H2 supported: >40% of unique theory content is representational-only
- H3 supported: Costume sensitivity is significantly >0 for substrate-dependent theories (IIT)
- H3 refuted: No theory shows costume sensitivity (all pass the "no costume" test)

## Timeline and Milestones
- Planning: 20 min (this document)
- Environment setup: 10 min
- Experiment 1 implementation & execution: 40 min
- Experiment 2 implementation & execution: 40 min
- Experiment 3 implementation & execution: 30 min
- Analysis & visualization: 30 min
- Documentation: 20 min

## Potential Challenges
- LLM may not perfectly represent each theory's predictions (mitigate: use detailed theory descriptions in prompts)
- Temperature and prompt sensitivity (mitigate: multiple runs, systematic prompting)
- Theories may have genuinely different predictions that LLMs don't capture (mitigate: validate against known distinguishing scenarios from literature)

## Success Criteria
- Clear quantification of costume ratio for each theory
- Statistically significant results on prediction overlap
- At least 3 well-visualized comparisons
- Actionable conclusion about which theories pass the "no costume" test

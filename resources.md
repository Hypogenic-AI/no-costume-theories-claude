# Resources Catalog

## Summary
This document catalogs all resources gathered for the "No Costume Theories" research project examining whether consciousness theories that rely solely on representational distinctions (without behavioral tests) are essentially aesthetic.

## Papers
Total papers downloaded: 14

| Title | Authors | Year | File | Key Info |
|-------|---------|------|------|----------|
| Quining Qualia | Dennett | 1988 | papers/dennett_1988_quining_qualia.pdf | Foundational argument against qualia; supports behavioral testability |
| Zombies and the Explanatory Gap | Chalmers | 2018 | papers/chalmers_zombies_explanatory_gap.pdf | Key counterargument via zombie conceivability |
| On a Confusion about a Function of Consciousness | Block | 1995/1997 | papers/block_1997_access_consciousness.pdf | P-consciousness vs A-consciousness distinction |
| Chalmers' Zombie Argument | Kind | — | papers/kind_chalmers_zombie_argument.pdf | Analysis of zombie argument |
| Two Kinds of Consciousness | Burge | 1997 | papers/burge_1997_two_kinds_consciousness.pdf | Alternative consciousness taxonomy |
| Empirical Support for Higher-Order Theories | Lau & Rosenthal | 2011 | papers/lau_rosenthal_2011_empirical_HOT.pdf | HOT makes testable behavioral predictions |
| Phenomenal Consciousness and Accessibility | Schlicht | — | papers/schlicht_phenomenal_consciousness_access.pdf | Separability of phenomenal from access consciousness |
| Quantifying Empirical Support for ToC | Kirkeby-Hinrup | 2024 | papers/wiese_2024_quantifying_empirical_support.pdf | Bayesian framework for theory comparison |
| Adversarial Collaboration Protocol (COGITATE) | Melloni et al. | 2023 | papers/cogitate_2023_adversarial_protocol.pdf | IIT vs GNW preregistered test protocol |
| ConTraSt Database | Yaron et al. | 2021 | papers/contrast_database_2021.pdf | Meta-analysis: theory allegiance predicted by methods |
| Conscious Perception and PFC | Michel | — | papers/michel_conscious_perception_pfc.pdf | Behavioral markers of consciousness |
| Consciousness in AI | Butlin, Long et al. | 2023 | papers/butlin_2023_consciousness_in_ai.pdf | Indicator properties from theories; behavioral tests insufficient |
| Reflective Analysis on Empirical Theories | — | 2025 | papers/reflective_analysis_2025.pdf | Recent field survey |
| Consciousness Science: Where Are We Going? | — | 2025 | papers/consciousness_science_2025.pdf | Current challenges and directions |

See papers/README.md for detailed descriptions.

### Key Papers Not Downloaded (Paywalled)
- Seth & Bayne (2022) "Theories of Consciousness" — Nature Reviews Neuroscience (major review)
- Doerig et al. (2019) "The Unfolding Argument" — Consciousness and Cognition (critical for the hypothesis)
- Doerig et al. (2021) "Falsification and Consciousness" — Neuroscience of Consciousness
- Melloni et al. (2025) Adversarial testing results — Nature (COGITATE results)
- Tononi et al. (2016) IIT 3.0 foundational paper

## Datasets
Total datasets identified: 2

| Name | Source | Size | Task | Location | Notes |
|------|--------|------|------|----------|-------|
| ConTraSt Database | contrastdb.tau.ac.il | 412 experiments | Theory-evidence meta-analysis | Web-based (no bulk download) | Method predicts theory allegiance |
| ARC-Cogitate Data | osf.io/mbcfy | 256 participants, multi-modal | IIT vs GNW adversarial test | OSF (large neuroimaging data) | Neither theory fully supported |

See datasets/README.md for detailed descriptions and access instructions.

## Code Repositories
Total repositories cloned: 3

| Name | URL | Purpose | Location | Notes |
|------|-----|---------|----------|-------|
| modelling-consciousness | github.com/Xaxis/modelling-consciousness | Formal consciousness quantification system | code/modelling-consciousness/ | Framework for measurable consciousness metrics |
| iit-consciousness | github.com/virgil/consciousness | IIT phi computation | code/iit-consciousness/ | Implements IIT measures; relevant for unfolding argument analysis |
| consciousness-framework | github.com/KarolFilipKowalczyk/Consciousness | Multi-theory comparison framework | code/consciousness-framework/ | Integrates IIT, GWT, AST; includes theory comparison appendix |

See code/README.md for detailed descriptions.

## Resource Gathering Notes

### Search Strategy
1. Used web search across multiple academic databases (arXiv, Semantic Scholar, Google Scholar, PubMed)
2. Targeted searches for: falsifiability of consciousness theories, behavioral testability, representational theories, zombie arguments, adversarial collaboration, ConTraSt database, IIT criticisms, higher-order theories empirical support
3. Downloaded open-access papers directly; documented paywalled papers for reference
4. Cloned GitHub repositories related to consciousness theory implementation and comparison

### Selection Criteria
- Papers directly addressing testability/falsifiability of consciousness theories
- Foundational philosophical arguments (Dennett, Chalmers, Block) defining the debate
- Empirical methodology papers (adversarial collaboration, meta-analysis)
- Papers showing theories making (or failing to make) distinct behavioral predictions
- Code repositories implementing theory-specific computational measures

### Challenges Encountered
- Several key papers are behind paywalls (especially Seth & Bayne 2022, Doerig et al. 2019)
- ConTraSt database has no bulk data export; data must be explored via web interface
- The research topic is primarily philosophical/theoretical; traditional "datasets" are limited
- The most critical paper for the hypothesis (Doerig et al. 2019 "Unfolding Argument") could not be downloaded

### Gaps and Workarounds
- For paywalled papers, relied on abstracts, web summaries, and citing papers for key arguments
- For ConTraSt database, documented the published findings about methodological prediction of theory allegiance
- For the unfolding argument, used the extensive discussion in available secondary sources

## Recommendations for Experiment Design

Based on gathered resources, recommend:

1. **Primary approach**: Philosophical/conceptual analysis rather than empirical experiment
   - Systematically compare behavioral predictions across theories
   - Formalize the "costume theory" concept and propose testable criteria

2. **Analytical framework**:
   - Use Kirkeby-Hinrup's QBE framework to quantify empirical content of theories
   - Apply the unfolding argument template to each major theory
   - Analyze ConTraSt database findings as evidence for the hypothesis

3. **Evaluation metrics**:
   - Number of unique behavioral predictions per theory
   - Degree of prediction overlap between theories
   - Ratio of representational claims to behavioral predictions
   - Predictive accuracy in adversarial collaboration settings

4. **Code to adapt/reuse**:
   - IIT phi computation (code/iit-consciousness/) for demonstrating unfolding argument
   - Consciousness framework comparisons (code/consciousness-framework/) for structured theory comparison

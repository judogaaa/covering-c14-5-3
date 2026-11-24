# The covering number C(14,5,3)

**Public research draft — 24 November 2026**

This project investigates the minimum number of five-element subsets of a fourteen-element set needed to cover every three-element subset. The proposed result is $C(14,5,3)=43$.

**Publication status:** initial import. The full computer-assisted lower-bound proof and its reproducibility package have been prepared locally; the complete set of sources and certificates is not yet present in this GitHub repository. The equality should be treated as a candidate pending review of the complete package. No claim of scientific priority or independent peer review is made.

An explicit 43-block construction, which establishes the upper bound, and its standalone checker are being imported. The lower-bound approach combines exhaustive local-link enumeration, exact integer inequalities and residual search. Verification of the upper bound alone is not a proof of optimality.

## Reproducibility and review

Once the full package has been imported, start with `PROOF.md`, `AUDIT.md` and `REPRODUCIBILITY.md`. The intended full verification command is `python3 -u audit.py` (Python 3.10+ and a C++17 compiler). A successful run is computational evidence, not formal verification or independent mathematical refereeing.

This is an AI-assisted investigation. ChatGPT contributed reasoning, code and computational checks; Gemini and DeepSeek supplied additional candidate arguments. The project maintainer is the GitHub account `judogaaa`. Confirmed publication-author metadata, licensing, and priority assessment are pending. Please use GitHub Issues for reproducible findings and corrections.

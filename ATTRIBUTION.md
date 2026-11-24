# Attribution and related work

## Authorship and disclosure

Generative language-model tools contributed substantially to mathematical reasoning, algorithm design, implementation, debugging, proof writing and computational checks. These tools also supplied candidate arguments that were critically reviewed and corrected where appropriate. This disclosure describes the research process; the computational checks are not independent human peer review.

The human author's preferred publication name, affiliations (if any), and precise contribution statement remain to be confirmed for formal publication. Do not infer authorship from GitHub account information. No scientific priority claim is made here. A license for the original code and prose and full citation metadata should be selected by the rights holder. The historical data are attributed separately.

## Related sources cited by the research draft

The following source links were used in the investigation. The two GitHub documents below were rechecked on 24 November 2026; no comprehensive priority search has been completed.

- Rob Gardiner, structural lower-bound work: <https://github.com/renidrag/covering/blob/main/coverings/14-5-3/proof.md>. The earlier draft used the removable-block lemma; the current main proof instead supplies its own finite verification of that lemma. Git blob `02880132c5320e678beca7a0a9854a5d90a29cde`. See `two_low/PREVIOUS_PROOF.md` for historical context. Gardiner credits Sharad S. Sane, “On Affine and Projective Failed Designs,” JCMCC 9 (1991), 209–219, for the general deletion antecedent; the current enumeration proves the needed special case independently of that premise.
- Related computer-assisted covering proof package: <https://github.com/dennisonbertram/covering-number-c12-6-4>. Cited as methodological inspiration; README Git blob `182bee139186973eeaefaf52de67fd9695e225c9`.
- The previously suggested arXiv identifier 2610.31696 has not been verified here and is not relied upon for any proof step.

Before formal submission, verify each reference against its original source, record exact versions or commit identifiers when available, and review the provenance of the explicit upper-bound construction in [data/UPPER_WITNESS_PROVENANCE.md](data/UPPER_WITNESS_PROVENANCE.md). Do not claim that a cited result or a reused construction originated in this project unless verified.

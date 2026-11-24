# Release checklist

Suggested GitHub repository name: `covering-c14-5-3`.

Suggested description: `Candidate computer-assisted proof of C(14,5,3)=43, with exhaustive enumeration and exact integer certificates. Pending independent review.`

1. Confirm the human author's publication name, contribution statement, and any affiliations. Review the research-provenance disclosure in `ATTRIBUTION.md`.
2. Review [LICENSE](LICENSE) for the original copyrightable materials and the separate source-data terms for the historical upper-bound witness. Confirm rights for any additional third-party materials before redistributing them.
3. Verify the related-work bibliography, provenance of the construction, and scientific priority separately from proof correctness.
4. Initialize the repository and run the supplied verifier on a clean checkout. Record the commit ID, environment, and logs. The maintainer has requested a public repository.
5. After reviewing the results, invite independent mathematical review. Do not describe a passing CI job as peer review or formal verification.
6. For a public release, select a version tag, add confirmed citation metadata, and archive that immutable revision (e.g., through a research-data archive if desired). Do not claim a DOI until one is issued.

## Updating the public repository

The public destination is https://github.com/judogaaa/covering-c14-5-3. Import the full verified tree on top of the existing `main` history, without a force-push. Check the Actions tab for `Reproduce covering proof`. Record the exact revision, environment and logs; a successful CI run is not peer review.

Do not tag the research as final or make a novelty claim until the bibliography, mathematical reductions, code and independent review have been checked. The repository is public for research verification; the original copyrightable materials are not released under an open-source license. See [LICENSE](LICENSE). The Zenodo v1 preprint DOI is [10.5281/zenodo.24514296](https://doi.org/10.5281/zenodo.24514296), and its identified research revision is `5811830`. Subsequent metadata-only changes do not modify that archived revision.

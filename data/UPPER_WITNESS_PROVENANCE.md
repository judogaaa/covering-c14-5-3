# Provenance of the upper-bound witness

The 43-block construction is not new. It is a relabeling of the historical construction credited to Nurmela and Östergård (simulated annealing, repository date 1 December 1996).

Source data: Daniel M. Gordon, *La Jolla Coverings Repository*, version 1.2, [Zenodo record 19735294](https://zenodo.org/records/19735294), CC BY 4.0 according to [Gardiner's source notes](https://github.com/renidrag/covering/blob/main/coverings/14-5-3/sources.md). The data were retrieved from [the historical witness JSON](https://github.com/renidrag/covering/blob/main/data/c1453-historical-witness.json), Git blob `4ffc77ba38828a7b1a8d4775103d7402a8ccd4d7`. Original one-byte labels have SHA-256 `173772ab8d73847ff258f4f5ae2859d0fbe7e312483e1afc23d58c721bd22f93`.

The explicit relabeling sends historical labels 1–14 respectively to:

```
14 10 4 9 6 11 2 3 13 8 1 12 7 5
```

The standalone checker verifies that the original labels have the specified digest and that the permutation maps the historical family to the current family. The data license is separate from the original proof and code; no license for those materials has been finalized.

# Provenance of the 43-block upper-bound witness

The construction used here is **not new**. It is isomorphic to the historical 43-block construction credited to Nurmela and Östergård (simulated annealing; repository date 1 December 1996). We retain the current labels for compatibility with the verification code.

Source data: Daniel M. Gordon, *La Jolla Coverings Repository*, version 1.2, [Zenodo record 19735294](https://zenodo.org/records/19735294), CC BY 4.0 as identified in [Gardiner's provenance notes](https://github.com/renidrag/covering/blob/main/coverings/14-5-3/sources.md). The preserved historical data were retrieved from [Gardiner's historical witness JSON](https://github.com/renidrag/covering/blob/main/data/c1453-historical-witness.json) (Git blob `4ffc77ba38828a7b1a8d4775103d7402a8ccd4d7`, checked 24 November 2026). `historical43_blocks.txt` transcribes its one-based ordered blocks to plain text. The SHA-256 digest of the original 215 one-byte labels is `173772ab8d73847ff258f4f5ae2859d0fbe7e312483e1afc23d58c721bd22f93`.

The explicit relabeling sends historical labels 1 through 14 to, respectively:

```
14 10 4 9 6 11 2 3 13 8 1 12 7 5
```

Applying this permutation to every historical block gives exactly the unordered set of blocks in `../upper43_blocks.txt`. `../verify_upper.py` verifies the source label digest, permutation, block correspondence and all 364 triples. The data license applies to the historical witness and its relabeling, not automatically to the other code and prose in this repository.

The proposed contribution of this project concerns the lower bound excluding 42 blocks, not the upper-bound construction. Priority for that lower bound remains unestablished.

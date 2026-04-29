# lsis-afs-artifacts
LunaNet Signal-In-Space Recommended Standard – Augmented Forward Signal (LSIS – AFS). 

Reference Implementation Artifacts for **Cross-implementation** comparison

## How to use

Clone repo:
```
git clone https://github.com/s59mz/lsis-afs-artifacts
cd lsis-afs-artifacts
```

Note our generated Code Vectors:

```
ls ./artifacts/code_vectors/
```

Edit ***scripts/compare_codes.sh*** file to set the path to your own generated hex Code Vectors:

`python3 -m scripts.compare_code_vectors artifacts/code_vectors /path/to/other/developer/code_vectors`

Run compare code script:

```
./scripts/compare_codes.sh
```

## How the result should look

```

Compared:  210 files
Mismatches: 0
```

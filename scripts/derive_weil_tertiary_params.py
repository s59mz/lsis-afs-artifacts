# Run this script to generate Weil tertiary shift parameters
# 
#  python -u -m scripts.derive_weil_tertiary_params | tee >(grep -vi "##" >  artifacts/derived_params/weil_tertiary_params.csv)
# 
# Compare the output with the reference config CSV file:
#  diff artifacts/derived_params/weil_tertiary_params.csv config/spec_tables/appendix_e_weil_tertiary_params.csv
#

import numpy as np

from lsis_afs.primitives.sequences.legendre import generate_legendre
from lsis_afs.validation.annex3 import load_weil_tertiary_reference


def find_k_for_prn(prn: int) -> int:
    p = 1499
    L = generate_legendre(p)
    ref = load_weil_tertiary_reference(prn)  # length 1500

    ref_core = ref[:p]  # remove appended 0

    idx = np.arange(p)

    for k in range(1, (p - 1) // 2 + 1):
        Lk = L[(idx + k) % p]
        candidate = L ^ Lk

        if np.array_equal(candidate, ref_core):
            return k

    raise ValueError(f"No match found for PRN {prn}")


def main():
    results = {}

    for prn in range(1, 211):
        k = find_k_for_prn(prn)
        print(f"## PRN {prn:3d} -> k = {k}")
        results[prn] = k

    print("# These Parameters were extracted from Reference Codes by")
    print("#   derive_weil_tertiary_params.py utility script for testing purposes only")
    print("#")

    print("# LSIS-AFS Appendix E: Weil Tertiary Code Parameters (Tables E-2..E-6)")
    print("# Legendre length: 1499 (prime)")
    print("# Output code length: 1500 chips (1499 Weil + 1 appended zero)")
    print("# W(t;k) = L(t) XOR L((t+k) mod 1499), append 0 at position 1499")

    print("prn,weil_index_k")

    for prn, k in results.items():
        print(f"{prn},{k}")


if __name__ == "__main__":
    main()

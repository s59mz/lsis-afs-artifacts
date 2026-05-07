# Run this script to generate Weil primary shift parameters
#
#  python -u -m scripts.derive_weil_primary_params | tee >(grep -vi "##" >  artifacts/derived_params/weil_primary_params.csv)
#
# Compare the output with the reference config CSV file:
#  diff artifacts/derived_params/weil_primary_params.csv config/spec_tables/appendix_d_weil_primary_params.csv
#
# WARNING: multiple matches for PRN 114: [(3079, 76), (3979, 83)]
# WARNING: multiple matches for PRN 117: [(5088, 5548), (5088, 5555)]
#

import numpy as np

from lsis_afs.primitives.sequences.legendre import generate_legendre
from lsis_afs.validation.annex3 import load_weil_primary_reference


EXPANSION = np.array([0, 1, 1, 0, 1, 0, 0], dtype=np.uint8)


def try_candidate(L, ref, insert_idx):
    """
    Try removing expansion at insert_idx and solve for k.
    """
    p = len(L)

    # remove expansion
    base = np.concatenate([ref[:insert_idx], ref[insert_idx + 7:]])

    if len(base) != p:
        return None

    idx = np.arange(p)

    for k in range(1, (p - 1) // 2 + 1):
        Lk = L[(idx + k) % p]
        candidate = L ^ Lk

        if np.array_equal(candidate, base):
            return k

    return None


def find_params_for_prn(prn: int):
    p = 10223

    L = generate_legendre(p)
    ref = load_weil_primary_reference(prn)

    matches = []

    for i in range(len(ref) - 6):
        if not np.array_equal(ref[i:i+7], EXPANSION):
            continue

        k = try_candidate(L, ref, i)

        if k is not None:
            matches.append((k, i))
            break

    if len(matches) == 0:
        raise ValueError(f"No valid (k, insert_idx) found for PRN {prn}")

    if len(matches) > 1:
        print(f"WARNING: multiple matches for PRN {prn}: {matches}")

    k, insert_idx = matches[0]

    # convert to spec (1-based)
    return k, insert_idx + 1


def main():
    results = {}

    for prn in range(1, 211):
        k, insert_idx = find_params_for_prn(prn)
        print(f"## PRN {prn:3d} → k={k}, insert_idx={insert_idx}")
        results[prn] = (k, insert_idx)

    print("# These Parameters were extracted from Reference Codes by")
    print("#   derive_weil_primary_params.py utility script for testing purposes only")
    print("#")

    print("# LSIS-AFS Appendix D: Weil Primary Code Parameters (Tables D-2..D-6)")
    print("# Legendre length: 10223 (prime)")
    print("# Output code length: 10230 chips (10223 + 7 expansion)")
    print("# Expansion sequence: [0 1 1 0 1 0 0]")
    print("# W(t;k) = L(t) XOR L((t+k) mod 10223), insert expansion at index p")

    print("prn,weil_index_k,insertion_index_p")

    for prn, (k, idx) in results.items():
        print(f"{prn},{k},{idx}")


if __name__ == "__main__":
    main()


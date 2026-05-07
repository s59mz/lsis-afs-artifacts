# Run this script to generate Gold Code shift parameters
#
#  python -u -m scripts.derive_gold_params | tee >(grep -vi "##" >  artifacts/derived_params/gold_params.csv)
#
# Compare the output with the reference config CSV file:
#  diff artifacts/derived_params/gold_params.csv config/spec_tables/appendix_c_gold_g2_delays.csv 
#

import numpy as np

from lsis_afs.primitives.sequences.gold import _lfsr_sequence
from lsis_afs.primitives.sequences.gold import generate_gold
from lsis_afs.validation.annex3 import load_gold_reference


def find_shift_for_prn(prn: int) -> int:
    G1_TAPS = [11, 2]
    G2_TAPS = [11, 8, 5, 2]

    seed = np.ones(11, dtype=np.uint8)

    g1 = _lfsr_sequence(G1_TAPS, seed, 2047)
    g2 = _lfsr_sequence(G2_TAPS, seed, 2047)

    ref = load_gold_reference(prn)

    for shift in range(len(g2)):
        gold = g1 ^ np.roll(g2, shift)
        gold = gold[:2046]

        if np.array_equal(gold, ref):
            return shift

    raise ValueError("No matching shift found")


def main():
    results = {}

    for prn in range(1, 211):
        k = find_shift_for_prn(prn)
        print(f"## PRN {prn:3d} -> k = {k}")
        results[prn] = k

    print("# These Parameters were extracted from Reference Codes by")
    print("#   derive_gold_params.py utility script for testing purposes only")
    print("#")

    print("# LSIS-AFS Appendix C: Gold Code G2 Delays (Tables C-1..C-5)")
    print("# Generator polynomials:")
    print("#   g1(x) = x^11 + x^2 + 1")
    print("#   g2(x) = x^11 + x^8 + x^5 + x^2 + 1")
    print("# Code length: 2046 chips (short-cycled from 2047)")
    print("# Both LFSRs initialised to all-1s; G2 pre-advanced by delay D_k")

    print("prn,g2_delay")

    for prn, k in results.items():
        print(f"{prn},{k}")


if __name__ == "__main__":
    main()

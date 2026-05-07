#!/bin/bash
#
# export Gold, Weil-Primary, Weil-Tertiary and Secondary codes in hex format
#   into: artefacts/code_vectors directory
#
# For compare generated codes to references repo, use:
#    diff -rB -I '^#' artifacts/code_vectors/ ../lsis-afs-test-vectors/codes/
#    ./scripts/compare_codes.sh
#

python3 -m scripts.export_code_vectors
diff -rB -I '^#' artifacts/code_vectors/ ../lsis-afs-test-vectors/codes/


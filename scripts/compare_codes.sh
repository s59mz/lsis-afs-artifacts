#!/bin/bash
#
#  Compare generated code vector files between two directories.
#  Returns number of mismatched files
#
# Use: python3 -m scripts.compare_code_vectors artifacts/code_vectors /path/to/other/developer/code_vectors
#

python3 -m scripts.compare_code_vectors artifacts/code_vectors ../luar-space/lsis-afs-test-vectors/codes


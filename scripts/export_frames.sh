#!/bin/bash
#
# Export test frame messages into: artefacts/frame_vectors directory
#
# Message 1: all zeros
# Message 2: all ones
# Message 3: alternating bits, start with 1 (0xAA)
# Message 4: bytewise marker.
#     Each subframe restarts marker from byte 0x00.
# Message 5: xorshift32 PRNG, seed 0xAF52.
#     One continuous stream across SB2 -> SB3 -> SB4.
# Boundary frame:
#     alternating bits, start with 0 (0x55), header maxima.
# Boundary max fields:
#     All-ones SB2/SB3/SB4 with SB2[13..21] (ITOW field) clamped to 503 spec max;
#     FID=3, TOI=99, PRN=210
#     WN=8191, ITOW=503 maxima
#
# For compare frames to references one, use: 
#    python -m scripts.export_frames_from_inputs
#    diff -r artifacts/frame_vectors artifacts/frame_vectors_from_inputs/
#    diff -r artifacts/frame_vectors ../lsis-afs-test-vectors/frames/
#

python3 -m scripts.export_frame_vectors
diff -r artifacts/frame_vectors ../lsis-afs-test-vectors/frames/


from pathlib import Path

import numpy as np

from lsis_afs.io.frame import write_frame_binary
from lsis_afs.protocol.frame import (
    SB2_PAYLOAD_BITS,
    SB34_PAYLOAD_BITS,
    build_fid0_frame_from_payloads,
)

OUT_DIR = Path("artifacts/frame_vectors")


def apply_sb2_spare_pattern(payload: np.ndarray) -> np.ndarray:
    """
    Apply LSIS-AFS SB2 spare-bit pattern.

    SB2 bits 1150..1175 inclusive are filled with alternating 0/1,
    starting with 0.
    """
    payload = payload.copy()
    payload[1150:1176] = (np.arange(26) % 2).astype(np.uint8)
    return payload


def all_zeros(length: int) -> np.ndarray:
    return np.zeros(length, dtype=np.uint8)


def all_ones(length: int) -> np.ndarray:
    return np.ones(length, dtype=np.uint8)


def alternating_bits(length: int, start_bit: int) -> np.ndarray:
    """
    Generate alternating bits.

    start_bit=1 -> 10101010... (0xAA)
    start_bit=0 -> 01010101... (0x55)
    """
    assert start_bit in (0, 1)
    return ((np.arange(length) + start_bit) % 2).astype(np.uint8)


def bytewise_marker_bits(length: int) -> np.ndarray:
    """
    Generate bytewise marker bits.

    bit i is the MSB-first bit of byte (i // 8) mod 256.
    Each subframe should call this independently, so the marker restarts
    from byte 0x00 for SB2, SB3, and SB4.
    """
    byte_index = (np.arange(length) // 8) % 256
    bit_index = np.arange(length) % 8
    return ((byte_index >> (7 - bit_index)) & 1).astype(np.uint8)


def xorshift32_bits(length: int, seed: int = 0xAF52) -> np.ndarray:
    """
    Generate xorshift32 bitstream.

    Matches CORRECTNESS.md:
        state ^= state << 13
        state ^= state >> 17
        state ^= state << 5
        bit = state & 1
    """
    state = np.uint32(seed)
    out = np.empty(length, dtype=np.uint8)

    for i in range(length):
        state ^= np.uint32(state << np.uint32(13))
        state ^= np.uint32(state >> np.uint32(17))
        state ^= np.uint32(state << np.uint32(5))
        out[i] = np.uint8(state & np.uint32(1))

    return out


def export_frame(
    name: str,
    sb2_payload: np.ndarray,
    sb3_payload: np.ndarray,
    sb4_payload: np.ndarray,
    fid: int = 0,
    toi: int = 0,
    node_id: int = 1,
) -> None:
    frame = build_fid0_frame_from_payloads(
        fid=fid,
        toi=toi,
        sb2_payload=apply_sb2_spare_pattern(sb2_payload),
        sb3_payload=sb3_payload,
        sb4_payload=sb4_payload,
    )

    path = OUT_DIR / f"frame_{name}.bin"
    write_frame_binary(path, frame, node_id=node_id)
    print(f"Wrote {path}")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Message 1: all zeros
    export_frame(
        "message_1",
        all_zeros(SB2_PAYLOAD_BITS),
        all_zeros(SB34_PAYLOAD_BITS),
        all_zeros(SB34_PAYLOAD_BITS),
    )

    # Message 2: all ones
    export_frame(
        "message_2",
        all_ones(SB2_PAYLOAD_BITS),
        all_ones(SB34_PAYLOAD_BITS),
        all_ones(SB34_PAYLOAD_BITS),
    )

    # Message 3: alternating bits, start with 1 (0xAA)
    export_frame(
        "message_3",
        alternating_bits(SB2_PAYLOAD_BITS, start_bit=1),
        alternating_bits(SB34_PAYLOAD_BITS, start_bit=1),
        alternating_bits(SB34_PAYLOAD_BITS, start_bit=1),
    )

    # Message 4: bytewise marker.
    # Each subframe restarts marker from byte 0x00.
    export_frame(
        "message_4",
        bytewise_marker_bits(SB2_PAYLOAD_BITS),
        bytewise_marker_bits(SB34_PAYLOAD_BITS),
        bytewise_marker_bits(SB34_PAYLOAD_BITS),
    )

    # Message 5: xorshift32 PRNG, seed 0xAF52.
    # One continuous stream across SB2 -> SB3 -> SB4.
    prng = xorshift32_bits(
        SB2_PAYLOAD_BITS + 2 * SB34_PAYLOAD_BITS,
        seed=0xAF52,
    )

    sb2 = prng[:SB2_PAYLOAD_BITS]
    sb3 = prng[SB2_PAYLOAD_BITS : SB2_PAYLOAD_BITS + SB34_PAYLOAD_BITS]
    sb4 = prng[SB2_PAYLOAD_BITS + SB34_PAYLOAD_BITS :]

    export_frame("message_5", sb2, sb3, sb4)

    # Boundary frame:
    # alternating bits, start with 0 (0x55), header maxima.
    export_frame(
        "boundary",
        alternating_bits(SB2_PAYLOAD_BITS, start_bit=0),
        alternating_bits(SB34_PAYLOAD_BITS, start_bit=0),
        alternating_bits(SB34_PAYLOAD_BITS, start_bit=0),
        fid=3,
        toi=99,
        node_id=210,
    )


if __name__ == "__main__":
    main()

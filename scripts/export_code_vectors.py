from datetime import datetime, timezone
from pathlib import Path

from lsis_afs.io.bitstream import bits_to_hex
from lsis_afs.primitives.sequences.gold import generate_gold
from lsis_afs.primitives.sequences.secondary import generate_secondary

from lsis_afs.primitives.sequences.weil import (
    generate_weil_primary,
    generate_weil_tertiary,
)


OUT_DIR = Path("artifacts/code_vectors")


def export_prn(prn: int) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    path = OUT_DIR / f"codes_prn{prn:03}.hex"
    # timestamp = datetime.now(timezone.utc).isoformat()
    timestamp = datetime.fromtimestamp(1738108800, timezone.utc).isoformat()

    gold = generate_gold(prn)
    weil_primary = generate_weil_primary(prn)
    weil_tertiary = generate_weil_tertiary(prn)

    secondary_ids = ["S0", "S1", "S2", "S3"]

    with path.open("w", encoding="utf-8") as f:
        f.write("# LSIS-AFS Code Test Vector\n")
        f.write(f"# PRN: {prn}\n")
        f.write(f"# Generated: {timestamp}\n\n")

        f.write("[GOLD_CODE]\n")
        f.write(f"length: {len(gold)}\n")
        f.write(f"hex: {bits_to_hex(gold)}\n\n")

        f.write("[WEIL_PRIMARY]\n")
        f.write(f"length: {len(weil_primary)}\n")
        f.write(f"hex: {bits_to_hex(weil_primary)}\n\n")

        f.write("[WEIL_TERTIARY]\n")
        f.write(f"length: {len(weil_tertiary)}\n")
        f.write(f"hex: {bits_to_hex(weil_tertiary)}\n\n")

        for sid in secondary_ids:
            seq = generate_secondary(sid)
            f.write(f"[SECONDARY_{sid}]\n")
            f.write(f"hex: {bits_to_hex(seq)}\n\n")

    return path


def main():
    for prn in range(1, 211):
        path = export_prn(prn)
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()

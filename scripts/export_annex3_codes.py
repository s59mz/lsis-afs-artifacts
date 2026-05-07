from pathlib import Path

from lsis_afs.primitives.sequences.gold import generate_gold
from lsis_afs.primitives.sequences.weil import (
    generate_weil_primary,
    generate_weil_tertiary,
)
from lsis_afs.io.bitstream import bits_to_hex


OUT = Path("artifacts/annex3_export")
OUT.mkdir(parents=True, exist_ok=True)


def export_set(name, generator, length):
    file = OUT / f"{name}.txt"

    with open(file, "w") as f:
        f.write(f"{name} = [ \\\n")

        for prn in range(1, 211):
            seq = generator(prn)
            hex_str = bits_to_hex(seq)

            f.write(f'"{hex_str}",\n')

        f.seek(f.tell() - 2)
        f.write("]\n")


def main():
    export_set("GoldCode2046", generate_gold, 2046)
    export_set("WeilPrimary10230", generate_weil_primary, 10230)
    export_set("WeilTertiary1500", generate_weil_tertiary, 1500)


if __name__ == "__main__":
    main()


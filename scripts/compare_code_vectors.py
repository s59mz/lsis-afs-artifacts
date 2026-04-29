from pathlib import Path
import argparse
import sys


def read_normalized(path: Path) -> str:
    """
    Read a code-vector file and normalize it for comparison.

    This ignores:
    - comment lines
    - blank lines
    - whitespace differences
    """
    lines = []

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith("#"):
            continue

        lines.append(line)

    return "\n".join(lines)


def compare_dirs(reference_dir: Path, candidate_dir: Path) -> int:
    """
    Compare generated code vector files between two directories.

    Returns number of mismatched files.
    """
    mismatches = 0

    reference_files = sorted(reference_dir.glob("codes_prn*.hex"))

    if not reference_files:
        raise RuntimeError(f"No codes_prn*.hex files found in {reference_dir}")

    for ref_file in reference_files:
        cand_file = candidate_dir / ref_file.name

        if not cand_file.exists():
            print(f"[MISSING] {cand_file}")
            mismatches += 1
            continue

        ref_text = read_normalized(ref_file)
        cand_text = read_normalized(cand_file)

        if ref_text != cand_text:
            print(f"[DIFF] {ref_file.name}")
            mismatches += 1
        #else:
        #    print(f"[OK]   {ref_file.name}")

    print()
    print(f"Compared:  {len(reference_files)} files")
    print(f"Mismatches: {mismatches}")

    return mismatches


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare LSIS-AFS generated code vector directories."
    )

    parser.add_argument(
        "reference_dir",
        type=Path,
        help="Directory containing local/reference codes_prn*.hex files",
    )

    parser.add_argument(
        "candidate_dir",
        type=Path,
        help="Directory containing candidate codes_prn*.hex files",
    )

    args = parser.parse_args()

    return compare_dirs(args.reference_dir, args.candidate_dir)


if __name__ == "__main__":
    sys.exit(main())


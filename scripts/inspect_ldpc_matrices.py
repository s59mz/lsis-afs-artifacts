from pathlib import Path
import csv


FILES = [
    "003a_lunanet_sf2_ldpc_submatrix_a_ind.csv",
    "003c_lunanet_sf2_ldpc_submatrix_b_inv_ind.csv",
    "003d_lunanet_sf2_ldpc_submatrix_c_ind.csv",
    "003e_lunanet_sf2_ldpc_submatrix_d_ind.csv",
    "003f_lunanet_sf3_ldpc_submatrix_a_ind.csv",
    "003h_lunanet_sf3_ldpc_submatrix_b_inv_ind.csv",
    "003i_lunanet_sf3_ldpc_submatrix_c_ind.csv",
    "003j_lunanet_sf3_ldpc_submatrix_d_ind.csv",
]


def inspect(path: Path):
    max_r = -1
    max_c = -1
    count = 0

    with path.open("r", encoding="utf-8") as f:
        reader = csv.reader(line for line in f if not line.startswith("#"))

        for row in reader:
            if not row:
                continue

            r = int(row[0])
            c = int(row[1])

            max_r = max(max_r, r)
            max_c = max(max_c, c)
            count += 1

    return max_r + 1, max_c + 1, count


def main():
    base = Path("tests/vectors/annex1/matrices")

    for name in FILES:
        rows, cols, nnz = inspect(base / name)
        print(f"{name}: shape≈({rows}, {cols}), ones={nnz}")


if __name__ == "__main__":
    main()


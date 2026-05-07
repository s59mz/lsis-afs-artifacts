from pathlib import Path

from lsis_afs.io.frame import write_frame_binary
from lsis_afs.io.frame_inputs import read_frame_input_file
from lsis_afs.protocol.frame import build_fid0_frame_from_payloads


INPUT_DIR = Path("../lsis-afs-test-vectors/inputs")
OUT_DIR = Path("artifacts/frame_vectors_from_inputs")

FRAME_TIMESTAMP = 1738108800


FRAME_METADATA = {
    "frame_message_1_input.bin": {"out": "frame_message_1.bin", "prn": 1, "fid": 0, "toi": 0},
    "frame_message_2_input.bin": {"out": "frame_message_2.bin", "prn": 1, "fid": 0, "toi": 0},
    "frame_message_3_input.bin": {"out": "frame_message_3.bin", "prn": 1, "fid": 0, "toi": 0},
    "frame_message_4_input.bin": {"out": "frame_message_4.bin", "prn": 1, "fid": 0, "toi": 0},
    "frame_message_5_input.bin": {"out": "frame_message_5.bin", "prn": 1, "fid": 0, "toi": 0},
    "frame_boundary_input.bin": {"out": "frame_boundary.bin", "prn": 210, "fid": 3, "toi": 99},
    "frame_boundary_max_fields_input.bin": {"out": "frame_boundary_max_fields.bin", "prn": 210, "fid": 3, "toi": 99},
}


def export_one(input_path: Path, meta: dict) -> Path:
    sb2, sb3, sb4 = read_frame_input_file(input_path)

    frame = build_fid0_frame_from_payloads(
        fid=meta["fid"],
        toi=meta["toi"],
        sb2_payload=sb2,
        sb3_payload=sb3,
        sb4_payload=sb4,
    )

    out_path = OUT_DIR / meta["out"]

    write_frame_binary(
        out_path,
        frame,
        node_id=meta["prn"],
        timestamp=FRAME_TIMESTAMP,
    )

    return out_path


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for input_name, meta in FRAME_METADATA.items():
        input_path = INPUT_DIR / input_name

        if not input_path.exists():
            raise FileNotFoundError(input_path)

        out_path = export_one(input_path, meta)
        print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()


"""Recreate the exact original fixed train/val/test CSVs. Standard library only."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path

def main():
    root=Path(__file__).resolve().parent
    parser=argparse.ArgumentParser()
    parser.add_argument("--output-dir",type=Path,default=root/"restored_splits")
    args=parser.parse_args()
    manifest=json.loads((root/"package_manifest.json").read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True,exist_ok=True)
    for split,info in manifest["splits"].items():
        path=args.output_dir/f"{split}.csv"
        temporary=path.with_suffix(".csv.part")
        if path.exists() or temporary.exists():
            raise FileExistsError(f"Refusing to overwrite {path}")
        result=hashlib.sha256()
        with temporary.open("wb") as writer:
            for i,part in enumerate(info["parts"]):
                p=root/part["path"]
                if hashlib.sha256(p.read_bytes()).hexdigest()!=part["sha256"]:
                    raise ValueError(f"Damaged shard: {p}")
                with gzip.open(p,"rb") as reader:
                    header=reader.readline()
                    if header!=b"\xef\xbb\xbfsource,game_id,title,description,genres\n":
                        raise ValueError("Unexpected shard header")
                    if i==0:
                        writer.write(header)
                        result.update(header)
                    for block in iter(lambda:reader.read(1024*1024),b""):
                        writer.write(block)
                        result.update(block)
        if result.hexdigest()!=info["original_csv_sha256"]:
            raise ValueError(f"Restoration checksum mismatch: {split}")
        temporary.replace(path)
        print("Restored exact CSV:",path)

if __name__=="__main__":
    main()

"""Check all packaged files and fixed memberships; no model training."""
import gzip
import hashlib
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path
import pandas as pd
from load_data import load_split,encode_targets,CLASSES,MANIFEST

def main():
    root=Path(__file__).resolve().parent
    for name,info in MANIFEST["files"].items():
        path=root/name
        h=hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda:f.read(1024*1024),b""):
                h.update(chunk)
        if h.hexdigest()!=info["sha256"]:
            raise ValueError(f"Package file changed: {name}")
    parts=[]
    for split in ["train","val","test"]:
        data=load_split(split)
        y=encode_targets(data)
        assert y.shape==(MANIFEST["splits"][split]["rows"],23)
        assert (y.sum(axis=0)>0).all()
        data["split"]=split
        parts.append(data)
        print(split,len(data),"target shape",y.shape)
    combined=pd.concat(parts,ignore_index=True)
    assert len(combined)==159066 and not combined.duplicated(["source","game_id"]).any()
    assignments=pd.read_csv(root/"metadata/split_assignments.csv.gz",dtype=str,keep_default_na=False)
    matched=combined.merge(assignments,on=["source","game_id"],how="outer",validate="one_to_one",indicator=True,suffixes=("_data","_metadata"))
    assert matched["_merge"].eq("both").all()
    assert matched.split_data.eq(matched.split_metadata).all()
    assert matched.groupby("split_group").split_data.nunique().eq(1).all()
    assert matched.description.map(lambda x:hashlib.sha256(x.encode()).hexdigest()).eq(matched.description_hash).all()
    key=matched.description.map(lambda x:re.sub(r"[\W_]+","",unicodedata.normalize("NFKC",x).casefold()))
    assert pd.DataFrame({"description":key,"split":matched.split_data}).groupby("description").split.nunique().eq(1).all()
    counts=Counter(g for raw in combined.genres for g in set(json.loads(raw)))
    frequency=pd.read_csv(root/"reports/final_genre_distribution.csv")
    assert dict(counts)==dict(zip(frequency.genre,frequency["count"]))
    print("PASS: file hashes, 159066 samples, 23 labels, fixed memberships, group integrity and normalized-text leakage checks")

if __name__=="__main__":
    main()

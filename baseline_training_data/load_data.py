"""Shared loader/target encoder. Does not clean, split, fit, or alter labels."""
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parent
INFO=json.loads((ROOT/"labels.json").read_text(encoding="utf-8"))
CLASSES=INFO["classes"]
LABEL2ID=INFO["label2id"]
MANIFEST=json.loads((ROOT/"package_manifest.json").read_text(encoding="utf-8"))

def load_split(split):
    if split not in ("train","val","test"):
        raise ValueError("Use train, val or test; no new split is generated")
    frames=[pd.read_csv(ROOT/part["path"],dtype=str,keep_default_na=False) for part in MANIFEST["splits"][split]["parts"]]
    frame=pd.concat(frames,ignore_index=True)
    if list(frame.columns)!=MANIFEST["schema"] or len(frame)!=MANIFEST["splits"][split]["rows"]:
        raise ValueError("Dataset schema or row count differs from the frozen package")
    return frame

def encode_targets(frame):
    y=np.zeros((len(frame),len(CLASSES)),dtype=np.uint8)
    for i,raw in enumerate(frame["genres"]):
        labels=json.loads(raw)
        if not isinstance(labels,list) or not labels:
            raise ValueError("Missing multi-label targets")
        unknown=set(labels)-set(LABEL2ID)
        if unknown:
            raise ValueError(f"Unknown labels: {unknown}; do not refit the label vocabulary")
        for label in labels:
            y[i,LABEL2ID[label]]=1
    return y

def load_xy(split):
    frame=load_split(split)
    return frame["description"].tolist(),encode_targets(frame)

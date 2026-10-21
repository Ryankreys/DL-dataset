"""Load baseline inputs and targets only; no feature extraction or model fitting."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from load_data import load_split,encode_targets,CLASSES

train=load_split("train")
val=load_split("val")
X_train=train["description"].tolist()
y_train=encode_targets(train)
X_val=val["description"].tolist()
y_val=encode_targets(val)
print("Training:",len(X_train),"target shape",y_train.shape)
print("Validation:",len(X_val),"target shape",y_val.shape)
print("Shared label order:",CLASSES)
# Fit text representations/models on TRAIN only. Use VAL for choices.
# Load test only after the final experiment protocol is fixed.

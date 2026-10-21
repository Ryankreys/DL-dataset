import sys
import unittest
from pathlib import Path
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from load_data import CLASSES,LABEL2ID,encode_targets,load_split

class LoaderTests(unittest.TestCase):
    def test_fixed_23_label_order(self):
        self.assertEqual(len(CLASSES),23)
        self.assertEqual(CLASSES,sorted(CLASSES))
        self.assertEqual([LABEL2ID[x] for x in CLASSES],list(range(23)))
    def test_multilabel_encoding(self):
        frame=pd.DataFrame({"genres":['["Action", "RPG"]','["Adventure"]']})
        y=encode_targets(frame)
        self.assertEqual(y.shape,(2,23))
        self.assertEqual(y[0].sum(),2)
        self.assertEqual(y[0,LABEL2ID["Action"]],1)
        self.assertEqual(y[0,LABEL2ID["RPG"]],1)
    def test_unknown_label_does_not_silently_change_vocabulary(self):
        with self.assertRaises(ValueError):
            encode_targets(pd.DataFrame({"genres":['["Unknown label"]']}))
    def test_invalid_split_does_not_create_new_partition(self):
        with self.assertRaises(ValueError):
            load_split("random")

if __name__=="__main__":
    unittest.main()

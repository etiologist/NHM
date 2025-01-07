import pandas as pd
import re
import string
from rapidfuzz import fuzz
import unicodedata

BHL = pd.read_excel("../data/raw/python test.xlsx", sheet_name="BHL")
Alma = pd.read_excel("../data/raw/python test.xlsx", sheet_name="Alma")

values = Alma["Title"]
keys = Alma["MMSID"]

AlmaDt = dict(zip(keys, values))

p = list(AlmaDt.items())


def remove_punct(BHL):
    BHL["FullTitle"] = BHL["FullTitle"].str.translate(
        str.maketrans("", "", string.punctuation)
    )
    BHL["FullTitle"] = BHL["FullTitle"].str.lower()
    return BHL


def normalize_string(s):
    return unicodedata.normalize("NFC", s)


def convert_string(Alma):
    Alma["Title"] = Alma["Title"].str.normalize("NFC")
    return Alma


data_transformed = remove_punct(BHL)


List1 = data_transformed["FullTitle"]
List2 = Alma["Title"]


def getMMSIDS():
    for x in List1:
        for y in List2:
            if fuzz.ratio(x, y) > 80 and (
                fuzz.token_set_ratio(x, y) > 90 or fuzz.token_sort_ratio(x, y) > 95
            ):
                for key, value in AlmaDt.items():
                    if value == y:
                        print(
                            x,
                            "Matches: ",
                            y,
                            "-",
                            key,
                            "basic ratio:",
                            fuzz.ratio(x, y),
                        )


print(getMMSIDS())

for x in List2:
    y = "Tropical agriculturist and magazine of the Ceylon Agricultural Society"
    if fuzz.token_sort_ratio(y, x) > 50:
        print(x, fuzz.ratio(y, x))

for x in List1:
    y = "The tropical agriculturist"
    print(x, fuzz.token_sort_ratio(x, y))


x = "Tropical agriculturist and magazine of the Ceylon Agricultural Society"
y = "The tropical agriculturist"
print(fuzz.token_set_ratio(y, x))


# Ignores if subset

for x in List1:
    for y in List2:
        if fuzz.token_set_ratio(x, y) > 90:
            print(x, fuzz.token_set_ratio(x, y), y)

# Ignores order

for x in List1:
    for y in List2:
        if fuzz.token_sort_ratio(x, y) > 80:
            print(x, fuzz.token_sort_ratio(x, y), y)

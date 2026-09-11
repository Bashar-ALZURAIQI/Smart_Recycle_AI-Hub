from collections import Counter
from zipfile import ZipFile
from pathlib import Path


SOURCE_ZIP = Path(
    r"data\raw\waste_management_ai"
    r"\Waste Management AI.v3-augmented-v2-trashnet.yolo26.zip"
)

CLASS_MAP = {
    0: 3,
    1: 2,
    2: 1,
    3: 3,
    4: 0,
}


def mapped_line(line: str) -> str:
    parts = line.split()
    parts[0] = str(CLASS_MAP[int(parts[0])])
    return " ".join(parts)


with ZipFile(SOURCE_ZIP) as z:
    labels = [
        n for n in z.namelist()
        if n.startswith("train/labels/")
        and n.endswith(".txt")
    ]

    raw_duplicate_files = 0
    raw_duplicate_lines = 0

    mapped_duplicate_files = 0
    mapped_duplicate_lines = 0

    introduced_files = 0
    introduced_lines = 0

    for label in labels:
        image_name = (
            label.replace("/labels/", "/images/")
            .rsplit(".", 1)[0]
        )

        # Match our V1 exclusion rule.
        if "tetra_pak" in image_name.lower():
            continue

        lines = [
            line.strip()
            for line in z.read(label)
            .decode("utf-8", "replace")
            .splitlines()
            if line.strip()
        ]

        raw_dups = len(lines) - len(set(lines))

        mapped = [
            mapped_line(line)
            for line in lines
        ]

        mapped_dups = len(mapped) - len(set(mapped))

        if raw_dups:
            raw_duplicate_files += 1
            raw_duplicate_lines += raw_dups

        if mapped_dups:
            mapped_duplicate_files += 1
            mapped_duplicate_lines += mapped_dups

        new_dups = mapped_dups - raw_dups

        if new_dups > 0:
            introduced_files += 1
            introduced_lines += new_dups


print("RAW SOURCE")
print("files with duplicates:", raw_duplicate_files)
print("duplicate lines:", raw_duplicate_lines)

print()

print("AFTER V1 MAPPING")
print("files with duplicates:", mapped_duplicate_files)
print("duplicate lines:", mapped_duplicate_lines)

print()

print("INTRODUCED BY MAPPING")
print("files affected:", introduced_files)
print("duplicate lines introduced:", introduced_lines)
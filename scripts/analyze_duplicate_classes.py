from collections import Counter
from pathlib import Path


ROOT = Path(r"data\processed\waste_v1\train\labels")

CLASS_NAMES = [
    "plastic",
    "metal",
    "glass",
    "paper_cardboard",
]


duplicate_by_class = Counter()
files_with_duplicates = 0
total_duplicate_lines = 0


for label_path in ROOT.glob("*.txt"):

    lines = [
        line.strip()
        for line in label_path.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]

    line_counts = Counter(lines)

    file_has_duplicate = False

    for line, count in line_counts.items():

        duplicates = count - 1

        if duplicates <= 0:
            continue

        file_has_duplicate = True
        total_duplicate_lines += duplicates

        class_id = int(line.split()[0])

        duplicate_by_class[class_id] += duplicates

    if file_has_duplicate:
        files_with_duplicates += 1


print("FILES WITH DUPLICATES:", files_with_duplicates)
print("TOTAL DUPLICATE LINES:", total_duplicate_lines)
print()

for class_id, class_name in enumerate(CLASS_NAMES):
    print(
        class_id,
        class_name,
        ":",
        duplicate_by_class[class_id],
    )
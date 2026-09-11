# Smart Recycle AI-Hub — V1 Dataset Preparation and Validation

## Document Purpose

This document records the complete dataset preparation process used for the **Smart Recycle AI-Hub V1** object-detection model.

It is intended to serve as:

- a reproducibility record,

- a technical handoff document,

- a reference for future dataset revisions,

- an explanation of all inclusion/exclusion decisions,

- and an audit trail showing how the final Train and Validation datasets were produced.

The raw datasets are intentionally kept unchanged.

All filtering, class remapping, duplicate removal, leakage prevention, and validation are performed when building the processed V1 dataset.

---

# 1. V1 Detection Scope

The final Smart Recycle V1 detector uses exactly four trainable classes:

| Target ID | Final Class |
|---:|---|
| 0 | plastic |
| 1 | metal |
| 2 | glass |
| 3 | paper_cardboard |

The physical prototype will also contain a **Reject** path.

However:

> **Reject is NOT a YOLO training class.**

Reject is handled later in application/decision logic.

Examples that may be sent to Reject include:

- unsupported materials,

- unknown objects,

- ambiguous detections,

- detections below the confidence threshold,

- items intentionally excluded from the V1 training scope.

---

# 2. Important V1 Scope Decisions

The following decisions were established before final training.

## Included

- Plastic

- Metal

- Glass

- Paper

- Cardboard

Paper and Cardboard are merged into one final class:

`paper_cardboard`

## Excluded from V1

- Tetra Pak / composite cartons

- Broken glass

- Organic waste

- Unsupported materials

- Materials requiring another sensing technology such as NIR

- Ambiguous composite materials that cannot be safely mapped to one of the four V1 categories

The training dataset must not silently convert ambiguous composite materials into one of the four target classes.

---

# 3. Dataset Directory Policy

The project separates raw, processed, temporary, inspection, and training-result data.

Important paths:

```text
data/
├── raw/
├── interim/
├── processed/
└── inspection/
```

## Raw data

`data/raw/`

Raw downloaded datasets are stored here.

The raw dataset is considered immutable.

The preprocessing scripts should read from the raw source and create a new processed dataset instead of editing raw files directly.

## Processed data

Final V1 dataset:

```text
data/processed/waste_v1/
```

Structure:

```text
data/processed/waste_v1/
├── data.yaml
├── train/
│   ├── images/
│   └── labels/
└── valid/
    ├── images/
    └── labels/
```

## Inspection data

Temporary visual inspection samples are stored under:

```text
data/inspection/
```

These files are used only for manual QA and are not committed to Git.

---

# 4. Git Ignore Policy

The project `.gitignore` currently contains:

```text
runs/
data/raw/
.env
.venv/
.vscode/
*.pt
data/processed/
data/interim/
data/inspection/
__pycache__/
*.pyc
```

This prevents large datasets, model weights, local environments, temporary inspection files, training runs, and Python cache files from being accidentally pushed to GitHub.

The preprocessing and analysis scripts themselves are committed because they are required to reproduce the dataset preparation process.

---

# 5. Dataset Sources

Three dataset sources were considered for V1.

---

# 5.1 Primary Dataset — Waste Management AI

## Source

**Name:** Waste Management AI

**Provider:** University of Tehran / Roboflow Universe

**Task:** Object Detection

**Version used:** 3

**License:** CC BY 4.0

**Downloaded format:** YOLO26

**Role:** Primary V1 dataset

The source metadata inside `data.yaml` reported:

```yaml
workspace: university-of-tehran
project: waste-management-ai
version: 3
license: CC BY 4.0
url: https://universe.roboflow.com/university-of-tehran/waste-management-ai/dataset/3
```

Downloaded archive:

```text
data/raw/waste_management_ai/
Waste Management AI.v3-augmented-v2-trashnet.yolo26.zip
```

The raw ZIP remains unchanged.

---

# 5.2 Secondary Dataset — DWSD

## Source

**Name:** DWSD — Dense Waste Segmentation Dataset

**Task:** Segmentation

**Role:** Secondary / optional enhancement dataset

**Status:** Inspected but NOT included in the first V1 baseline training

Downloaded archive:

```text
data/raw/dwsd/
DWSD Dense Waste Segmentation Dataset.zip
```

The downloaded archive contained a second nested archive:

```text
DWSD Dense Waste Segmentation Dataset/
└── DSWD.zip
```

The inner dataset structure was:

```text
DSWD/
├── Train/
│   ├── Image/
│   └── Mask/
└── Test/
    ├── Image/
    └── Mask/
```

Counts found:

| Split | Images | Masks |
|---|---:|---:|
| Train | 640 | 640 |
| Test | 144 | 144 |
| Total | 784 | 784 |

All were PNG files.

The masks were grayscale label maps rather than YOLO bounding-box labels.

Therefore DWSD would require conversion from segmentation masks to object-detection bounding boxes before it could be added to the YOLO training dataset.

### Useful DWSD images

After analyzing mask class IDs, only images containing V1-compatible categories were counted as useful.

Useful unique images:

| Split | Useful images |
|---|---:|
| Train | 121 |
| Test | 26 |
| Total | 147 |

Class presence across all useful DWSD images:

| Final V1 category | Images |
|---|---:|
| plastic | 68 |
| metal | 72 |
| glass | 38 |
| paper_cardboard | 45 |

One image can contain more than one useful class, therefore these class counts do not sum to 147.

### DWSD decision

DWSD is approved as a **secondary dataset only**.

For the first YOLO26 V1 baseline:

> DWSD is NOT mixed into the primary dataset.

Reason:

The primary dataset is already large enough for an initial baseline.

DWSD will only be added later if evaluation shows that the baseline needs more diversity or more examples for specific weak classes.

---

# 5.3 Optional Dataset — TACO

**Name:** TACO — Trash Annotations in Context

**Role:** Optional future source

**Status:** Not downloaded for V1 baseline

Local placeholder:

```text
data/raw/taco_optional/
```

The folder was intentionally left empty.

TACO may later be used for difficult real-world examples or additional negative/background data if required.

---

# 6. Primary Dataset Archive Inspection

The Waste Management AI ZIP was inspected without extracting or modifying it.

Total archive entries found:

```text
35202
```

The archive contained normal YOLO-style folders such as:

```text
train/images/
train/labels/
valid/images/
valid/labels/
```

The dataset contained no usable test split.

---

# 7. Primary Dataset Class Definition

The source `data.yaml` contained:

```yaml
nc: 5
names:
  - Cardboard
  - Glass
  - Metal
  - Paper
  - Plastic
```

Source IDs:

| Source ID | Source class |
|---:|---|
| 0 | Cardboard |
| 1 | Glass |
| 2 | Metal |
| 3 | Paper |
| 4 | Plastic |

The Smart Recycle V1 mapping is:

| Source | Source ID | Final class | Final ID |
|---|---:|---|---:|
| Cardboard | 0 | paper_cardboard | 3 |
| Glass | 1 | glass | 2 |
| Metal | 2 | metal | 1 |
| Paper | 3 | paper_cardboard | 3 |
| Plastic | 4 | plastic | 0 |

Therefore both:

```text
Cardboard
Paper
```

become:

```text
paper_cardboard
```

---

# 8. Original Primary Dataset Counts

Before V1 filtering, the downloaded archive contained:

| Split | Images | Label files |
|---|---:|---:|
| Train | 16,248 | 16,248 |
| Valid | 1,351 | 1,351 |
| Test | 0 | 0 |

Image and label counts matched exactly.

## Raw object counts

### Train

| Source class | Objects |
|---|---:|
| Cardboard | 15,799 |
| Glass | 19,366 |
| Metal | 14,202 |
| Paper | 22,092 |
| Plastic | 20,032 |
| **Total** | **91,491** |

### Validation

| Source class | Objects |
|---|---:|
| Cardboard | 395 |
| Glass | 462 |
| Metal | 298 |
| Paper | 557 |
| Plastic | 503 |
| **Total** | **2,215** |

---

# 9. Raw YOLO Label Integrity Check

Before modifying the labels, the raw YOLO annotations were checked.

The validation covered:

- label-file count,

- object count,

- empty labels,

- malformed YOLO rows,

- source class IDs outside `0–4`,

- invalid normalized bounding-box coordinates.

## Raw Train result

```text
labels = 16248
objects = 91491
empty = 0
bad_lines = 0
bad_class = 0
bad_box = 0
```

## Raw Validation result

```text
labels = 1351
objects = 2215
empty = 0
bad_lines = 0
bad_class = 0
bad_box = 0
```

Conclusion:

> The raw YOLO annotation structure was valid before preprocessing.

---

# 10. Content-Level Inspection

File and label syntax being correct does not automatically mean every object belongs in the Smart Recycle V1 scope.

Several filename families were therefore investigated manually and statistically.

The most important were:

```text
tetra_pak
plastic_bag
spray_cans
```

Counts:

| Keyword | Train | Valid | Total |
|---|---:|---:|---:|
| tetra_pak | 902 | 67 | 969 |
| plastic_bag | 285 | 23 | 308 |
| spray_cans | 357 | 29 | 386 |

---

# 11. Tetra Pak Investigation

Tetra Pak is a composite packaging material.

It was already outside the defined V1 scope.

However, it was important to determine how the primary dataset had annotated these images.

Across all 969 `tetra_pak` images:

| Source class | Images containing class | Objects |
|---|---:|---:|
| Cardboard | 969 | 3,025 |
| Glass | 256 | 328 |
| Metal | 402 | 1,040 |
| Paper | 32 | 35 |
| Plastic | 482 | 1,071 |

Every Tetra Pak image contained at least one Cardboard annotation.

Many also contained other materials because some source images were augmented/mosaic images containing several objects.

## Visual inspection

Six Tetra Pak examples were extracted to:

```text
data/inspection/tetra_pak/
```

The samples confirmed that the images contained composite Tetra Pak/carton packaging.

Because the annotations only identified the object using the coarse source classes, it was not possible to reliably identify and remove only the exact Tetra Pak bounding box in every mosaic image.

## Final decision

For V1:

> If an image filename contains `tetra_pak`, the entire image and its matching label file are excluded from the processed dataset.

This is intentionally conservative.

It prevents composite cartons from teaching the model that Tetra Pak should automatically be treated as `paper_cardboard`.

Total scope removal:

```text
Train: 902 images
Valid: 67 images
Total: 969 images
```

The raw source files remain untouched.

---

# 12. Plastic Bag Investigation

`plastic_bag` images were also inspected.

Total:

```text
308 images
```

Annotation distribution:

| Source class | Images containing class | Objects |
|---|---:|---:|
| Cardboard | 27 | 42 |
| Glass | 3 | 3 |
| Metal | 5 | 14 |
| Paper | 12 | 12 |
| Plastic | 308 | 1,569 |

All 308 images contained the Plastic class.

Visual inspection also confirmed plastic bags/wrappers were appropriate plastic examples.

## Final decision

```text
plastic_bag -> KEEP
```

---

# 13. Spray Can Investigation

Total:

```text
386 images
```

Annotation distribution:

| Source class | Images containing class | Objects |
|---|---:|---:|
| Cardboard | 262 | 488 |
| Glass | 26 | 28 |
| Metal | 384 | 1,348 |
| Paper | 9 | 10 |
| Plastic | 275 | 550 |

384 out of 386 images contained a Metal annotation.

Other annotations appear because many images are multi-object or mosaic images.

Visual inspection supported their use as Metal examples.

## Final decision

```text
spray_cans -> KEEP
```

---

# 14. First Processed Mapping Result

After:

1. removing Tetra Pak images,

2. remapping the five source classes to the four V1 classes,

the intermediate counts were:

## Train

```text
Images kept: 15,346
Images excluded: 902
plastic:          18,967
metal:            13,162
glass:            19,044
paper_cardboard:  34,925
Total objects:    86,098
```

## Validation

```text
Images kept: 1,284
Images excluded: 67
plastic:          497
metal:            298
glass:            456
paper_cardboard:  858
Total objects:    2,109
```

At this point, structural label validation still showed:

```text
EMPTY = 0
BAD_LINES = 0
BAD_CLASS = 0
BAD_BOX = 0
```

---

# 15. Exact Duplicate Annotation Investigation

During an Ultralytics sanity training run, Ultralytics reported lines such as:

```text
duplicate labels removed
```

This triggered a full duplicate-label investigation.

## Initial processed dataset result

```text
Train:
892 files with exact duplicate annotations
1112 duplicate lines
Valid:
0 duplicate lines
```

Distribution of the 1,112 Train duplicates:

| Final class | Duplicate annotations |
|---|---:|
| plastic | 181 |
| metal | 18 |
| glass | 549 |
| paper_cardboard | 364 |
| **Total** | **1,112** |

---

# 16. Was the Duplicate Problem Caused by Class Merging?

Because both Paper and Cardboard are mapped to `paper_cardboard`, it was necessary to determine whether class merging created the duplicates.

The raw archive was compared against the mapped output.

Result:

```text
RAW SOURCE
files with duplicates: 889
duplicate lines: 1109
AFTER V1 MAPPING
files with duplicates: 892
duplicate lines: 1112
INTRODUCED BY MAPPING
files affected: 3
duplicate lines introduced: 3
```

Conclusion:

> The original dataset already contained almost all of the duplicate annotations.

Only three duplicate annotations were introduced by the V1 Paper/Cardboard merge.

---

# 17. Exact Duplicate Removal Rule

The preprocessing script was updated to remove exact duplicate annotation lines.

Important:

> Only 100% identical annotation lines are removed.

Example removed:

```text
2 0.500 0.400 0.200 0.300
2 0.500 0.400 0.200 0.300
```

Only one copy is retained.

However:

```text
2 0.500 0.400 0.200 0.300
2 0.501 0.400 0.200 0.300
```

are treated as two different boxes and are both preserved.

The script does NOT perform fuzzy deduplication, IoU-based removal, or manual guessing.

---

# 18. Initial Duplicate-Cleaned Result

Before Train/Validation leakage correction, exact duplicate removal produced:

## Train

```text
Images: 15,346
plastic:          18,786
metal:            13,144
glass:            18,495
paper_cardboard:  34,561
Total objects:    84,986
```

Duplicates removed:

```text
plastic:          181
metal:             18
glass:            549
paper_cardboard:  364
Total:           1,112
```

## Validation

No exact duplicate annotations were found.

---

# 19. Augmentation and Train/Validation Leakage Investigation

The downloaded Roboflow dataset is augmented.

Roboflow-generated filenames use a structure similar to:

```text
cardboard-100_jpg.rf.<hash>.jpg
```

The part before:

```text
.rf.
```

was treated as the original source-image key.

Example:

```text
cardboard-100_jpg.rf.abc123.jpg
```

source key:

```text
cardboard-100_jpg
```

This allowed us to determine whether augmented versions of the same original source image appeared in both Train and Validation.

---

# 20. Leakage Found Before Correction

Before leakage correction:

```text
TRAIN IMAGES: 15346
TRAIN UNIQUE SOURCES: 4986
VALID IMAGES: 1284
VALID UNIQUE SOURCES: 1268
```

The analysis found:

```text
OVERLAPPING SOURCE GROUPS: 66
TRAIN IMAGES FROM OVERLAPPING SOURCES: 198
VALID IMAGES FROM OVERLAPPING SOURCES: 66
```

Therefore 66 original source images had augmented variants present in both Train and Validation.

This could artificially inflate validation performance because the model could train on one transformed version of an image and then be evaluated on another version of the same original source.

The validation set also contained internal duplication by source:

```text
VALID SOURCE GROUPS WITH >1 IMAGE: 16
EXTRA VALID IMAGES FROM SAME SOURCE: 16
```

---

# 21. Leakage Prevention Policy

The following deterministic policy was implemented.

## Rule 1 — Validation owns the source

If an original source key exists in Validation:

> All Train images with that same original source key are excluded.

Validation is preserved.

## Rule 2 — One Validation image per source

If Validation contains multiple augmented images from the same original source:

> Only one deterministic image is retained.

The preprocessing script sorts the candidate filenames and keeps one image per source.

## Rule 3 — Multiple augmentations are allowed inside Train

Several augmented images from one original source are allowed inside Train.

This is normal data augmentation.

What is prohibited is:

```text
same original source
Train ↔ Validation
```

---

# 22. Final Leakage-Safe Dataset Build

After applying:

1. V1 scope filtering,

2. Tetra Pak exclusion,

3. class remapping,

4. exact duplicate annotation removal,

5. Train/Validation source leakage prevention,

6. Validation source deduplication,

the final dataset became:

## Final Train

```text
Images kept: 15,148
Excluded by V1 scope: 902
Excluded for split leakage: 198
```

Final objects:

| Final class | Objects |
|---|---:|
| plastic | 18,785 |
| metal | 13,018 |
| glass | 18,480 |
| paper_cardboard | 33,567 |
| **Total** | **83,850** |

Exact duplicate annotations removed during the final build:

| Class | Removed |
|---|---:|
| plastic | 181 |
| metal | 18 |
| glass | 549 |
| paper_cardboard | 361 |
| **Total** | **1,109** |

The final-build duplicate count is 1,109 instead of the earlier 1,112 because three duplicate annotations were located in Train images that were later completely removed by the Train/Validation leakage filter.

---

# 23. Final Validation Dataset

```text
Images kept: 1,268
Excluded by V1 scope: 67
Extra same-source Validation images removed: 16
```

Final objects:

| Final class | Objects |
|---|---:|
| plastic | 497 |
| metal | 298 |
| glass | 456 |
| paper_cardboard | 835 |
| **Total** | **2,086** |

No exact duplicate annotations remained.

---

# 24. Final Source-Level Split Verification

After the final rebuild:

```text
TRAIN IMAGES: 15148
TRAIN UNIQUE SOURCES: 4920
VALID IMAGES: 1268
VALID UNIQUE SOURCES: 1268
```

Train/Validation overlap:

```text
OVERLAPPING SOURCE GROUPS: 0
TRAIN IMAGES FROM OVERLAPPING SOURCES: 0
VALID IMAGES FROM OVERLAPPING SOURCES: 0
```

Validation internal source duplication:

```text
VALID SOURCE GROUPS WITH >1 IMAGE: 0
EXTRA VALID IMAGES FROM SAME SOURCE: 0
```

Therefore:

> No original source image appears in both Train and Validation.

And:

> Every Validation image represents a unique original source key.

---

# 25. Train Augmentation Statistics

The final Train dataset contains:

```text
15,148 images
4,920 unique original source groups
```

The analysis reported:

```text
TRAIN SOURCE GROUPS WITH >1 IMAGE: 4920
EXTRA TRAIN AUGMENTED IMAGES: 10228
```

This is expected.

Multiple augmented variants of one source are intentionally allowed inside the training split.

They are not considered Train/Validation leakage because none of those source groups appear in Validation.

---

# 26. Final Exact Duplicate Check

After the final leakage-safe dataset was rebuilt:

```text
FILES WITH DUPLICATES: 0
TOTAL DUPLICATE LINES: 0
plastic: 0
metal: 0
glass: 0
paper_cardboard: 0
```

Therefore no exact duplicate YOLO annotation lines remain in the final processed dataset.

---

# 27. Final YOLO Label Validation

The final Train and Validation labels were fully checked again after all preprocessing.

## Final Train

```text
LABELS: 15148
OBJECTS: 83850
0 plastic:         18785
1 metal:           13018
2 glass:           18480
3 paper_cardboard: 33567
EMPTY: 0
BAD_LINES: 0
BAD_CLASS: 0
BAD_BOX: 0
```

## Final Validation

```text
LABELS: 1268
OBJECTS: 2086
0 plastic:         497
1 metal:           298
2 glass:           456
3 paper_cardboard: 835
EMPTY: 0
BAD_LINES: 0
BAD_CLASS: 0
BAD_BOX: 0
```

Meaning:

- every expected label file exists,

- no label file is empty,

- every line uses valid YOLO format,

- all class IDs are within `0–3`,

- normalized bounding-box coordinates are valid,

- no exact duplicate annotation remains.

---

# 28. Visual Bounding-Box Validation

A separate inspection script was used to select sample Train and Validation images and draw the final V1 bounding boxes and class names on the images.

Script:

```text
scripts/inspect_waste_v1.py
```

Inspection output:

```text
data/inspection/final_labels/
```

Samples were visually reviewed.

The inspection confirmed:

- boxes were positioned on the intended objects,

- remapped class names matched the objects,

- no obvious systematic box displacement was observed.

The visual validation passed.

---

# 29. Final V1 Dataset Status

Final status:

```text
Smart Recycle AI-Hub
V1 Object Detection Dataset
STATUS:
READY FOR BASELINE TRAINING
```

Final dataset:

```text
Train:
15,148 images
83,850 objects
Validation:
1,268 images
2,086 objects
```

Final target classes:

```text
0 plastic
1 metal
2 glass
3 paper_cardboard
```

Final QA:

```text
Exact duplicate labels:       0
Train/Valid source overlap:   0
Duplicate Valid sources:      0
Empty labels:                 0
Malformed label lines:        0
Invalid class IDs:            0
Invalid boxes:                0
Tetra Pak in processed data:  0
```

---

# 30. Dataset Preparation Scripts

The following scripts are part of the reproducible preparation workflow.

## `scripts/prepare_waste_v1.py`

Main preprocessing script.

Responsibilities:

- read the raw Waste Management AI ZIP,

- preserve raw data unchanged,

- exclude V1 out-of-scope filename groups such as `tetra_pak`,

- remap five source classes into four V1 classes,

- merge Paper and Cardboard into `paper_cardboard`,

- remove exact duplicate annotations,

- build a leakage-safe Validation source plan,

- remove Train images sharing a source key with Validation,

- retain only one Validation image per source key,

- copy final images,

- generate final labels,

- generate final `data.yaml`,

- print detailed preprocessing statistics.

Safety behavior:

> If `data/processed/waste_v1` already exists, the script stops instead of automatically deleting or overwriting it.

This prevents accidental dataset destruction or merging between builds.

---

# 31. `scripts/analyze_duplicate_labels.py`

Used to determine whether duplicate annotations existed in:

- the raw source dataset,

- the mapped V1 labels,

- and how many duplicates were introduced specifically by the V1 class mapping.

This script established that almost all duplicate annotations already existed in the raw source dataset.

---

# 32. `scripts/analyze_duplicate_classes.py`

Reads the processed Train label files and reports:

- number of files containing duplicate annotation lines,

- total duplicate lines,

- duplicate count per final V1 class.

The final processed dataset must return:

```text
FILES WITH DUPLICATES: 0
TOTAL DUPLICATE LINES: 0
```

---

# 33. `scripts/analyze_split_leakage.py`

Analyzes Roboflow source keys before `.rf.<hash>`.

Reports:

- Train image count,

- Train unique source count,

- Validation image count,

- Validation unique source count,

- Train/Validation source overlap,

- images affected by overlap,

- duplicate source groups inside Validation,

- Train augmentation statistics.

The final required condition is:

```text
OVERLAPPING SOURCE GROUPS: 0
VALID SOURCE GROUPS WITH >1 IMAGE: 0
```

---

# 34. `scripts/inspect_waste_v1.py`

Creates visual QA samples by drawing YOLO bounding boxes and final class names on selected images.

Used only for manual dataset inspection.

Inspection output is intentionally ignored by Git.

---

# 35. Model / Training Environment

Environment used during dataset and training sanity validation:

```text
OS: Windows
Python: 3.14.6
PyTorch: 2.14.0+cu126
Ultralytics: 8.4.142
CUDA runtime used by PyTorch: 12.6
GPU: NVIDIA GeForce RTX 4050 Laptop GPU
GPU VRAM: approximately 6 GB
Model family: YOLO26
Baseline model: YOLO26n
OpenCV: 5.0.0
```

PyTorch verification confirmed:

```text
CUDA available: True
Device count: 1
GPU: NVIDIA GeForce RTX 4050 Laptop GPU
```

A direct CUDA test also passed:

```text
torch.cuda.set_device(0)
CUDA tensor creation
CUDA synchronization
```

---

# 36. Temporary CUDA / System Memory Issue

During the first training attempt, CUDA returned:

```text
CUDA-capable device(s) is/are busy or unavailable
```

A later PyTorch test also encountered:

```text
OpenBLAS error:
Memory allocation still failed after 10 retries
```

System memory inspection at that moment showed approximately:

```text
RAM total: 15.71 GB
RAM available: 1.57 GB
RAM used: 90%
```

After memory pressure decreased:

```text
RAM available: approximately 3.97 GB
RAM used: approximately 74.7%
```

PyTorch successfully detected and used the RTX 4050 again.

Direct test result:

```text
SET DEVICE: OK
TENSOR DEVICE: cuda:0
CUDA TEST: SUCCESS
```

Conclusion:

The first failure was an environment/runtime resource condition, not a dataset-format problem.

No PyTorch or CUDA reinstall was performed.

---

# 37. Sanity Training Philosophy

Before full training, very small sanity runs were used.

Important:

> Sanity runs are NOT used to judge final model accuracy.

They were intentionally:

```text
epochs = 1
fraction = 0.05
imgsz = 640
```

They were designed to verify:

- dataset readability,

- four-class model configuration,

- GPU execution,

- AMP,

- DataLoader behavior,

- VRAM use,

- training completion,

- validation completion,

- weight saving.

---

# 38. Batch 8 Sanity Run

Configuration included:

```text
batch = 8
workers = 4
fraction = 0.05
epochs = 1
```

After the temporary CUDA/system-memory problem was resolved, the run completed.

Observed GPU memory:

```text
approximately 1.33 GB
```

This confirmed that the model and dataset could train successfully on the RTX 4050.

This run occurred before all later dataset-cleaning improvements and is not considered a final performance benchmark.

---

# 39. DataLoader Worker Failure

A later sanity test used:

```text
batch = 16
workers = 4
```

Training itself completed.

Observed GPU memory:

```text
approximately 2.55 GB
```

However, Validation failed near completion with:

```text
RuntimeError:
DataLoader worker (...) exited unexpectedly
```

The failure occurred inside PyTorch's DataLoader multiprocessing.

This was not a CUDA out-of-memory error.

---

# 40. Workers = 0 Test

To isolate the DataLoader issue, only one variable was changed:

```text
workers = 4
```

to:

```text
workers = 0
```

Batch remained:

```text
batch = 16
```

The test then completed:

- training,

- validation,

- best weight saving,

- last weight saving.

Observed GPU memory:

```text
approximately 2.53 GB
```

This established `workers=0` as the stable Windows configuration for the current machine.

---

# 41. Batch 32 Test

A second stable test used:

```text
batch = 32
workers = 0
```

It also completed successfully.

Observed GPU memory:

```text
approximately 4.8 GB
```

The speed improvement compared with Batch 16 was relatively small, while VRAM use increased considerably.

Therefore the baseline training recommendation is:

```text
batch = 16
workers = 0
```

rather than Batch 32.

This provides more VRAM headroom and is expected to be safer during a long training run.

---

# 42. Planned Baseline Training Configuration

Full baseline training has NOT yet started at the time this document was written.

The planned baseline configuration is:

```text
model = yolo26n.pt
imgsz = 640
batch = 16
workers = 0
device = 0
epochs = 80
patience = 15
```

Planned command:

```cmd
yolo detect train model=yolo26n.pt data=data\processed\waste_v1\data.yaml epochs=80 patience=15 imgsz=640 batch=16 device=0 workers=0 project=runs\waste_v1 name=yolo26n_v1_baseline
```

This command should only be executed after the dataset-preparation scripts and documentation are committed to Git.

---

# 43. Why DWSD Is Not Used in the First Baseline

Although DWSD contains useful additional examples, the first baseline intentionally uses only the cleaned primary dataset.

Reasons:

1. The primary dataset already contains more than 15,000 final Train images.

2. A clean baseline is needed before measuring whether additional data actually helps.

3. DWSD requires segmentation-mask-to-bounding-box conversion.

4. Adding DWSD immediately would make it harder to determine whether later improvements came from:

   - more data,

   - different data,

   - class balance,

   - or model/training changes.

Recommended workflow:

```text
Primary-only baseline
        ↓
Evaluate weaknesses
        ↓
Identify weak classes / conditions
        ↓
Add selected DWSD examples if needed
        ↓
Retrain and compare
```

---

# 44. Rebuilding the Processed Dataset

The processed dataset is reproducible from the raw ZIP.

Because the preparation script intentionally refuses to overwrite an existing processed dataset, rebuilding requires an explicit manual delete.

Example:

```cmd
rmdir /s /q data\processed\waste_v1
```

Then:

```cmd
python scripts\prepare_waste_v1.py
```

After rebuilding, quality checks should be repeated.

---

# 45. Required Post-Build Checks

After every future rebuild, run at minimum:

## Duplicate annotation validation

```cmd
python scripts\analyze_duplicate_classes.py
```

Required:

```text
FILES WITH DUPLICATES: 0
TOTAL DUPLICATE LINES: 0
```

## Train/Validation source leakage validation

```cmd
python scripts\analyze_split_leakage.py
```

Required:

```text
OVERLAPPING SOURCE GROUPS: 0
VALID SOURCE GROUPS WITH >1 IMAGE: 0
```

A final YOLO label integrity scan should also confirm:

```text
EMPTY = 0
BAD_LINES = 0
BAD_CLASS = 0
BAD_BOX = 0
```

---

# 46. Raw Data Preservation Rule

Do NOT manually edit the raw ZIP to fix labels.

Do NOT delete source files from `data/raw`.

Do NOT perform permanent corrections directly inside raw dataset folders.

All V1 changes must be encoded in scripts.

This ensures:

- reproducibility,

- auditability,

- easier debugging,

- clean future dataset revisions,

- ability to compare V1 and future V2 processing policies.

---

# 47. Current Project State at End of Dataset Phase

The V1 dataset-preparation phase is complete.

Current final dataset:

```text
TRAIN
Images: 15,148
Objects: 83,850
VALID
Images: 1,268
Objects: 2,086
```

Quality status:

```text
Tetra Pak excluded: YES
Target classes correct: YES
Exact duplicate annotations: 0
Train/Valid source overlap: 0
Duplicate Valid sources: 0
Empty labels: 0
Malformed labels: 0
Invalid class IDs: 0
Invalid bounding boxes: 0
Visual label inspection: PASS
```

Secondary DWSD:

```text
Inspected: YES
Used in baseline: NO
```

TACO:

```text
Optional
Not downloaded
Not used in baseline
```

YOLO26n sanity testing:

```text
CUDA: PASS
AMP: PASS
Training: PASS
Validation: PASS with workers=0
batch=16: PASS
batch=32: PASS
Recommended baseline batch: 16
Recommended workers: 0
```

Full baseline training:

```text
NOT STARTED YET
```

---

# 48. Next Step

The immediate next project step is:

1. Commit the dataset-preparation scripts.

2. Commit this documentation.

3. Push the dataset-preparation checkpoint to GitHub.

4. Start the full YOLO26n V1 baseline training.

5. Track training metrics.

6. Evaluate `best.pt` on Validation and independent real-world prototype images.

7. Only after baseline evaluation decide whether DWSD or other supplemental data is necessary.

---

# 49. Summary

The final Smart Recycle AI-Hub V1 dataset was not used directly as downloaded.

It went through a controlled preparation pipeline:

```text
Waste Management AI raw ZIP
        ↓
Raw format verification
        ↓
Raw label integrity check
        ↓
V1 scope review
        ↓
Tetra Pak removal
        ↓
5 source classes → 4 V1 classes
        ↓
Exact annotation duplicate removal
        ↓
Roboflow source-key analysis
        ↓
Train/Validation leakage removal
        ↓
Validation source deduplication
        ↓
Final YOLO label validation
        ↓
Visual bounding-box inspection
        ↓
Training sanity tests
        ↓
V1 dataset ready for baseline training
```

This process is intentionally reproducible through scripts rather than undocumented manual edits.

The resulting dataset is the official input dataset for the first Smart Recycle AI-Hub YOLO26n V1 baseline.

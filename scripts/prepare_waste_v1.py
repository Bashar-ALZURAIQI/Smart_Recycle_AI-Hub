from collections import Counter
from pathlib import Path
from zipfile import ZipFile
import shutil


# --------------------------------------------------
# Paths
# --------------------------------------------------

SOURCE_ZIP = Path(
    r"data\raw\waste_management_ai"
    r"\Waste Management AI.v3-augmented-v2-trashnet.yolo26.zip"
)

OUTPUT_DIR = Path(r"data\processed\waste_v1")


# --------------------------------------------------
# V1 class mapping
# --------------------------------------------------

# Source dataset:
# 0 = Cardboard
# 1 = Glass
# 2 = Metal
# 3 = Paper
# 4 = Plastic
#
# Smart Recycle V1:
# 0 = plastic
# 1 = metal
# 2 = glass
# 3 = paper_cardboard

CLASS_MAP = {
    0: 3,  # Cardboard -> paper_cardboard
    1: 2,  # Glass -> glass
    2: 1,  # Metal -> metal
    3: 3,  # Paper -> paper_cardboard
    4: 0,  # Plastic -> plastic
}

TARGET_NAMES = [
    "plastic",
    "metal",
    "glass",
    "paper_cardboard",
]

EXCLUDED_KEYWORDS = {
    "tetra_pak",
}

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp",
}


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def should_exclude(filename: str) -> bool:
    """
    Return True when an image is outside Smart Recycle V1 scope.
    """
    name = filename.lower()

    return any(
        keyword in name
        for keyword in EXCLUDED_KEYWORDS
    )


def source_key(filename: str) -> str:
    """
    Return the original source-image name before Roboflow's
    augmentation hash.

    Example:

        cardboard-100_jpg.rf.abc123.jpg

    becomes:

        cardboard-100_jpg
    """

    return (
        Path(filename)
        .name
        .lower()
        .split(".rf.")[0]
    )


# --------------------------------------------------
# Label conversion
# --------------------------------------------------

def convert_label(
    text: str,
) -> tuple[str, Counter, Counter]:
    """
    Convert source YOLO labels to Smart Recycle V1 labels.

    Operations:
    1. Validate YOLO label format.
    2. Remap source class IDs to V1 class IDs.
    3. Preserve bounding-box coordinates unchanged.
    4. Remove exact duplicate annotations after mapping.

    Only 100% identical mapped label lines are removed.
    Similar or overlapping bounding boxes are NOT removed.
    """

    converted_lines = []
    seen_lines = set()

    object_counts = Counter()
    duplicate_counts = Counter()

    for line_number, line in enumerate(
        text.splitlines(),
        start=1,
    ):

        line = line.strip()

        if not line:
            continue

        parts = line.split()

        if len(parts) != 5:
            raise ValueError(
                f"Invalid YOLO label at line "
                f"{line_number}: {line}"
            )

        try:
            source_class = int(parts[0])

        except ValueError as error:
            raise ValueError(
                f"Invalid class ID at line "
                f"{line_number}: {line}"
            ) from error

        if source_class not in CLASS_MAP:
            raise ValueError(
                f"Unexpected source class ID "
                f"{source_class} at line "
                f"{line_number}"
            )

        target_class = CLASS_MAP[
            source_class
        ]

        converted_line = " ".join(
            [str(target_class)] + parts[1:]
        )

        # ------------------------------------------
        # Remove exact duplicate annotations only
        # ------------------------------------------

        if converted_line in seen_lines:

            duplicate_counts[
                target_class
            ] += 1

            continue

        seen_lines.add(
            converted_line
        )

        converted_lines.append(
            converted_line
        )

        object_counts[
            target_class
        ] += 1

    result = "\n".join(
        converted_lines
    )

    if result:
        result += "\n"

    return (
        result,
        object_counts,
        duplicate_counts,
    )


# --------------------------------------------------
# Validation split plan
# --------------------------------------------------

def build_validation_plan(
    archive_names: list[str],
) -> tuple[
    set[str],
    set[str],
    int,
]:
    """
    Build a clean validation plan.

    Rules:

    1. Ignore items outside V1 scope.
    2. Validation owns its original source key.
    3. Keep only ONE validation image per original source.
    4. Training images with a source key that exists in validation
       will later be excluded.

    Returns:

        valid_source_keys
            Original source keys reserved exclusively for validation.

        valid_keep_images
            Exact validation image filenames to keep.

        valid_duplicate_images_removed
            Number of extra validation images removed because they
            came from an already-used original source.
    """

    valid_images = sorted(
        name
        for name in archive_names
        if name.startswith(
            "valid/images/"
        )
        and Path(
            name
        ).suffix.lower()
        in IMAGE_EXTENSIONS
        and not should_exclude(
            Path(name).name
        )
    )

    valid_source_keys = set()

    valid_keep_images = set()

    valid_duplicate_images_removed = 0

    for image_name in valid_images:

        key = source_key(
            image_name
        )

        # Same original source already exists in validation.
        # Keep only the first deterministic image.
        if key in valid_source_keys:

            valid_duplicate_images_removed += 1

            continue

        valid_source_keys.add(
            key
        )

        valid_keep_images.add(
            image_name
        )

    return (
        valid_source_keys,
        valid_keep_images,
        valid_duplicate_images_removed,
    )


# --------------------------------------------------
# Split preparation
# --------------------------------------------------

def prepare_split(
    archive: ZipFile,
    archive_names: list[str],
    archive_name_set: set[str],
    split: str,
    valid_source_keys: set[str],
    valid_keep_images: set[str],
) -> dict:
    """
    Prepare one clean Smart Recycle V1 split.
    """

    output_images = (
        OUTPUT_DIR
        / split
        / "images"
    )

    output_labels = (
        OUTPUT_DIR
        / split
        / "labels"
    )

    output_images.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_labels.mkdir(
        parents=True,
        exist_ok=True,
    )

    image_prefix = (
        f"{split}/images/"
    )

    image_files = sorted(
        name
        for name in archive_names
        if name.startswith(
            image_prefix
        )
        and Path(
            name
        ).suffix.lower()
        in IMAGE_EXTENSIONS
    )

    stats = {
        "kept_images": 0,
        "excluded_scope": 0,
        "excluded_leakage": 0,
        "excluded_valid_duplicate": 0,
        "object_counts": Counter(),
        "duplicate_counts": Counter(),
    }

    for image_name in image_files:

        filename = Path(
            image_name
        ).name

        # ------------------------------------------
        # Exclude items outside V1 scope
        # ------------------------------------------

        if should_exclude(
            filename
        ):

            stats[
                "excluded_scope"
            ] += 1

            continue

        key = source_key(
            filename
        )

        # ------------------------------------------
        # Prevent Train -> Valid leakage
        # ------------------------------------------

        if (
            split == "train"
            and key
            in valid_source_keys
        ):

            stats[
                "excluded_leakage"
            ] += 1

            continue

        # ------------------------------------------
        # Keep one validation image per source
        # ------------------------------------------

        if (
            split == "valid"
            and image_name
            not in valid_keep_images
        ):

            stats[
                "excluded_valid_duplicate"
            ] += 1

            continue

        # ------------------------------------------
        # Find matching label
        # ------------------------------------------

        label_name = (
            image_name
            .replace(
                "/images/",
                "/labels/",
            )
            .rsplit(
                ".",
                1,
            )[0]
            + ".txt"
        )

        if (
            label_name
            not in archive_name_set
        ):

            raise FileNotFoundError(
                f"Missing label for image: "
                f"{image_name}"
            )

        image_destination = (
            output_images
            / filename
        )

        label_destination = (
            output_labels
            / Path(
                label_name
            ).name
        )

        # ------------------------------------------
        # Copy image unchanged
        # ------------------------------------------

        with archive.open(
            image_name
        ) as source:

            with image_destination.open(
                "wb"
            ) as destination:

                shutil.copyfileobj(
                    source,
                    destination,
                )

        # ------------------------------------------
        # Read original label
        # ------------------------------------------

        original_label = (
            archive.read(
                label_name
            )
            .decode(
                "utf-8",
                errors="replace",
            )
        )

        # ------------------------------------------
        # Convert + clean labels
        # ------------------------------------------

        (
            converted_label,
            counts,
            duplicates,
        ) = convert_label(
            original_label
        )

        label_destination.write_text(
            converted_label,
            encoding="utf-8",
        )

        stats[
            "object_counts"
        ].update(
            counts
        )

        stats[
            "duplicate_counts"
        ].update(
            duplicates
        )

        stats[
            "kept_images"
        ] += 1

    return stats


# --------------------------------------------------
# Ultralytics data.yaml
# --------------------------------------------------

def write_data_yaml() -> None:
    """
    Create final Ultralytics dataset configuration.
    """

    yaml_content = """train: train/images
val: valid/images

nc: 4

names:
  0: plastic
  1: metal
  2: glass
  3: paper_cardboard
"""

    (
        OUTPUT_DIR
        / "data.yaml"
    ).write_text(
        yaml_content,
        encoding="utf-8",
    )


# --------------------------------------------------
# Main
# --------------------------------------------------

def main() -> None:

    # ------------------------------------------
    # Verify source
    # ------------------------------------------

    if not SOURCE_ZIP.exists():

        raise FileNotFoundError(
            f"Dataset ZIP not found:\n"
            f"{SOURCE_ZIP}"
        )

    # ------------------------------------------
    # Prevent accidental overwrite
    # ------------------------------------------

    if OUTPUT_DIR.exists():

        raise SystemExit(
            f"Output already exists:\n"
            f"{OUTPUT_DIR}\n\n"
            "Delete it manually only if you "
            "intentionally want to rebuild "
            "the processed dataset."
        )

    print(
        "Preparing Smart Recycle V1 dataset..."
    )

    print()

    results = {}

    # ------------------------------------------
    # Open source archive
    # ------------------------------------------

    with ZipFile(
        SOURCE_ZIP
    ) as archive:

        archive_names = (
            archive.namelist()
        )

        archive_name_set = set(
            archive_names
        )

        # --------------------------------------
        # Build leakage-safe validation plan
        # --------------------------------------

        (
            valid_source_keys,
            valid_keep_images,
            planned_valid_duplicates_removed,
        ) = build_validation_plan(
            archive_names
        )

        print(
            "Validation unique source groups:",
            len(
                valid_source_keys
            ),
        )

        print(
            "Planned extra validation "
            "images removed:",
            planned_valid_duplicates_removed,
        )

        print()

        # --------------------------------------
        # Process Train + Valid
        # --------------------------------------

        for split in (
            "train",
            "valid",
        ):

            print(
                f"Processing {split}..."
            )

            results[
                split
            ] = prepare_split(
                archive=archive,
                archive_names=archive_names,
                archive_name_set=archive_name_set,
                split=split,
                valid_source_keys=valid_source_keys,
                valid_keep_images=valid_keep_images,
            )

    # ------------------------------------------
    # Write YAML
    # ------------------------------------------

    write_data_yaml()

    # ------------------------------------------
    # Final summary
    # ------------------------------------------

    print()

    print(
        "=" * 64
    )

    print(
        "SMART RECYCLE V1 DATASET SUMMARY"
    )

    print(
        "=" * 64
    )

    total_duplicates_removed = 0

    for split in (
        "train",
        "valid",
    ):

        stats = results[
            split
        ]

        counts = stats[
            "object_counts"
        ]

        duplicates = stats[
            "duplicate_counts"
        ]

        duplicate_total = sum(
            duplicates.values()
        )

        total_duplicates_removed += (
            duplicate_total
        )

        print()

        print(
            split.upper()
        )

        print(
            f"Images kept: "
            f"{stats['kept_images']}"
        )

        print(
            f"Excluded by V1 scope: "
            f"{stats['excluded_scope']}"
        )

        print(
            f"Excluded for split leakage: "
            f"{stats['excluded_leakage']}"
        )

        print(
            f"Extra valid-source images removed: "
            f"{stats['excluded_valid_duplicate']}"
        )

        print()

        print(
            "Objects kept:"
        )

        for (
            class_id,
            class_name,
        ) in enumerate(
            TARGET_NAMES
        ):

            print(
                f"{class_id} "
                f"{class_name}: "
                f"{counts[class_id]}"
            )

        print(
            f"Total objects: "
            f"{sum(counts.values())}"
        )

        print()

        print(
            "Exact duplicate annotations removed:"
        )

        for (
            class_id,
            class_name,
        ) in enumerate(
            TARGET_NAMES
        ):

            print(
                f"{class_id} "
                f"{class_name}: "
                f"{duplicates[class_id]}"
            )

        print(
            f"Total duplicates removed: "
            f"{duplicate_total}"
        )

    print()

    print(
        "=" * 64
    )

    print(
        "TOTAL EXACT DUPLICATE "
        "ANNOTATIONS REMOVED:",
        total_duplicates_removed,
    )

    print(
        "=" * 64
    )

    print()

    print(
        f"Dataset created at: "
        f"{OUTPUT_DIR}"
    )

    print(
        f"Config: "
        f"{OUTPUT_DIR / 'data.yaml'}"
    )


if __name__ == "__main__":
    main()
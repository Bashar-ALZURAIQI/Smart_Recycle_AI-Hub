from collections import defaultdict
from pathlib import Path


# --------------------------------------------------
# Paths
# --------------------------------------------------

ROOT = Path(r"data\processed\waste_v1")

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

def source_key(path: Path) -> str:
    """
    Return the original source-image name before
    Roboflow's augmentation hash.

    Example:

        cardboard-100_jpg.rf.abc123.jpg

    becomes:

        cardboard-100_jpg
    """

    return path.name.lower().split(".rf.")[0]


def get_images(split: str) -> list[Path]:
    """
    Return all supported images from a dataset split.
    """

    images_dir = ROOT / split / "images"

    if not images_dir.exists():
        raise FileNotFoundError(
            f"Images directory not found:\n{images_dir}"
        )

    return sorted(
        path
        for path in images_dir.iterdir()
        if path.is_file()
        and path.suffix.lower() in IMAGE_EXTENSIONS
    )


# --------------------------------------------------
# Main analysis
# --------------------------------------------------

def main() -> None:

    if not ROOT.exists():
        raise FileNotFoundError(
            f"Processed dataset not found:\n{ROOT}"
        )

    train_images = get_images("train")
    valid_images = get_images("valid")

    train_groups = defaultdict(list)
    valid_groups = defaultdict(list)

    # ----------------------------------------------
    # Group Train images by original source
    # ----------------------------------------------

    for image in train_images:
        train_groups[
            source_key(image)
        ].append(image)

    # ----------------------------------------------
    # Group Valid images by original source
    # ----------------------------------------------

    for image in valid_images:
        valid_groups[
            source_key(image)
        ].append(image)

    train_keys = set(
        train_groups
    )

    valid_keys = set(
        valid_groups
    )

    # ----------------------------------------------
    # Train / Valid source leakage
    # ----------------------------------------------

    overlap = sorted(
        train_keys
        & valid_keys
    )

    train_affected = sum(
        len(train_groups[key])
        for key in overlap
    )

    valid_affected = sum(
        len(valid_groups[key])
        for key in overlap
    )

    # ----------------------------------------------
    # Duplicate original sources inside Valid
    # ----------------------------------------------

    valid_duplicate_groups = sorted(
        key
        for key, images
        in valid_groups.items()
        if len(images) > 1
    )

    valid_extra_images = sum(
        len(valid_groups[key]) - 1
        for key in valid_duplicate_groups
    )

    # ----------------------------------------------
    # Duplicate original sources inside Train
    # ----------------------------------------------
    #
    # Multiple augmented Train images from the same
    # original source are allowed. We report them
    # only for information.
    # ----------------------------------------------

    train_multi_groups = sorted(
        key
        for key, images
        in train_groups.items()
        if len(images) > 1
    )

    train_extra_augmented_images = sum(
        len(train_groups[key]) - 1
        for key in train_multi_groups
    )

    # ----------------------------------------------
    # Report
    # ----------------------------------------------

    print(
        "TRAIN IMAGES:",
        len(train_images),
    )

    print(
        "TRAIN UNIQUE SOURCES:",
        len(train_keys),
    )

    print()

    print(
        "VALID IMAGES:",
        len(valid_images),
    )

    print(
        "VALID UNIQUE SOURCES:",
        len(valid_keys),
    )

    print()

    print(
        "OVERLAPPING SOURCE GROUPS:",
        len(overlap),
    )

    print(
        "TRAIN IMAGES FROM OVERLAPPING SOURCES:",
        train_affected,
    )

    print(
        "VALID IMAGES FROM OVERLAPPING SOURCES:",
        valid_affected,
    )

    print()

    print(
        "VALID SOURCE GROUPS WITH >1 IMAGE:",
        len(valid_duplicate_groups),
    )

    print(
        "EXTRA VALID IMAGES FROM SAME SOURCE:",
        valid_extra_images,
    )

    print()

    print(
        "TRAIN SOURCE GROUPS WITH >1 IMAGE:",
        len(train_multi_groups),
    )

    print(
        "EXTRA TRAIN AUGMENTED IMAGES:",
        train_extra_augmented_images,
    )

    print()

    print(
        "FIRST 20 OVERLAPPING SOURCES:"
    )

    if overlap:

        for key in overlap[:20]:

            print(
                key,
                "| train:",
                len(
                    train_groups[key]
                ),
                "| valid:",
                len(
                    valid_groups[key]
                ),
            )

    else:
        print("NONE")

    print()

    print(
        "FIRST 20 DUPLICATED VALID SOURCES:"
    )

    if valid_duplicate_groups:

        for key in valid_duplicate_groups[:20]:

            print(
                key,
                "| valid:",
                len(
                    valid_groups[key]
                ),
            )

    else:
        print("NONE")


if __name__ == "__main__":
    main()
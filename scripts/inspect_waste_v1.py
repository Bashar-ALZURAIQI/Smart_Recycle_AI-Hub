from pathlib import Path
import random
import cv2


ROOT = Path(r"data\processed\waste_v1")
OUTPUT = Path(r"data\inspection\final_labels")

CLASS_NAMES = [
    "plastic",
    "metal",
    "glass",
    "paper_cardboard",
]

random.seed(42)


def draw_sample(split: str, count: int = 6) -> None:
    images_dir = ROOT / split / "images"
    labels_dir = ROOT / split / "labels"
    output_dir = OUTPUT / split

    output_dir.mkdir(parents=True, exist_ok=True)

    images = list(images_dir.glob("*"))
    images = [
        p for p in images
        if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    ]

    selected = random.sample(images, min(count, len(images)))

    for image_path in selected:
        image = cv2.imread(str(image_path))

        if image is None:
            print("FAILED TO READ:", image_path)
            continue

        height, width = image.shape[:2]

        label_path = labels_dir / f"{image_path.stem}.txt"

        for line in label_path.read_text(
            encoding="utf-8"
        ).splitlines():

            if not line.strip():
                continue

            class_id, x, y, w, h = line.split()

            class_id = int(class_id)
            x = float(x)
            y = float(y)
            w = float(w)
            h = float(h)

            x1 = int((x - w / 2) * width)
            y1 = int((y - h / 2) * height)
            x2 = int((x + w / 2) * width)
            y2 = int((y + h / 2) * height)

            cv2.rectangle(
                image,
                (x1, y1),
                (x2, y2),
                (255, 255, 255),
                2,
            )

            cv2.putText(
                image,
                CLASS_NAMES[class_id],
                (x1, max(y1 - 7, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                2,
            )

        destination = output_dir / image_path.name
        cv2.imwrite(str(destination), image)

        print("CREATED:", destination)


draw_sample("train", 6)
draw_sample("valid", 6)

print()
print("Visual inspection samples created.")
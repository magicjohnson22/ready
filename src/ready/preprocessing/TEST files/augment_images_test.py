from pathlib import Path
from PIL import Image, ImageOps
import argparse


def augment_image(image):
    return [
        ("hflip", ImageOps.mirror(image)),
        ("vflip", ImageOps.flip(image)),
        ("rot90", image.rotate(90)),
        ("rot180", image.rotate(180)),
        ("rot270", image.rotate(270)),
    ]


def main():
    parser = argparse.ArgumentParser(description="Resize and augment images.")
    parser.add_argument("--image-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--width", type=int, default=640)
    parser.add_argument("--height", type=int, default=400)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    out_images = Path(args.output_dir) / "images"
    out_images.mkdir(parents=True, exist_ok=True)

    images = sorted(Path(args.image_dir).rglob("*.jpg"))

    if args.limit:
        images = images[:args.limit]

    count = 0

    for image_path in images:
        stem = image_path.stem
        image = Image.open(image_path).convert("RGB")
        image = image.resize((args.width, args.height), Image.Resampling.LANCZOS)
        image.save(out_images / f"{stem}.jpg")
        count += 1

        for name, aug_image in augment_image(image):
            aug_image.save(out_images / f"{stem}_{name}.jpg")
            count += 1

    print(f"Done. {count} total images saved to: {args.output_dir}")


if __name__ == "__main__":
    main()

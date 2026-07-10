from pathlib import Path
from PIL import Image
import argparse

from ready.preprocessing.utils import find_pairs
from ready.preprocessing.geometric import augment_pair
from ready.preprocessing.transforms import augment_image


def main():
    parser = argparse.ArgumentParser(description="Resize and augment image and mask pairs for segmentation training.")
    parser.add_argument("--image-dir",   required=True)
    parser.add_argument("--mask-dir",    required=True)
    parser.add_argument("--output-dir",  required=True)
    parser.add_argument("--width",       type=int, default=640)
    parser.add_argument("--height",      type=int, default=400)
    parser.add_argument("--limit",       type=int, default=None)
    parser.add_argument("--geometric",   action="store_true", help="Apply geometric augmentations")
    parser.add_argument("--photometric", action="store_true", help="Apply photometric augmentations")
    parser.add_argument("--enhancement", action="store_true", help="Apply enhancement augmentations")
    args = parser.parse_args()

    out_images = Path(args.output_dir) / "images"
    out_masks  = Path(args.output_dir) / "masks"
    out_images.mkdir(parents=True, exist_ok=True)
    out_masks.mkdir(parents=True, exist_ok=True)

    pairs, skipped = find_pairs(args.image_dir, args.mask_dir)

    if args.limit:
        pairs = pairs[:args.limit]

    geo_count   = 0
    photo_count = 0
    enh_count   = 0

    for image_path, mask_path in pairs:
        stem  = image_path.stem
        image = Image.open(image_path).convert("RGB")
        mask  = Image.open(mask_path)

        # resize before any augmentation
        # BILINEAR for images - standard for photo resizing (OcularSeg)
        # NEAREST for masks - preserves integer class labels, no blending between classes (RITnet)
        image = image.resize((args.width, args.height), Image.Resampling.BILINEAR)
        mask  = mask.resize((args.width, args.height),  Image.Resampling.NEAREST)

        # save resized original
        image.save(out_images / f"{stem}.jpg")
        mask.save(out_masks   / f"{stem}.png")

        if args.geometric:
            for name, aug_image, aug_mask in augment_pair(image, mask):
                aug_image.save(out_images / f"{stem}_{name}.jpg")
                aug_mask.save(out_masks   / f"{stem}_{name}.png")
                geo_count += 1

        if args.photometric or args.enhancement:
            for name, aug_image in augment_image(image):
                # skip enhancement augmentations if only --photometric passed
                if name in ("equalize", "gamma") and not args.enhancement:
                    continue
                # skip photometric augmentations if only --enhancement passed
                if name not in ("equalize", "gamma") and not args.photometric:
                    continue
                aug_image.save(out_images / f"{stem}_{name}.jpg")
                mask.save(out_masks       / f"{stem}_{name}.png")
                if name in ("equalize", "gamma"):
                    enh_count += 1
                else:
                    photo_count += 1

    total = len(pairs) + geo_count + photo_count + enh_count
    print(f"\nDone. Saved to: {args.output_dir}")
    print(f"  Originals:   {len(pairs)}")
    print(f"  Geometric:   {geo_count}")
    print(f"  Photometric: {photo_count}")
    print(f"  Enhancement: {enh_count}")
    print(f"  Total:       {total}")

    if skipped:
        print(f"\nSkipped {len(skipped)} pairs:")
        for filename, reason in skipped:
            print(f"  - {filename}: {reason}")


if __name__ == "__main__":
    main()

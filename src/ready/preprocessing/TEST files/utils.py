from pathlib import Path
from PIL import Image
 
 
def find_pairs(image_dir, mask_dir):
    """
    Walk mask_dir and find matching images in image_dir.
    Also checks for images with no matching mask.
    Checks each pair exists and is the same size before accepting it.
    Returns valid pairs and a list of (filename, reason) for anything skipped.
    """
    pairs = []
    skipped = []
 
    for mask_path in sorted(Path(mask_dir).rglob("*.png")):
        rel = mask_path.relative_to(mask_dir)
        image_path = Path(image_dir) / rel.with_suffix(".jpg")
 
        if not image_path.exists():
            image_path = Path(image_dir) / rel.with_suffix(".png")
 
        if not image_path.exists():
            skipped.append((mask_path.name, "no matching image found"))
            continue
 
        image_size = Image.open(image_path).size
        mask_size  = Image.open(mask_path).size
 
        if image_size != mask_size:
            skipped.append((mask_path.name, f"image size {image_size} does not match mask size {mask_size}"))
            continue
 
        pairs.append((image_path, mask_path))
 
    # check for images with no matching mask
    for image_path in sorted(Path(image_dir).rglob("*.jpg")):
        rel = image_path.relative_to(image_dir)
        mask_path = Path(mask_dir) / rel.with_suffix(".png")
        if not mask_path.exists():
            skipped.append((image_path.name, "no matching mask found"))
 
    return pairs, skipped
 
 
if __name__ == "__main__":
    import sys
 
    if len(sys.argv) != 3:
        print("Usage: python utils.py <image-dir> <mask-dir>")
        sys.exit(1)
 
    pairs, skipped = find_pairs(sys.argv[1], sys.argv[2])
    print(f"Found {len(pairs)} valid pairs")
 
    print(f"Skipped {len(skipped)} pairs")
    for filename, reason in skipped:
        print(f"  - {filename}: {reason}")
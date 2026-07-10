from PIL import Image, ImageOps


def augment_pair(image, mask):
    """
    Geometric augmentations applied to both image and mask together.
    Uses Image.Transpose for rotations to avoid any interpolation.
    """
    return [
        ("hflip",  ImageOps.mirror(image), ImageOps.mirror(mask)),
        ("vflip",  ImageOps.flip(image),   ImageOps.flip(mask)),
        ("rot90",  image.transpose(Image.Transpose.ROTATE_90),  mask.transpose(Image.Transpose.ROTATE_90)),
        ("rot180", image.transpose(Image.Transpose.ROTATE_180), mask.transpose(Image.Transpose.ROTATE_180)),
        ("rot270", image.transpose(Image.Transpose.ROTATE_270), mask.transpose(Image.Transpose.ROTATE_270)),
    ]

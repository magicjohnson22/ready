from PIL import ImageEnhance, ImageFilter, ImageOps


def augment_image(image):
    """
    Photometric and enhancement augmentations applied to image only.
    Mask is never changed as pixel label values must stay intact.
    """
    return [
        # photometric
        ("brightness_up",   ImageEnhance.Brightness(image).enhance(1.5)),
        ("brightness_down", ImageEnhance.Brightness(image).enhance(0.6)),
        ("contrast_up",     ImageEnhance.Contrast(image).enhance(1.5)),
        ("blur",            image.filter(ImageFilter.GaussianBlur(radius=2))),
        ("grayscale",       ImageOps.grayscale(image).convert("RGB")),
        # enhancement
        ("equalize",        ImageOps.equalize(image)),
        ("gamma",           ImageOps.autocontrast(image)),
    ]

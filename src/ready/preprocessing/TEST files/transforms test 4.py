from PIL import ImageEnhance, ImageFilter, ImageOps


def apply(image, args):
    """
    Photometric and enhancement augmentations applied to image only.
    Mask is never changed as pixel label values must stay intact.
    """
    results = []

    if args.brightness_up:
        results.append(("brightness_up", ImageEnhance.Brightness(image).enhance(args.brightness_up_factor)))

    if args.brightness_down:
        results.append(("brightness_down", ImageEnhance.Brightness(image).enhance(args.brightness_down_factor)))

    if args.contrast_up:
        results.append(("contrast_up", ImageEnhance.Contrast(image).enhance(args.contrast_up_factor)))

    if args.blur:
        results.append(("blur", image.filter(ImageFilter.GaussianBlur(radius=args.blur_factor))))

    if args.grayscale:
        results.append(("grayscale", ImageOps.grayscale(image).convert("RGB")))

    if args.equalize:
        results.append(("equalize", ImageOps.equalize(image)))

    if args.gamma:
        results.append(("gamma", ImageOps.autocontrast(image, cutoff=args.gamma_factor)))

    return results

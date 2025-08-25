import os
from PIL import Image, ImageDraw, ImageFont


def resize_image(file_path, size=(800, 800)):
    img = Image.open(file_path)
    img.thumbnail(size)
    output_path = file_path.replace('uploads', 'processed')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    return output_path


def generate_thumbnail(file_path, size=(128, 128)):
    img = Image.open(file_path)
    img.thumbnail(size)
    base, ext = os.path.splitext(file_path)
    thumb_path = f"{base}_thumbnail{ext}"
    img.save(thumb_path)


def apply_filters_and_watermark(file_path):
    img = Image.open(file_path)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    draw = ImageDraw.Draw(img)
    text = "Watermark"
    font = ImageFont.load_default()
    draw.text((10, 10), text, fill=(255, 0, 0, 180), font=font)
    base, ext = os.path.splitext(file_path)
    wm_path = f"{base}_watermark{ext}"
    img.save(wm_path)

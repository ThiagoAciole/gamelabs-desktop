from PIL import Image, ImageDraw

def round_corners(img: Image.Image, radius: int, border_width: int = 0, border_color=(255, 255, 255, 255)) -> Image.Image:
    """
    Arredonda os cantos de uma imagem PIL e opcionalmente adiciona borda.
    """
    img = img.convert("RGBA")
    w, h = img.size

    # Máscara arredondada
    mask = Image.new("L", (w, h), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle(
        [(0, 0), (w - 1, h - 1)],
        radius=radius,
        fill=255,
    )

    # Aplica transparência
    img.putalpha(mask)

    # Desenha borda se necessário
    if border_width > 0:
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle(
            [
                (border_width // 2, border_width // 2),
                (w - border_width // 2 - 1, h - border_width // 2 - 1),
            ],
            radius=radius,
            outline=border_color,
            width=border_width,
        )

    return img

def crop_image(pil_img: Image.Image, target_size: tuple) -> Image.Image:
    """
    Redimensiona mantendo proporção e corta o excesso (Center Crop) para atingir target_size.
    """
    target_w, target_h = target_size
    img_w, img_h = pil_img.size

    if img_w == 0 or img_h == 0:
        return pil_img

    scale = max(target_w / img_w, target_h / img_h)
    new_w = int(img_w * scale)
    new_h = int(img_h * scale)

    img_resized = pil_img.resize((new_w, new_h), Image.LANCZOS)

    left = (new_w - target_w) / 2
    top = (new_h - target_h) / 2
    right = (new_w + target_w) / 2
    bottom = (new_h + target_h) / 2

    return img_resized.crop((left, top, right, bottom))

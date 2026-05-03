from PIL import Image
import os
import math

def tile_images_keep_aspect(
    input_folder,
    output_path,
    cell_size=(256, 256),
    padding=10,
    bg_color=(255, 255, 255)
):
    # Get PNG files
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".png")]
    image_files.sort()

    if not image_files:
        raise ValueError("No PNG images found.")

    # Load images
    images = [Image.open(os.path.join(input_folder, f)) for f in image_files]

    n = len(images)
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)

    cell_w, cell_h = cell_size

    # Output canvas size
    out_w = cols * cell_w + (cols - 1) * padding
    out_h = rows * cell_h + (rows - 1) * padding

    canvas = Image.new("RGB", (out_w, out_h), color=bg_color)

    for idx, img in enumerate(images):
        row = idx // cols
        col = idx % cols

        # Scale image to fit inside cell (preserve aspect ratio)
        img_ratio = img.width / img.height
        cell_ratio = cell_w / cell_h

        if img_ratio > cell_ratio:
            # Fit to width
            new_w = cell_w
            new_h = int(cell_w / img_ratio)
        else:
            # Fit to height
            new_h = cell_h
            new_w = int(cell_h * img_ratio)

        resized = img.resize((new_w, new_h), Image.LANCZOS)

        # Center inside cell
        x_offset = (cell_w - new_w) // 2
        y_offset = (cell_h - new_h) // 2

        x = col * (cell_w + padding) + x_offset
        y = row * (cell_h + padding) + y_offset

        # Handle transparency if needed
        if resized.mode in ("RGBA", "LA"):
            canvas.paste(resized, (x, y), resized)
        else:
            canvas.paste(resized, (x, y))

    canvas.save(output_path)
    print(f"Saved to {output_path}")


# compute the thumbnail
tile_images_keep_aspect(
    input_folder="input_pngs",
    output_path="tiled_output.png",
    cell_size=(300, 300),
    padding=20
)

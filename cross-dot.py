import os
import numpy as np
from PIL import Image

def create_cross_dot_datasets(input_dir, cross_dir, dot_dir):
    os.makedirs(cross_dir, exist_ok=True)
    os.makedirs(dot_dir, exist_ok=True)

    # Assuming all images are 512x512, 8-bit grayscale
    H, W = 512, 512

    # Precompute masks once
    rows, cols = np.indices((H, W))
    cross_mask = ((rows + cols) % 2 == 0)   # True for Cross pixels
    dot_mask   = ~cross_mask                # True for Dot pixels

    for filename in os.listdir(input_dir):
        if not filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tif", ".tiff")):
            continue

        input_path = os.path.join(input_dir, filename)

        # change extension to .png
        base_name = os.path.splitext(filename)[0]
        cross_output_path = os.path.join(cross_dir, base_name + ".png")
        dot_output_path   = os.path.join(dot_dir,   base_name + ".png")

        try:
            # Load image, ensure grayscale
            img = Image.open(input_path).convert("L")

            # Optionally, sanity check size
            if img.size != (W, H):
                raise ValueError(f"Unexpected size {img.size}, expected (512, 512)")

            arr = np.array(img, dtype=np.uint8)

            # Cross image: keep cross pixels, zero out dot pixels
            cross_arr = np.where(cross_mask, arr, 0).astype(np.uint8)

            # Dot image: keep dot pixels, zero out cross pixels
            dot_arr = np.where(dot_mask, arr, 0).astype(np.uint8)

            # Save as PNG (lossless)
            cross_img = Image.fromarray(cross_arr, mode="L")
            dot_img   = Image.fromarray(dot_arr, mode="L")

            cross_img.save(cross_output_path, format="PNG")
            dot_img.save(dot_output_path,   format="PNG")

            print(f"Processed: {filename} -> {base_name}.png")

        except Exception as e:
            print(f"Failed: {filename} -> {e}")


# Example usage
input_folder = "dataset_final"      # your preprocessed 512x512 grayscale PNG images
cross_folder = "dataset_cross"
dot_folder   = "dataset_dot"

create_cross_dot_datasets(input_folder, cross_folder, dot_folder)
